```python
"""게임 전체 흐름을 관리하는 QuizGame 클래스."""

from input_handler import read_int

LINE = "=" * 40
THIN_LINE = "-" * 40


class QuizGame:
    """퀴즈 목록과 최고 점수를 들고 메뉴 흐름을 진행한다."""

    def __init__(self):
        self.quizzes = []
        self.best_score = None     # 0~100점. 아직 안 풀었으면 None

    def run(self):
        print(LINE)
        print("        🎯 개발자 기초 상식 퀴즈 🎯")
        print(LINE)

        while True:
            self.show_menu()
            choice = read_int("선택: ", 1, 5)
            print()
            if choice == 1:
                self.play()
            elif choice == 2:
                self.add_quiz()
            elif choice == 3:
                self.list_quizzes()
            elif choice == 4:
                self.show_score()
            else:
                self.exit_game()
                break

    def show_menu(self):
        print(LINE)
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")
        print(LINE)

    def exit_game(self):
        print("👋 프로그램을 종료합니다. 다음에 또 만나요!")

    def play(self):
        print("🚧 준비 중입니다.\n")

    def add_quiz(self):
        print("🚧 준비 중입니다.\n")

    def list_quizzes(self):
        print("🚧 준비 중입니다.\n")

    def show_score(self):
        print("🚧 준비 중입니다.\n")

    def save_state(self):
        return False
```
