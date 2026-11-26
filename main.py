```python
"""퀴즈 게임 실행 진입점. 실행: python main.py"""
```bash
- 첫 실행 → "📂 저장된 데이터가 없어 기본 퀴즈로 시작합니다." + 폴더에 `state.json` 생김
- 퀴즈 1개 추가 + 한 판 풀고 종료 → 다시 실행 → "📂 저장된 데이터를 불러왔습니다. (퀴즈 8개, 최고점수 ○점)"
- `cat state.json` → 한글이 그대로 보이는지 (UTF-8)
- 손상 테스트: `echo broken > state.json` 후 실행 → "⚠️ 데이터 파일이 손상되었습니다 … 복구했습니다"
- 테스트 후 정리: `rm -f state.corrupted-*.json` (어차피 .gitignore 대상이라 커밋엔 안 들어감)
- `git status`에 `state.json`이 안 보여야 정상 (.gitignore)
```
`
from pathlib import Path

from game import QuizGame
from storage import StateStore

# 어느 폴더에서 실행하든 항상 프로젝트 루트(이 파일이 있는 폴더)의 state.json을 사용한다.
STATE_PATH = Path(__file__).resolve().parent / "state.json"


def main():
    game = QuizGame(StateStore(STATE_PATH))
    try:
        game.run()
    except (KeyboardInterrupt, EOFError):
        print("\n\n⚠️ 입력이 중단되었습니다. 지금까지의 데이터를 저장하고 종료합니다.")
        if game.save_state():
            print("💾 저장 완료. 안전하게 종료합니다.")


if __name__ == "__main__":
    main()
```