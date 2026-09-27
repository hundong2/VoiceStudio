<div align="center">
  <img src="docs/logo.png" alt="VoiceStudio" width="88" />
  <h1>VoiceStudio</h1>
  <p><a href="https://trendshift.io/repositories/28176?utm_source=repository-badge&amp;utm_medium=badge&amp;utm_campaign=badge-repository-28176"><img src="https://trendshift.io/api/badge/repositories/28176" alt="Trendshift 순위" width="220" height="48" /></a></p>
  <p><strong>646개 언어의 음성 복제, 음성 설계, 영상 더빙, 받아쓰기, 전사, 오디오북 제작을 위한 오픈소스 도구.</strong></p>
  <p>
    <a href="https://voicestudio.sh/?utm_source=github&utm_medium=readme&utm_campaign=project">웹사이트</a> ·
    <a href="https://github.com/debpalash/VoiceStudio/releases/latest">다운로드</a> ·
    <a href="#시작하기">시작하기</a> · <a href="#문서">문서</a> ·
    <a href="https://discord.gg/bzQavDfVV9">Discord</a> ·
    <a href="README.md">English</a> · <a href="README_CN.md">简体中文</a>
  </p>
  <p>
    <a href="https://github.com/debpalash/VoiceStudio/actions/workflows/ci.yml"><img src="https://img.shields.io/github/actions/workflow/status/debpalash/VoiceStudio/ci.yml?branch=main" alt="CI" /></a>
    <a href="https://github.com/debpalash/VoiceStudio/releases/latest"><img src="https://img.shields.io/github/v/release/debpalash/VoiceStudio" alt="최신 릴리스" /></a>
    <a href="LICENSE"><img src="https://img.shields.io/badge/license-AGPL--3.0-blue" alt="AGPL-3.0" /></a>
  </p>
</div>

번역·확인일: 2026-09-27. [원본 README](README.md), 기준 revision `31975717b2d473eb0ddb672f43f3cfc07c800996`.
646개 언어는 프로젝트의 소개 수치이며 모든 엔진이 같은 언어·성능을 지원한다는 뜻은 아닙니다.
배포·후원 링크는 원문의 upstream을 유지했습니다. 이 번역과 추가 학습 자료는 `hundong2/VoiceStudio`에서 관리합니다.

목차: [작업 흐름](#나의-목소리-나의-작업-흐름) · [시작하기](#시작하기) · [문서](#문서) · [후원](#후원) · [라이선스](#라이선스와-책임-있는-사용)

![Electron 앱의 음성 복제, 음성 설계, 더빙, 모델 관리 소개](docs/media/electron/voicestudio.gif)

## 나의 목소리. 나의 작업 흐름.

| 만들기 | 제작하기 | 연결하기 |
| :--- | :--- | :--- |
| 목소리를 복제하거나 새 목소리 설계 | 타이밍에 맞춘 영상 더빙 | 에이전트용 로컬 API와 MCP |
| 떠 있는 위젯으로 받아쓰기 | 이야기, 오디오북, 일괄 작업 | 선택적 원격 워커 |

기본 엔진인 **VoiceStudio**(k2-fsa/OmniVoice 기반)로 시작하거나 다른 엔진을 선택하세요. [기능·엔진 목록](docs/feature-catalog.md).

로컬 작업은 사용자 하드웨어에서 실행됩니다. 원격 서비스는 선택 사항이며 사용 분석에는 동의가 필요합니다.

<details>
<summary><strong>작업 공간 둘러보기</strong> — 복제, 더빙, 설계, 모델</summary>

<table>
  <tr>
    <td><img src="docs/media/electron/voice-cloning.png" alt="데모 음성을 사용한 Electron 음성 복제" width="100%" /></td>
    <td><img src="docs/media/electron/dubbing.png" alt="Electron 영상 더빙" width="100%" /></td>
  </tr>
  <tr><td align="center">음성 복제</td><td align="center">영상 더빙</td></tr>
  <tr>
    <td><img src="docs/media/electron/voice-design.png" alt="원하는 음성 설명하기" width="100%" /></td>
    <td><img src="docs/media/electron/models.png" alt="로컬 음성 모델 설치와 관리" width="100%" /></td>
  </tr>
  <tr><td align="center">음성 설계</td><td align="center">로컬 모델</td></tr>
</table>

<img width="2628" height="1950" alt="VoiceStudio 데스크톱 작업 공간" src="https://github.com/user-attachments/assets/b474497d-a453-49a3-a2dd-f023ec6b7659" />

</details>

## 시작하기

### 한 줄 설치 (macOS / Linux)

다음은 원문의 설치 명령입니다. 원격 스크립트의 출처와 내용을 확인한 뒤 실행하세요. 이 자료 작성 과정에서는 실행하지 않았습니다.

```sh
# 최신 Electron 릴리스
curl -fsSL https://voicestudio.sh/install | sh

# 지정한 Electron 릴리스 (X.Y.Z를 실제 버전으로 교체)
curl -fsSL https://voicestudio.sh/install | sh -s -- --version X.Y.Z

# 현재 main을 빌드해 데스크톱 앱 설치
curl -fsSL https://voicestudio.sh/install | sh -s -- --main

# 데이터는 보존하고 앱 제거
curl -fsSL https://voicestudio.sh/install | sh -s -- --uninstall
```

릴리스 다운로드에는 curl과 SHA-256 도구가 필요합니다. `--main`에는 Git, Node.js 22+, Bun, Rust/Cargo, 플랫폼 빌드 도구가 필요합니다. [설치 전제 조건과 동작](docs/install/script.md)을 확인하세요.
설치기는 설정·프로젝트·모델을 보존합니다. 구버전도 Electron 패키지가 있어야 하며 과거 Tauri 빌드로 되돌아가지 않습니다.

[릴리스](https://github.com/debpalash/VoiceStudio/releases/latest)에서 내려받은 뒤 플랫폼별 안내를 따르세요.

**[macOS](docs/install/macos.md) · [Windows](docs/install/windows.md) · [Linux](docs/install/linux.md) · [Docker](docs/install/docker.md)**

**Voice cloning**을 열고 음성을 선택하거나 잡음 없는 참조 녹음을 추가한 뒤, 텍스트를 입력하고 생성합니다. 안내가 표시되면 필요한 모델을 설치하세요. 엔진별 하드웨어 요구 사항은 [성능 문서](docs/performance.md)를 참고하세요.

### 프롬프트로 설치

코딩 에이전트에 다음 프롬프트를 전달할 수 있습니다.

```text
아래 안내에 따라 이 장치에 VoiceStudio Electron 앱을 설치하고 정상 동작을 확인해 주세요.
https://github.com/debpalash/VoiceStudio/blob/main/docs/install/agent.md
```

[에이전트 안내](docs/install/agent.md)는 하드웨어 탐지, 기존 데이터 재사용, 모델 다운로드 전 확인, 시험 생성을 다룹니다. 스킬을 지원하는 에이전트는 `npx skills add debpalash/VoiceStudio`도 사용할 수 있습니다.

<details>
<summary><strong>소스에서 Electron 미리보기 실행</strong></summary>

```bash
git clone https://github.com/debpalash/VoiceStudio.git
cd VoiceStudio
bun install
bun run setup:api  # Electron 시작 전에 Python 의존성 준비
bun run dev
```

필수 도구와 백엔드 설정은 [Electron 안내](electron/README.md)를 확인하세요.
`bun run smoke-test`는 격리된 패키지형 Electron 앱을 빌드하고 실행합니다. 네트워크를 사용하는 관리형 런타임 설치 확인은 `-- --install`을 추가합니다.

</details>

> **Electron이 유일한 데스크톱 앱이자 웹 UI입니다.** 0.5.3은 마지막 Tauri 릴리스였습니다. 기존 사용자는 [Electron을 별도로 설치](docs/electron-migration.md)해야 합니다. Tauri 셸과 이전 UI 진입점은 제거되었습니다. 플랫폼 문서의 Legacy Tauri 절을 현재 설치법으로 적용하지 마세요.

## 문서

| 필요 사항 | 시작점 |
| --- | --- |
| 설치 지원 | [문제 해결](docs/install/troubleshooting.md) · [모델 다운로드](docs/downloading-models.md) |
| 모델과 음질 | [엔진 안내](docs/engines/README.md) · [벤치마크](docs/benchmarks.md) |
| 연동 | [로컬 API](docs/speech-platform.md) · [MCP](docs/mcp.md) · [예제](examples/README.md) |
| 개발 | [기여](.github/CONTRIBUTING.md) · [Electron](electron/README.md) · [변경 기록](CHANGELOG.md) |
| 한국어 학습 자료 | [기초→심화 가이드](guide/README.md) · [실제 코드 아키텍처](docs/archify/README.md) |

에이전트 스킬: `npx skills add debpalash/VoiceStudio`. 음성 작업에는 **voicestudio**, 저장소 유지보수에는 **voicestudio-maintainer**를 선택합니다.

## 후원

<a href="https://forms.gle/2PYCvd39hbwijzX37"><img src="docs/media/sponsor-slot.svg" alt="VoiceStudio 주요 후원 자리 신청" width="640" /></a>

주요 파트너로 참여하세요. [유료 게재 신청](https://forms.gle/2PYCvd39hbwijzX37) · [이메일](mailto:partner@voicestudio.sh)

개발 지원: [Ko-fi](https://ko-fi.com/debpalash) · [PayPal](https://paypal.me/palashCoder) · [후원 상세](SPONSORS.md)

## 라이선스와 책임 있는 사용

[AGPL-3.0](LICENSE). 모델에는 별도 라이선스가 있으므로 상업적으로 쓰기 전에 확인하세요. 음성 복제는 허락받은 음성으로만 진행하세요. [라이선스 상세](LICENSE-NOTICE.md).
