# 02 — API, 오디오, 저장 구조

[가이드 목차](README.md)

## 오디오 기초

샘플 수 N, 샘플레이트 f가 주어지면 길이는 N/f초입니다. 16-bit PCM은 부호 있는 정수 -32768…32767을 저장합니다. 정규화한 값의 제곱 평균에 제곱근을 취하면 RMS이며, 크기의 최댓값이 peak입니다. 둘 모두 음질·화자 유사도 점수가 아닙니다.

```powershell
python guide/examples/02_practice.py
python guide/examples/02_practice.py --wav path/to/your-consented-recording.wav
```

기본값은 메모리상의 1초 합성 정수 배열을 측정할 뿐 오디오 파일을 만들거나 음성을 합성하지 않습니다. 실제 파일 입력은 무압축 mono PCM16 WAV만 허용합니다. stereo·다른 비트 폭은 거부하여 잘못 해석하는 것을 막습니다. 파일 전체 대신 블록 단위로 읽습니다.

## API 계약 읽기

[speech-platform.md](../docs/speech-platform.md)의 discovery 주소는 `/.well-known/voicestudio-speech`입니다. 백엔드는 상대 경로를 광고합니다. `mcp_stdio`의 path는 셸 실행 명령이고 HTTP URL이 아니므로 모든 path를 URL로 합치면 안 됩니다.

배치 전사 `/v1/audio/transcriptions`와 스트리밍 전사 `/v1/audio/transcriptions/stream`은 별개입니다. 바이너리 오디오를 보내는 WebSocket에서 마지막 제어 메시지는 `{"type":"input_audio.end"}`입니다. 데이터의 sample rate와 프로토콜 파라미터가 일치해야 합니다.

생성 API `/generate`는 `Form` 필드를 받습니다. JSON body라고 가정하지 마세요. 텍스트·언어·참조 녹음·seed·engine 등의 인자를 받으며 `stream=true`일 때 NDJSON 미리보기 경로를 씁니다. 이 TTS 스트림과 ASR WebSocket 이벤트를 혼동하면 안 됩니다.

## 저장소 읽는 순서

| 경로 | 책임 | 확인할 질문 |
| --- | --- | --- |
| `electron/src/main/index.ts` | 데스크톱 시작, supervisor·프로토콜·IPC 구성 | 백엔드 주소와 인증 헤더를 누가 소유하는가? |
| `electron/src/main/protocol.ts` | `app://voicestudio/api` 요청 프록시 | `/api` 제거, 헤더 치환, 파일 경로 검증은 어디인가? |
| `backend/main.py` | 앱 lifecycle·보안·라우터 등록 | 라우터가 정의만 된 것인가 실제 등록됐는가? |
| `backend/api/routers/generation.py` | 생성 요청·엔진 호출·결과 저장 | 추론 실패와 이력 저장 실패가 같은가? |
| `backend/services/tts_backend.py` | 엔진 인터페이스·선택 | 지원 언어·기능·sample rate를 누가 결정하는가? |
| `backend/core/db.py` | SQLite WAL·트랜잭션 | 파일과 DB가 하나의 원자적 트랜잭션인가? |
| `omnivoice/` | 기본 모델 구현 | 애플리케이션 orchestration과 모델 계산의 경계는? |

`_finalize_generation`은 워터마크 경유 → WAV 저장 → 이력 기록 → 정리 → 이벤트 발행 순서입니다. DB 이력 실패 시 음성 파일이 이미 생성됐을 수 있어 “API 성공=모든 저장소 완전 일치”는 아닙니다. 출력·캐시·DB는 성격이 다르므로 백업과 보존 정책도 나누어야 합니다.

과제: 직접 만든 WAV의 sample rate만 잘못 해석했을 때 길이와 재생 속도가 왜 바뀌는지 설명하고, 수치 지표가 좋아도 음질이 나쁜 사례를 적으세요.
