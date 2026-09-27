# 01 — 설치와 안전한 첫 실행

[가이드 목차](README.md)

## 시작 전

음성 복제는 본인 또는 명확한 사용 허락이 있는 음성으로만 수행합니다. 녹음·프로젝트는 개인정보로 취급하고 공유 전 별도로 확인하세요. 생성 음성을 실제 인물의 발언으로 속이지 마세요.

Python 실습만 하려면 Python 3.11+면 충분합니다. 앱은 Electron, Python ML 런타임, 모델을 별도로 필요로 합니다. CPU/GPU의 메모리 요구량은 엔진마다 달라 단일 최소 VRAM 값으로 보장할 수 없습니다.

## 앱 설치 선택

배포 앱은 [공식 upstream 릴리스](https://github.com/debpalash/VoiceStudio/releases/latest)에서 운영체제에 맞는 Electron 패키지를 선택합니다. fork에 같은 릴리스가 있다고 가정하지 않습니다. 모델 설치는 크기·라이선스·저장 위치를 확인한 뒤 명시적으로 시작합니다.

소스 실행은 현재 저장소 루트에서 수행합니다. 이미 submodule로 체크아웃했으면 다시 clone하지 않습니다.

```powershell
git submodule update --init --recursive
node --version
bun --version
uv --version
bun install
bun run setup:api
bun run dev
```

Node.js 22+, manifest의 Bun 버전(분석 시 `bun@1.4.2`), uv/Python, 네이티브 빌드에 필요한 Rust/Cargo·플랫폼 도구를 준비합니다. 위 설치 명령은 패키지 다운로드·디스크 사용을 유발합니다. 세부 요구 사항은 [Electron README](../electron/README.md)와 [설치기 문서](../docs/install/script.md)를 따릅니다. 단순 Python 예제를 실행하려고 이 전체 설치를 할 필요는 없습니다.

현재 데스크톱은 Electron뿐입니다. [Windows 문서](../docs/install/windows.md)의 상단 Electron 절만 현재 경로이며 아래 Legacy Tauri 명령은 새 설치에 사용하지 않습니다.

## 첫 생성 체크리스트

1. Voice cloning에서 데모 음성 또는 허락받은 깨끗한 단일 화자 녹음을 선택합니다.
2. 짧은 문장과 지원 언어를 선택합니다. 다운로드 안내가 나오면 사용자 판단으로 진행합니다.
3. 결과를 들어 누락·발음·잡음·화자 유사도를 기록합니다. 성공 여부와 음질은 별개입니다.
4. 엔진·모델·장치·seed·문장·생성 시간을 기록합니다. 결과 WAV와 이력 저장도 확인합니다.

## 환경변수는 필수인가?

기본 로컬 사용에는 별도 API 키나 환경변수가 필수라는 전제가 없습니다. 설정 UI를 우선 사용하세요. 필요 시 `OMNIVOICE_DATA_DIR`은 사용자 데이터, `OMNIVOICE_CACHE_DIR`은 모델 캐시, `OMNIVOICE_PORT`는 백엔드 포트 등을 조정합니다. 기본 데이터 경로는 Windows `%APPDATA%/OmniVoice`, macOS `~/Library/Application Support/OmniVoice`, Linux `~/.omnivoice`이며 기존 데이터를 삭제하지 마세요.

## 실습 1

```powershell
python guide/examples/01_foundations.py
# 본인이 이미 실행한 로컬 백엔드에 대해서만 선택적으로 조회
python guide/examples/01_foundations.py --live http://127.0.0.1:3900
```

기본 출력은 학습용 fixture의 capability 이름입니다. `--live`는 읽기 전용 discovery GET 한 번만 수행하며 모델을 실행하지 않습니다. 리디렉션·프록시·원격 호스트는 차단합니다. 서비스가 없으면 명확한 오류로 종료됩니다. 이 예제는 인증된 원격 서비스용 범용 SDK가 아닙니다.
