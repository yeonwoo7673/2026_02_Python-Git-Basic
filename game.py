```python
"""게임 전체 흐름을 관리하는 QuizGame 클래스."""

from default_quizzes import get_default_quizzes
from input_handler import read_int
from quiz import Quiz

POINTS_PER_QUESTION = 10   # 문제당 배점
LINE = "=" * 40
THIN_LINE = "-" * 40


class QuizGame:
    """퀴즈 목록과 최고 점수를 들고 메뉴 흐름을 진행한다."""

    def __init__(self):
        self.quizzes = get_default_quizzes()
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
        if not self.quizzes:
            print("📭 등록된 퀴즈가 없습니다. 먼저 '퀴즈 추가'로 퀴즈를 등록해 주세요.\n")
            return

        selected = self.quizzes
        count = len(selected)
        print(f"📝 퀴즈를 시작합니다! (총 {count}문제)")

        correct_count = 0
        earned = 0
        for number, quiz in enumerate(selected, start=1):
            print(THIN_LINE)
            quiz.display(number)
            answer = self._ask_answer(quiz)

            if quiz.is_correct(answer):
                correct_count += 1
                earned += POINTS_PER_QUESTION
                print(f"✅ 정답입니다! (+{POINTS_PER_QUESTION}점)\n")
            else:
                print(f"❌ 오답입니다. 정답은 {quiz.answer}번 '{quiz.answer_text}'입니다.\n")

        score = round(earned / (count * POINTS_PER_QUESTION) * 100)
        self._finish_game(count, correct_count, score)

    def _ask_answer(self, quiz):
        """1~4 사이의 정답 번호를 입력받는다."""
        return read_int(f"정답 입력 (1-{Quiz.CHOICE_COUNT}): ", 1, Quiz.CHOICE_COUNT)

    def _finish_game(self, total, correct, score):
        print(LINE)
        print(f"🏆 결과: {total}문제 중 {correct}문제 정답! ({score}점)")
        print(LINE + "\n")

    def add_quiz(self):
        print("🚧 준비 중입니다.\n")

    def list_quizzes(self):
        print("🚧 준비 중입니다.\n")

    def show_score(self):
        print("🚧 준비 중입니다.\n")

    def save_state(self):
        return False
```