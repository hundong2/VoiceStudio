"""Dependency-free regression tests; no microphone, models, or network required."""
import importlib.util
from pathlib import Path
import struct
import sys
import tempfile
import unittest
from unittest.mock import patch
import wave


def load(name):
    spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(name + ".py"))
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


discovery = load("01_foundations")
audio = load("02_practice")
stream = load("03_advanced")


class DiscoveryTests(unittest.TestCase):
    def test_offline(self):
        self.assertEqual(len(discovery.summarize(discovery.FIXTURE)), 3)

    def test_loopback_only(self):
        for value in ["https://127.0.0.1", "http://example.com", "http://localhost",
                      "http://127.0.0.1/path", "http://user@127.0.0.1",
                      "http://127.0.0.1?x=1", "http://127.0.0.1:0"]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                discovery.local_base(value)
        self.assertEqual(discovery.local_base("http://[::1]:3900/"), "http://[::1]:3900")

    def test_bad_contract(self):
        for value in [None, {}, {"protocol": discovery.PROTOCOL, "endpoints": {}},
                      {"protocol": discovery.PROTOCOL, "endpoints": {"x": None}}]:
            with self.assertRaises(ValueError):
                discovery.summarize(value)

    def test_redirect_rejected(self):
        with self.assertRaises(ValueError):
            discovery.NoRedirect().redirect_request(None, None, 302, "", {}, "http://example.com")

    def test_invalid_target_never_opens(self):
        with patch.object(discovery, "build_opener") as opener:
            with self.assertRaises(ValueError):
                discovery.discover("http://example.com")
            opener.assert_not_called()


class AudioTests(unittest.TestCase):
    def test_known_values(self):
        result = audio.measure([(8192, 2), (-8192, 2)])
        self.assertEqual(result["duration_seconds"], 1)
        self.assertEqual(result["rms"], .25)
        self.assertEqual(result["peak"], .25)

    def test_silence_and_full_scale(self):
        self.assertEqual(audio.measure([(0, 1)])["rms"], 0)
        self.assertEqual(audio.measure([(-32768, 1)])["full_scale_fraction"], 1)

    def test_invalid_samples(self):
        for values in [[], [(0, 0)], [(40000, 1)], [(0, 1), (0, 2)]]:
            with self.assertRaises(ValueError):
                audio.measure(values)

    def test_wav_and_stereo_rejection(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "fixture.wav"
            for channels in [1, 2]:
                with wave.open(str(path), "wb") as wav:
                    wav.setparams((channels, 2, 16000, 0, "NONE", "not compressed"))
                    wav.writeframes(struct.pack("<hh", 0, 8192))
                if channels == 1:
                    self.assertEqual(len(list(audio.pcm16_samples(path))), 2)
                else:
                    with self.assertRaises(ValueError):
                        list(audio.pcm16_samples(path))


class StreamTests(unittest.TestCase):
    def setUp(self):
        self.state = stream.Transcript()
        self.state.accept({"type": "session.started", "session_id": "a"})

    def event(self, **kw):
        self.state.accept({"session_id": "a", **kw})

    def test_summary_not_duplicated(self):
        self.event(type="partial", text="one")
        self.event(type="final", final_kind="utterance", text="one two")
        self.event(type="final", final_kind="summary", text="One two.")
        self.assertEqual(self.state.text(), "One two.")
        self.assertEqual(self.state.partial, "")
        self.assertTrue(self.state.finished)

    def test_empty_summary(self):
        self.event(type="final", final_kind="utterance", text="draft")
        self.event(type="final", final_kind="summary", text="")
        self.assertEqual(self.state.text(), "")

    def test_session_mismatch(self):
        with self.assertRaises(ValueError):
            self.state.accept({"type": "partial", "session_id": "b", "text": "bad"})

    def test_missing_start_and_repeated_start(self):
        with self.assertRaises(ValueError):
            stream.Transcript().accept({"type": "status", "session_id": "a"})
        with self.assertRaises(ValueError):
            self.event(type="session.started")

    def test_unknown_and_invalid_text(self):
        for event in [{"type": "unknown"}, {"type": "partial", "text": 10},
                      {"type": "final", "final_kind": "unknown", "text": "x"}]:
            with self.assertRaises(ValueError):
                self.event(**event)

    def test_error_is_terminal(self):
        with self.assertRaises(RuntimeError):
            self.event(type="error")
        with self.assertRaises(RuntimeError):
            self.state.text()
        with self.assertRaises(ValueError):
            self.event(type="partial", text="late")


if __name__ == "__main__":
    unittest.main()
