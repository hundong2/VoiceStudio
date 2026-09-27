# VoiceStudio 한국어 학습 가이드

작성·확인일: 2026-09-27

## 목차

- [출처와 작업 범위](#출처와-작업-범위)
- [한눈에 보기](#한눈에-보기)
- [학습 순서](#학습-순서)
- [용어 정리](#용어-정리)
- [코드 리뷰와 다음 학습](#코드-리뷰와-다음-학습)

## 출처와 작업 범위

- [대상 fork](https://github.com/hundong2/VoiceStudio), main `31975717b2d473eb0ddb672f43f3cfc07c800996`, package 버전 0.5.6.
- [upstream](https://github.com/debpalash/VoiceStudio), [원본 README](../README.md), [한국어 번역](../README_KO.md).
- 주요 언어: Python 백엔드·음성 처리, TypeScript/React Electron UI, Rust 네이티브 헬퍼. 라이선스는 [AGPL-3.0](../LICENSE), 모델별 조건은 별도.
- 갤러리 중첩 submodule `omnivoice-gallery`: `22e8e6da806fb1904a75db99adb1759832b6ebd0`.
- 코드·문서 기반 학습 자료입니다. 앱 설치, 실제 음성 추론, GPU 성능 검증을 수행했다고 주장하지 않습니다. 실습은 Python 표준 라이브러리만 사용하며 기본값은 오프라인입니다.

## 한눈에 보기

VoiceStudio는 모델 하나가 아니라 음성 제작 작업을 묶은 로컬 우선 애플리케이션입니다. TTS로 문자를 음성으로 만들고, ASR로 녹음을 문자로 바꾸며, 더빙에서는 전사·번역·합성·정렬을 조합합니다. 음성 설계와 참조 녹음 기반 복제는 서로 다른 입력 조건입니다.

646개 언어라는 소개 수치를 엔진별 동일 지원으로 해석하지 마세요. 언어·복제·장치 지원과 모델 라이선스를 함께 확인해야 합니다. 로컬 우선은 설치·업데이트·선택적 클라우드까지 네트워크가 절대 없다는 뜻이 아닙니다.

## 학습 순서

| 단계 | 읽을 자료 | 실습 | 완료 기준 |
| --- | --- | --- | --- |
| 1. 설치·기초 | [01 시작하기](01_getting_started.md) | [기능 탐색](examples/01_foundations.py) | 모델 실행 없이 discovery 응답의 계약 설명 |
| 2. API·오디오 | [02 핵심 개념](02_core_concepts.md) | [WAV 지표](examples/02_practice.py) | duration, peak, RMS 계산과 한계 설명 |
| 3. 안정성·운영 | [03 심화](03_advanced.md) | [스트림 상태 처리](examples/03_advanced.py) | summary/utterance 중복 및 오류 처리 검증 |
| 4. 내부 구조 | [Archify 코드 분석](../docs/archify/README.md) | [검증 기록](validation.md) | UI→API→합성→저장 경계 추적 |

저장소 루트에서 다음 명령은 모델·추가 패키지·네트워크 없이 실행됩니다.

```powershell
python guide/examples/01_foundations.py
python guide/examples/02_practice.py
python guide/examples/03_advanced.py
python -m unittest discover -s guide/examples -p "test_*.py" -v
```

## 용어 정리

| 용어 | 의미와 이 저장소에서의 역할 |
| --- | --- |
| TTS (Text-to-Speech) | 문자를 오디오 텐서로 만드는 엔진 계층 |
| ASR (Automatic Speech Recognition) | 녹음/마이크 음성을 텍스트로 전사 |
| PCM / sample rate | 샘플의 수치 표현 / 초당 샘플 수. 모델 및 재생기의 형식을 맞춰야 함 |
| RTF (Real-Time Factor) | 생성 시간÷오디오 길이. 1보다 작으면 해당 조건에서 실시간보다 빠름 |
| IPC | Electron 프로세스 사이의 제한된 메시지 전달 |
| discovery | 고정 주소를 추측하는 대신 지원 엔드포인트와 프로토콜을 조회 |
| MCP (Model Context Protocol) | 에이전트용 도구 인터페이스. REST API 전체와 동일하지 않음 |
| provenance watermark | 합성 음성 식별 표식. 동의·인증의 대체물이 아님 |
| WAL | SQLite 읽기/쓰기 경합 완화를 위한 로그 방식. 무제한 동시 쓰기를 뜻하지 않음 |

## 코드 리뷰와 다음 학습

핵심 실행 경로와 근거 줄 번호는 [아키텍처 문서](../docs/archify/README.md)에 모았습니다. `backend/main.py`의 라우터 등록, `generation.py`의 생성과 마무리, `tts_backend.py`의 엔진 추상화를 순서대로 읽으세요. 렌더러는 백엔드 포트를 직접 고정하지 않고 앱 프록시를 사용합니다.

확장 지점은 엔진 capability와 생성 인터페이스, 라우터, Electron IPC입니다. 실제 기능 변경 시 세 운영체제의 동작, 21개 locale, offline 테스트, 워터마크 경유 규칙을 지켜야 합니다. [기여 지침](../.github/CONTRIBUTING.md)과 [CLAUDE.md](../CLAUDE.md)를 먼저 읽으세요.

다음 과제: 본인 음성으로 엔진별 RTF·발음 품질 기록 → 긴 텍스트의 청크 경계 평가 → 원격 워커 실패 복구 검증. 검증되지 않은 속도나 모든 언어의 음질을 보장하지 마세요.
