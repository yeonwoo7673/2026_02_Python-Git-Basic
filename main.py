"""퀴즈 게임 실행 진입점. 실행: python main.py"""

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
