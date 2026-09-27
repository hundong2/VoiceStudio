# 03 — 스트림, 보안, 성능과 운영

[가이드 목차](README.md)

## 상태 기반 스트림 처리

ASR 스트림의 `partial`은 계속 바뀌는 중간 결과입니다. `final_kind=utterance`는 구간 확정, `final_kind=summary`는 세션 요약이므로 두 결과를 무조건 이어 붙이면 같은 말을 중복 삽입할 수 있습니다. 세션 ID가 섞이지 않도록 검사하세요.

```powershell
python guide/examples/03_advanced.py
python -m unittest discover -s guide/examples -p "test_*.py" -v
```

예제는 [공식 speech contract](../docs/speech-platform.md)를 좁혀 만든 오프라인 이벤트 reducer입니다. 실제 WebSocket, 마이크, 실시간 전사 엔진, 재접속 프로토콜은 구현하지 않습니다. 완전한 production client가 아닌 상태·오류 처리 학습용입니다. 오류가 발생하면 기존 구간도 성공 transcript로 반환하지 않고 실패를 드러냅니다.

## 신뢰 경계

- Electron 렌더러→main: preload와 IPC는 권한 경계입니다. renderer가 임의의 master 인증 헤더를 덮어쓰지 못하도록 프록시가 치환합니다.
- 로컬→원격: discovery는 원격 bearer 인증을 광고합니다. 외부 공개 시 TLS·최소 노출·비밀 관리가 필요합니다. 예제의 loopback 제한을 삭제해 원격 클라이언트로 쓰지 마세요.
- 백엔드→파일·DB: 참조 음성, 전사, 생성 이력은 민감한 데이터입니다. 로그·공유·백업까지 확인하세요.
- 합성→배포: `mark_synthetic`는 설정·모델 가용성에 따라 통과할 수도 있습니다. 모든 WAV에 항상 표식이 들어간다고 보장하지 않습니다. 동의와 사용 고지는 별도입니다.

## 성능 실험 설계

동일 문장, 참조 녹음, seed, 엔진·모델 revision, 장치, dtype, 청크 설정을 고정합니다. 처음 모델 로드하는 cold run과 로드 후 warm run을 따로 측정합니다. RTF, 최초 청크까지 시간, peak VRAM, 실패율, 사람이 들은 품질을 함께 기록하세요. 짧은 문장의 평균 처리량으로 긴 오디오북의 품질을 추정하지 마세요.

워터마크 CPU 풀과 GPU 추론 풀은 책임이 다릅니다. timeout이나 취소가 있다고 실행 중 GPU 작업이 즉시 해제된다고 가정하지 마세요. `_TempReferenceLease`처럼 임시 파일을 읽는 작업이 끝날 때까지 수명을 관리하는 코드도 확인합니다.

## 문제 해결

| 증상 | 먼저 확인할 것 |
| --- | --- |
| 연결 거부/503 | 백엔드 준비 상태·실제 포트·supervisor 로그, renderer proxy 경로 |
| 첫 생성 실패 | 엔진별 설치 상태·지원 언어·디스크와 메모리, 암묵 다운로드 금지 |
| 음성이 빠르거나 느림 | sample rate·채널·컨테이너·PCM 형식 |
| 전사 중복 | summary/utterance 구분, session_id 혼합 여부 |
| WAV는 있으나 이력이 없음 | DB 쓰기/복구 로그, 데이터 폴더 권한 |
| Windows GPU가 기대와 다름 | 엔진별 장치 지원, 실제 PyTorch 런타임; 모든 가속기를 보장하지 않음 |

## 검증·배포·기여

공식 테스트는 `HF_HUB_OFFLINE=1`과 **비어 있는 임시 HF_HUB_CACHE**를 사용합니다. 개발 캐시를 그대로 쓰면 누락 모델을 놓칩니다. [검증 기록](validation.md)에 이번 작업에서 수행한 것과 미실행한 것을 구분했습니다.

의존성을 준비한 별도 개발 환경에서는 CI 정의에 따라 다음을 실행합니다.

```sh
uv run --no-sync pytest tests/ -q --tb=short
uv run --no-sync pytest backend/tests/ -q --tb=short
bun run check:electron
bun run test:frontend
```

위 명령 전 환경변수를 설정해야 합니다. 브라우저 smoke·네이티브·운영체제 matrix·컨테이너 검증을 이 네 줄로 대체하지 않습니다. Docker는 renderer 빌드와 Python 런타임을 분리하고 CUDA/ROCm 기반 torch를 유지하는 guard가 있습니다. lockfile 변경은 Docker의 frozen install까지 영향을 주므로 의존성 변경 시 전체 소비자를 검증합니다.

실제 확장은 작은 엔진 adapter→capability 테스트→라우팅→UI locale→세 운영체제 동작 순서로 진행하세요. 아키텍처 전체는 [Archify 분석](../docs/archify/README.md)을 참고합니다.
