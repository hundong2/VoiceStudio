"""Check local documentation links and the artifact-bound architecture evidence."""
import hashlib
import json
from pathlib import Path
import re
import unittest
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[2]
DOCUMENTS = [ROOT / "README.md", ROOT / "README_KO.md",
             *sorted((ROOT / "guide").glob("*.md")), ROOT / "docs/archify/README.md"]


class DocumentationTests(unittest.TestCase):
    def test_local_links(self):
        checked = 0
        for document in DOCUMENTS:
            text = document.read_text(encoding="utf-8")
            targets = re.findall(r'\]\(([^)]+)\)', text)
            targets += re.findall(r'(?:src|href)="([^"]+)"', text)
            for target in targets:
                url = urlsplit(target)
                if url.scheme or url.netloc:
                    continue
                path = (document.parent / unquote(url.path)).resolve() if url.path else document
                with self.subTest(document=document.name, target=target):
                    self.assertTrue(path.exists(), f"Missing local target: {target}")
                    if url.fragment and path.suffix == ".md":
                        body = path.read_text(encoding="utf-8")
                        headings = re.findall(r'^#{1,6}\s+(.+)$', body, flags=re.M)
                        anchors = {re.sub(r'[^\w\s-]', '', h.lower()).replace(' ', '-') for h in headings}
                        anchors.update(re.findall(r'id="([^"]+)"', body))
                        self.assertIn(unquote(url.fragment), anchors)
                    checked += 1
        self.assertGreater(checked, 80)

    def test_artifact_receipt(self):
        directory = ROOT / "docs/archify"
        receipt = json.loads((directory / "architecture.visual-check.json").read_text(encoding="utf-8"))
        artifact = (directory / "architecture.html").read_bytes()
        self.assertEqual(hashlib.sha256(artifact).hexdigest(), receipt["artifact"]["sha256"])
        self.assertEqual(len(artifact), receipt["artifact"]["bytes"])
        self.assertEqual(receipt["status"], "pass")
        self.assertEqual(len(receipt["containment"]["viewports"]), 4)
        for capture in receipt["captures"]["screenshots"]:
            self.assertTrue((directory / capture["file"]).is_file())


if __name__ == "__main__":
    unittest.main()
