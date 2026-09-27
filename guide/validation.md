# 검증 기록

기준일: 2026-09-27. [가이드](README.md) · [아키텍처 검증](../docs/archify/README.md)

## 이번 작업의 범위

한국어 README·단계별 문서·독립 Python 예제·아키텍처 산출물입니다. 애플리케이션 실행 코드, 의존성, 버전, lockfile, 모델 설정은 변경하지 않습니다. 한국어 문서를 기존 CJK 검사에서 허용하기 위해 **문서 파일만** 정확한 경로로 허용 목록에 추가합니다. UI 전체나 제품 코드를 예외 처리하지 않습니다.

## 검증 범위와 제한

- Python 표준 라이브러리 예제 3개 기본 실행 및 unittest 17개 통과(실습 15개, 링크·artifact receipt 2개).
- CJK·버전·locale parity·changelog 정적 테스트 549개 통과. 기존 locale baseline 개선 알림 18개는 경고로 남아 있으며 UI 번역 데이터를 임의로 바꾸지 않았습니다.
- CJK 검사는 한국어 문서 9개에서 먼저 실패함을 확인하고, 그 문서만 허용한 뒤 통과했습니다. 제품 코드의 CJK 차단은 유지됩니다.
- 처음 버전 검사 1개는 패키지가 설치되지 않아 실패했습니다. 별도 임시 Python 3.11 환경에 pytest와 현재 프로젝트 wheel을 `--no-deps`로 설치한 뒤 재검증했습니다. 이는 앱 의존성 설치·실행 검증이 아닙니다.
- 테스트에는 `HF_HUB_OFFLINE=1`과 매번 새로 만든 빈 HF_HUB_CACHE를 사용했습니다. 기존 모델·사용자 데이터는 사용하지 않았습니다.
- Archify: 9/9 artifact checks, composition error 0 / warning 0, 4개 viewport containment 통과. 두 테마 이미지 직접 확인.
- 모델은 다운로드하지 않았으며 음성 합성, 녹음, GPU, 실제 앱 설치는 실행하지 않았습니다.
- 현재 호스트에는 Bun과 전체 Python ML 의존성이 없습니다. 전체 Electron 빌드·backend 통합·OS matrix·Docker build 성공을 주장하지 않습니다.
- fork의 GitHub Actions 조회에서 작업 시작 시 workflow/run 목록이 비어 있었습니다. 이는 CI 통과가 아니라 원격 검증 증거가 없다는 뜻입니다.

## CI 영향 검토

| 정의 | 검증하는 대상 | 이번 변경과 관계 |
| --- | --- | --- |
| `ci.yml` | installer, Python/backend, Electron, 브라우저 smoke, Linux native, macOS/Intel/Windows/Linux smoke | CJK 문서 허용·버전·locale 등 정적 규칙 확인 필요; 전체 런타임 matrix는 별도 |
| `security.yml` | secret scan, JS/TS·Python CodeQL, backend Bandit, 의존성 감사 | 학습 예제는 원격 접근·명령 실행을 하지 않는 기본값; 원격 CodeQL 실행은 미확인 |
| `docker.yml` + `deploy/Dockerfile` | CUDA·ROCm 이미지, frozen JS install, GPU torch guard | package/lockfile/runtime COPY 경로를 바꾸지 않음; 새 학습 파일은 제품 빌드 입력으로 추가하지 않음 |
| `electron-build.yml` / `electron-release.yml` | 수동 패키지, 태그 릴리스 | 배포·버전·태그 변경 없음 |
| `install-smoke.yml` / `build-omnivoice-tts.yml` / `cosyvoice-dependencies.yml` | 경로 필터 기반 설치·native·엔진 의존성 | 해당 구현·의존성 파일 변경 없음 |
| `docs-drift.yml` / `evals.yml` | 예약·수동 문서 점검과 평가 | 기능 inventory·평가 데이터·모델 변경 없음 |

전체 플랫폼의 성공 증거가 필요하다면 필요한 개발 도구와 의존성을 갖춘 CI에서 현재 revision을 검증해야 합니다. 문서·toy 예제 검사만으로 제품 성능이나 배포 가능성을 보장하지 않습니다.

## 게시 상태

전체 active CI 검증 조건은 아직 충족하지 못했습니다. 이 제한을 보고한 뒤 사용자가 2026-09-27에 이번 작업의 commit·push를 명시적으로 요청하여, 위의 제한된 검증 범위로 게시합니다. 이 승인은 전체 CI 통과를 의미하거나 향후 작업의 검증 규칙을 변경하지 않습니다. 기존 다른 주제의 미커밋 파일은 포함하지 않습니다.
