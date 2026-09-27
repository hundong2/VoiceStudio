# VoiceStudio 코드 아키텍처

작성·확인일: 2026-09-27

목차: [분석 범위](#분석-범위) · [코드 근거](#코드-근거) · [경계와 한계](#경계와-한계) · [검증](#검증)

[HTML 뷰어](architecture.html) · [원본 명세](architecture.json) · [시각 증거](architecture.visual-check.html) · [학습 가이드](../../guide/README.md)

GitHub에서는 HTML이 직접 실행되지 않으므로 파일을 내려받아 브라우저에서 여세요. standalone HTML의 생성 코드·SVG는 파일 안에 포함됩니다.

## 분석 범위

- 저장소: <https://github.com/hundong2/VoiceStudio>
- 분석 revision: `31975717b2d473eb0ddb672f43f3cfc07c800996` (문서 추가 전 main)
- 대표 경로: Electron 데스크톱의 로컬 `/generate` 요청과 결과 저장.
- 구성요소 8개, 관계 7개, 코드 참조 17개. 전 시스템의 모든 기능을 나열한 배포도가 아닙니다.
- 한국어로 작성했지만 Archify 2.17 Viewer의 한국어 locale은 지원되지 않아 `meta.locale`을 생략했습니다. 고정 UI와 `<html lang>`은 영어 fallback이며 완전한 UI 번역은 아닙니다.

## 코드 근거

| 구성요소 | 증거 | 확인한 관계 |
| --- | --- | --- |
| 생성 UI | [`generate.ts`](../../electron/src/shared/api/generate.ts#L28), [`client.ts`](../../electron/src/shared/api/client.ts#L361) | FormData를 `apiFetch('/generate')`로 전송 |
| 앱 프록시 | [`protocol.ts`](../../electron/src/main/protocol.ts#L100) | `/api`를 제거하고 `net.fetch`로 backend에 전달 |
| 백엔드 관리 | [`index.ts`](../../electron/src/main/index.ts#L242), [`backend.ts`](../../electron/src/main/backend.ts) | `BackendSupervisor`를 생성하고 주소·인증 헤더 콜백 제공 |
| 생성 라우터 | [`main.py`](../../backend/main.py#L763), [`generation.py`](../../backend/api/routers/generation.py#L1558) | 실제 등록된 라우터가 Form 인자를 받아 생성 작업 구성 |
| 음성 엔진 | [`tts_backend.py`](../../backend/services/tts_backend.py#L488), [`generation.py`](../../backend/api/routers/generation.py#L2220) | TTSBackend 인터페이스의 `generate` 호출 |
| 결과 마무리 | [`generation.py`](../../backend/api/routers/generation.py#L1301) | `_finalize_generation`이 워터마크·저장·이력을 처리 |
| 생성 이력 | [`db.py`](../../backend/core/db.py#L15), [`generation.py`](../../backend/api/routers/generation.py#L1351) | SQLite WAL 연결과 이력 INSERT |
| 음성 파일 | [`generation.py`](../../backend/api/routers/generation.py#L1343), [`config.py`](../../backend/core/config.py) | OUTPUTS_DIR 아래 WAV 저장 |

요청이 왼쪽에서 오른쪽으로 전달됩니다. 생성 라우터의 엔진 호출은 텐서를 반환한 뒤 마무리 함수로 이어지며, 복잡도를 낮추려고 반환선은 생략했습니다. 위·아래 분기는 독립 마이크로서비스라는 뜻이 아니라 코드 책임 단위입니다.

`_finalize_generation`은 WAV를 먼저 쓰고 이력을 뒤에 기록합니다. SQL 쓰기 실패 시 schema self-heal을 한 번 시도하고 여전히 실패하더라도 오디오를 반환할 수 있습니다. 두 저장소 사이에 분산 트랜잭션이 있는 것처럼 읽으면 안 됩니다.

## 경계와 한계

Electron main은 renderer가 전달한 authorization을 그대로 신뢰하지 않고 관리되는 헤더로 치환합니다. 개발 환경의 프록시와 패키지 환경의 app protocol은 구현이 달라 이 그림은 패키지형 로컬 경로를 대표합니다. 원격 백엔드·bearer/TLS 운영은 [speech platform](../speech-platform.md)을 별도로 읽으세요.

워터마크 chokepoint 경유와 실제 AudioSeal 삽입 성공은 다릅니다. 설정·가용성·실패 처리에 따라 통과할 수 있어 안전 보장으로 표현하지 않았습니다. 엔진별 subprocess·모델 캐시, ASR, 네이티브 받아쓰기, 더빙, MCP, 원격 워커, opt-in analytics, 전체 GPU pool 수명은 그림에서 제외했습니다.

테스트 근거는 [`test_watermark_route_coverage.py`](../../tests/test_watermark_route_coverage.py), [`test_generation_history_self_heal.py`](../../tests/test_generation_history_self_heal.py), [`client.test.ts`](../../electron/src/shared/api/client.test.ts) 등에 있습니다. 이 링크는 해당 테스트를 모두 실행했다는 뜻이 아닙니다. [별도 검증 기록](../../guide/validation.md)을 확인하세요.

배포 근거인 [`deploy/Dockerfile`](../../deploy/Dockerfile)은 React renderer build와 Python GPU runtime을 분리합니다. Docker 배포와 Electron 프로세스를 같은 런타임으로 합쳐 그리지 않았습니다.

## 검증

Archify schema v1, `architecture`, `showcase`. 초기 자동 배치에서 두 수직 라벨이 노드와 겹쳐 validator가 제안한 `labelAt`을 각각 적용했습니다. 최종 후보는 validation 이후 수정하지 않았습니다.

```text
diagram_type: architecture
output: D:/workspace/laboratory/VoiceStudio/docs/archify/architecture.html
specification_sha256: 94386c5c3b62b0aeaeafc3c285e17d9cc525ca899742fc3802e04306fef213da
specification_bytes: 4435
artifact_sha256: d3e837520c5f03eb8fd8f6bca5743b42b724c4b168febbc1b30671b487bf6fe8
artifact_bytes: 714908
validation: 9/9 showcase, 0 errors, 0 warnings
browser_evidence: passed
visual_review: passed
correction_rounds: 0
```

`correction_rounds`는 deliver 후 시각 검토에 따른 재생성 횟수이며, deliver 전 라벨 진단 수정 2회와 별개입니다. `deliver`의 byte identity, 자동 브라우저 증거, 이미지 검토는 다른 증거입니다.

[자동 receipt](architecture.visual-check.json)는 1440×900, 1600×1000, 1920×1080, 2048×1320 light 화면의 overflow 없음과 1440/2048 light·dark 캡처를 기록합니다. receipt의 `visualReview: pending`은 자동화가 사람/이미지 판단을 대신하지 않기 때문에 그대로 보존했습니다.

실제 1440×900 light와 2048×1320 dark 이미지를 열어 글자·노드·카드 잘림, 교차, 라벨 충돌, 하단 여백을 검토했습니다. 두 테마 모두 주요 흐름과 주의 사항을 읽을 수 있고 결함을 발견하지 못했습니다. 모든 상호작용·export 형식을 수동으로 누른 검증은 아니며 본 검토는 기본 READ/Still 화면 범위입니다.
