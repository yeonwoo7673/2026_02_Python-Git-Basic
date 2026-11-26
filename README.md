# 🎯 개발자 기초 상식 퀴즈 게임

## 프로젝트 개요

- 터미널에서 실행하는 객관식 퀴즈 게임
- **Python 기본 문법**, **표준 라이브러리 사용**, **클래스별 역할 구분**
- 퀴즈, 점수 기록은 `state.json`에 저장, 프로그램 종료/시작 후 유지
- 언어: Python 3.12.10
- 표준 라이브러리: `json`, `random`, `datetime`, `pathlib`, `os`

## 퀴즈 주제와 선정 이유

**주제: 개발자 기초 상식 (Python · Git · 웹 · DB · 객체 지향)**
이번 과정에서 Python을 활용해 문제를 만들고, 풀고, 추가하고, 삭제하는 메서드를 구현하고 싶었습니다. 힌트와 보너스 개념 또한 추가하여 진짜 게임을 하는 것 같은 느낌이 들도록 하고 싶었습니다.

## 실행 방법

```bash
# 1. 저장소 복제
git clone https://github.com/yeonwoo7673/2026_02_Python-Git-Basic.git
cd <2026_02_python-git-basic>

# 2. Python 버전 확인 (3.10 이상)
python 3.12.10

# 3. 실행 (macOS/Linux에서 python이 없으면 python3)
python main.py
```

![버전 확인, 실행](docs/screenshots/02.python%20--version,%20main.py.png)

- 메뉴에서 번호를 입력해 기능을 고릅니다.
- 실행 중 `Ctrl+C`를 눌러도 데이터를 저장한 뒤 안전하게 종료됩니다.

## 기능 목록

### 기본 기능
| 메뉴 | 기능 | 설명 |
|---|---|---|
| 1 | 퀴즈 풀기 | 저장된 퀴즈를 출제하고 정답/오답을 알려준 뒤 결과(점수)를 표시 |
| 2 | 퀴즈 추가 | 문제, 선택지 4개, 정답 번호, (선택) 힌트를 입력받아 등록 후 저장 |
| 3 | 퀴즈 목록 | 등록된 퀴즈 목록 출력 (💡 = 힌트 있음) |
| 4 | 점수 확인 | 최고 점수와 최근 게임 기록 출력 |
| 5 | 퀴즈 삭제 | 번호로 골라 확인(y/n) 후 삭제, 파일에 반영 |
| 6 | 종료 | 저장 후 종료 |

### 보너스 기능
- **랜덤 출제**: `random.sample()`로 매번 문제 순서를 섞어 출제
- **문제 수 선택**: 풀기 전에 1~(전체 개수) 중 몇 문제를 풀지 선택
- **힌트**: 💡 표시 문제에서 `h` 입력 시 힌트 표시. 힌트를 보고 맞히면 10점 → 5점
- **퀴즈 삭제**: 메뉴 5번
- **점수 기록 히스토리**: 게임마다 날짜/시간, 푼 문제 수, 정답 수, 힌트 사용 수, 점수를 저장

### 점수 계산
- 문제당 10점, 힌트를 사용하고 맞히면 5점, 틀리면 0점
- 최종 점수 = 얻은 점수 ÷ (문제 수 × 10) × 100 (반올림, 100점 만점)
- 문제 수가 달라도 비교할 수 있도록 100점 만점으로 환산해 최고 점수와 비교합니다.

### 입력/예외 처리
- 입력 앞뒤 공백 제거 (` 1 ` → `1`)
- 빈 입력, 숫자가 아닌 입력(`abc`), 범위 밖 숫자(`9`, `0`)는 안내 후 다시 입력
- `Ctrl+C`(KeyboardInterrupt), 입력 끝(EOFError) 발생 시 저장 후 안전하게 종료
- `state.json`이 없으면 기본 퀴즈로 시작
- `state.json`이 손상되면 안내 후 `state.corrupted-날짜시간.json`으로 백업하고 기본 데이터로 복구

## 파일 구조

```
.
├── main.py              # 실행 진입점, Ctrl+C/EOF 처리
├── game.py              # QuizGame 클래스: 메뉴, 풀기/추가/목록/점수/삭제, 저장·불러오기 흐름
├── quiz.py              # Quiz 클래스: 문제 1개 (출력, 정답 확인, dict 변환)
├── storage.py           # StateStore 클래스: state.json 읽기/쓰기, 손상 파일 백업
├── input_handler.py     # 공통 입력 검증 함수 (숫자 범위, 빈 입력, y/n)
├── default_quizzes.py   # 기본 퀴즈 7개
├── state.json           # 실행하면 자동 생성되는 데이터 파일 (.gitignore로 제외)
├── docs/
│   └── screenshots/     # 실행 화면 캡처
├── .gitignore
└── README.md
```

### 클래스별 역할
| 클래스 | 책임 |
|---|---|
| `Quiz` | 퀴즈 1개의 데이터와 검증, 화면 출력, 정답 확인 |
| `QuizGame` | 게임 전체 상태(퀴즈 목록, 최고 점수, 기록)와 메뉴 흐름 |
| `StateStore` | 파일 입출력만 담당 (게임 로직은 모름) |

## 데이터 파일 설명 (`state.json`)

- **경로**: 프로젝트 루트의 `state.json` (`main.py`와 같은 폴더, 어디서 실행해도 같은 위치)
- **인코딩**: UTF-8 (한글이 그대로 보이도록 `ensure_ascii=False`)
- **역할**: 퀴즈 목록, 최고 점수, 게임 기록을 저장해 재실행 후에도 유지
- **생성 시점**: 첫 실행 시 자동 생성되고, 퀴즈 추가/삭제, 게임 종료, 프로그램 종료 때마다 저장
- **저장 방식**: 임시 파일(`state.json.tmp`)에 먼저 쓴 뒤 교체하여, 저장 도중 문제가 생겨도 기존 파일이 깨지지 않음
- **Git 관리**: 개인 플레이 기록이므로 `.gitignore`에 넣어 저장소에는 올리지 않음

### 스키마

```json
{
    "quizzes": [
        {
            "question": "Python에서 리스트의 맨 끝에 요소 하나를 추가하는 메서드는?",
            "choices": ["append()", "insert()", "extend()", "add()"],
            "answer": 1,
            "hint": "'덧붙이다'라는 뜻의 영어 단어예요."
        }
    ],
    "best_score": 80,
    "best_record": {
        "played_at": "2026-11-25 19:40:00",
        "total": 5,
        "correct": 4,
        "hints_used": 0,
        "score": 80
    },
    "history": [
        {
            "played_at": "2026-11-25 19:40:00",
            "total": 5,
            "correct": 4,
            "hints_used": 0,
            "score": 80
        }
    ]
}
```

| 키 | 타입 | 설명 |
|---|---|---|
| `quizzes` | list | 퀴즈 목록 (필수) |
| `quizzes[].question` | str | 문제 |
| `quizzes[].choices` | list[str] | 선택지 4개 |
| `quizzes[].answer` | int | 정답 번호 (1~4) |
| `quizzes[].hint` | str | 힌트 (없으면 빈 문자열) |
| `best_score` | int \| null | 최고 점수 (0~100), 아직 안 풀었으면 `null` |
| `best_record` | object \| null | 최고 점수를 낸 게임의 기록 |
| `history` | list | 모든 게임 기록 (`played_at`, `total`, `correct`, `hints_used`, `score`) |

`best_record`, `history`, `hint`가 없는 예전 형식의 파일도 그대로 불러올 수 있습니다.

## 실행 화면

| 메뉴 | 퀴즈 풀기 |
|---|---|
| ![menu](docs/screenshots/menu.png) | ![play](docs/screenshots/play.png) |

| 퀴즈 추가 | 점수 확인 |
|---|---|
| ![add](docs/screenshots/add_quiz.png) | ![score](docs/screenshots/score.png)
