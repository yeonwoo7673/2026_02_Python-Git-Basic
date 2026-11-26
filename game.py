```python
"""게임 전체 흐름을 관리하는 QuizGame 클래스."""

import random
from default_quizzes import get_default_quizzes
from input_handler import parse_int, read_int, read_line, read_text, read_yes_no
from quiz import Quiz
from storage import StateFileError

POINTS_PER_QUESTION = 10   # 문제당 배점
HINT_PENALTY = 5           # 힌트를 보고 맞히면 차감되는 점수LINE = "=" * 40
THIN_LINE = "-" * 40


class QuizGame:
    """퀴즈 목록과 최고 점수를 들고 메뉴 흐름을 진행한다."""

    def __init__(self, store):
        self.store = store
        self.quizzes = []
        self.best_score = None     # 0~100점. 아직 안 풀었으면 None
        self.menu = [
            ("퀴즈 풀기", self.play),
            ("퀴즈 추가", self.add_quiz),
            ("퀴즈 목록", self.list_quizzes),
            ("점수 확인", self.show_score),
            ("퀴즈 삭제", self.delete_quiz),
            ("종료", None),
        ]

    def run(self):
        print(LINE)
        print("        🎯 개발자 기초 상식 퀴즈 🎯")
        print(LINE)
        print(self.load_state())

        while True:
            self.show_menu()
            choice = read_int("선택: ", 1, len(self.menu))
            label, handler = self.menu[choice - 1]
            if handler is None:
                self.exit_game()
                return
            print()
            handler()

    def show_menu(self):
        print(LINE)
        for number, (label, _) in enumerate(self.menu, start=1):
            print(f"{number}. {label}")
        print(LINE)

    def exit_game(self):
        self.save_state()
        print("👋 프로그램을 종료합니다. 다음에 또 만나요!")

    def play(self):
        if not self.quizzes:
            print("📭 등록된 퀴즈가 없습니다. 먼저 '퀴즈 추가'로 퀴즈를 등록해 주세요.\n")
            return

        available = len(self.quizzes)
        count = read_int(f"몇 문제를 풀까요? (1-{available}): ", 1, available)
        selected = random.sample(self.quizzes, count)  # 중복 없이 무작위로 뽑기 = 섞기

        # 1 → "몇 문제를 풀까요? (1-퀴즈 개수)" / `0`, `99` 거절 / `2` → 2문제만 출제
        print(f"\n📝 퀴즈를 시작합니다! (총 {count}문제, 순서 랜덤)")
        print(f"💡 표시가 있는 문제는 h를 입력하면 힌트를 볼 수 있어요. (정답 시 {HINT_PENALTY}점 차감)")

        correct_count = 0
        hints_used = 0
        earned = 0
        for number, quiz in enumerate(selected, start=1):
            print(THIN_LINE)
            quiz.display(number)
            answer, used_hint = self._ask_answer(quiz)
            if used_hint:
                hints_used += 1

            if quiz.is_correct(answer):
                gained = POINTS_PER_QUESTION - (HINT_PENALTY if used_hint else 0)
                correct_count += 1
                earned += gained
                print(f"✅ 정답입니다! (+{gained}점)\n")
            else:
                print(f"❌ 오답입니다. 정답은 {quiz.answer}번 '{quiz.answer_text}'입니다.\n")

        score = round(earned / (count * POINTS_PER_QUESTION) * 100)
        self._finish_game(count, correct_count, hints_used, score)

    def _ask_answer(self, quiz):
        """정답 번호를 입력받는다. h 입력 시 힌트를 보여준다.

        돌려주는 값: (정답 번호, 힌트 사용 여부)
        """
        used_hint = False
        prompt = "정답 입력 (1-4, 힌트 h): " if quiz.has_hint() else "정답 입력 (1-4): "
        while True:
            text = read_line(prompt)
            if text.lower() == "h":
                if not quiz.has_hint():
                    print("🙅 이 문제에는 힌트가 없습니다.")
                else:
                    if not used_hint:
                        print(f"(힌트 사용: 이 문제는 맞혀도 {HINT_PENALTY}점 차감)")
                    used_hint = True
                    print(f"💡 힌트: {quiz.hint}")
                continue

            value, error = parse_int(text, 1, Quiz.CHOICE_COUNT)
            if error is None:
                return value, used_hint
            print(f"⚠️ {error}")

    def _finish_game(self, total, correct, hints_used, score):
        is_new_best = self.best_score is None or score > self.best_score
        if is_new_best:
            self.best_score = score

        print(LINE)
        print(f"🏆 결과: {total}문제 중 {correct}문제 정답! ({score}점)")
        if hints_used:
            print(f"   힌트 사용: {hints_used}회")
        if is_new_best:
            print("🎉 새로운 최고 점수입니다!")
        else:
            print(f"   (최고 점수: {self.best_score}점)")
        print(LINE + "\n")
        self.save_state()

    def add_quiz(self):
        print("📌 새로운 퀴즈를 추가합니다.\n")
        question = read_text("문제를 입력하세요: ")

        choices = []
        while len(choices) < Quiz.CHOICE_COUNT:
            choice = read_text(f"선택지 {len(choices) + 1}: ")
            if choice in choices:
                print("⚠️ 이미 입력한 선택지입니다. 다른 내용을 입력하세요.")
                continue
            choices.append(choice)

        answer = read_int(f"정답 번호 (1-{Quiz.CHOICE_COUNT}): ", 1, Quiz.CHOICE_COUNT)
        hint = read_line("힌트 (없으면 그냥 Enter): ")

        self.quizzes.append(Quiz(question, choices, answer, hint))
        if self.save_state():
            print("\n✅ 퀴즈가 추가되었습니다!\n")
        else:
            print("\n⚠️ 퀴즈는 추가했지만 파일 저장에 실패했습니다. 종료 시 다시 저장을 시도합니다.\n")

    def list_quizzes(self):
        if not self.quizzes:
            print("📭 등록된 퀴즈가 없습니다.\n")
            return
        print(f"📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)\n")
        self._print_quiz_lines()
        print()

    def _print_quiz_lines(self):
        print(THIN_LINE)
        for number, quiz in enumerate(self.quizzes, start=1):
            mark = " 💡" if quiz.has_hint() else ""
            print(f"[{number}] {quiz.question}{mark}")
        print(THIN_LINE)

    def show_score(self):
        if self.best_score is None:
            print("📭 아직 퀴즈를 풀지 않았습니다. '퀴즈 풀기'로 첫 기록을 남겨 보세요!\n")
            return
        print(f"🏆 최고 점수: {self.best_score}점\n")

    def delete_quiz(self):
        if not self.quizzes:
            print("📭 삭제할 퀴즈가 없습니다.\n")
            return

        print("🗑️ 삭제할 퀴즈를 고르세요.\n")
        self._print_quiz_lines()
        number = read_int(f"삭제할 번호 (1-{len(self.quizzes)}, 취소는 0): ", 0, len(self.quizzes))
        if number == 0:
            print("삭제를 취소했습니다.\n")
            return

        target = self.quizzes[number - 1]
        if not read_yes_no(f"'{target.question}' 퀴즈를 삭제할까요? (y/n): "):
            print("삭제를 취소했습니다.\n")
            return

        self.quizzes.pop(number - 1)
        self.save_state()
        print(f"✅ 삭제했습니다. (남은 퀴즈 {len(self.quizzes)}개)\n")

    # ------------------------------------------------------------------
    # 파일 저장 / 불러오기
    def load_state(self):
        """state.json을 불러오고, 화면에 보여줄 안내 문구를 돌려준다."""
        try:
            data = self.store.load()
            if data is None:
                self._reset_to_default()
                self.save_state()
                return "📂 저장된 데이터가 없어 기본 퀴즈로 시작합니다."
            self._apply_state(data)
        except StateFileError as error:
            return self._recover(str(error), error.corrupted)
        except (ValueError, KeyError, TypeError) as error:
            return self._recover(f"데이터 구조 오류 - {error}", corrupted=True)

        best = "없음" if self.best_score is None else f"{self.best_score}점"
        return f"📂 저장된 데이터를 불러왔습니다. (퀴즈 {len(self.quizzes)}개, 최고점수 {best})"

    def _recover(self, reason, corrupted):
        """불러오기 실패 시 기본 데이터로 복구한다."""
        self._reset_to_default()
        if not corrupted:
            # 읽기 권한 문제 등: 원본을 덮어쓰지 않도록 이번 실행에서는 저장하지 않는다.
            return f"⚠️ 데이터 파일을 읽지 못했습니다. ({reason})\n   기본 퀴즈 데이터로 실행합니다."

        backup = self.store.backup_corrupted()
        self.save_state()
        lines = [f"⚠️ 데이터 파일이 손상되었습니다. ({reason})"]
        if backup:
            lines.append(f"   손상된 파일은 {backup.name} 으로 백업했습니다.")
        lines.append("   기본 퀴즈 데이터로 복구했습니다.")
        return "\n".join(lines)

    def _reset_to_default(self):
        self.quizzes = get_default_quizzes()
        self.best_score = None

    def _apply_state(self, data):
        """dict 형태의 상태를 검증해서 속성에 반영한다. 형식이 틀리면 ValueError."""
        raw_quizzes = data["quizzes"]
        if not isinstance(raw_quizzes, list):
            raise ValueError("quizzes는 목록이어야 합니다.")
        quizzes = [Quiz.from_dict(item) for item in raw_quizzes]

        best_score = data.get("best_score")
        if best_score is not None and not self._is_valid_score(best_score):
            raise ValueError("best_score는 0~100 사이 정수 또는 null이어야 합니다.")

        # 모든 검증을 통과한 뒤에 한 번에 반영 (중간에 실패하면 아무것도 바뀌지 않음)
        self.quizzes = quizzes
        self.best_score = best_score

    @staticmethod
    def _is_valid_score(value):
        return isinstance(value, int) and not isinstance(value, bool) and 0 <= value <= 100

    def _to_state(self):
        return {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
        }

    def save_state(self):
        """현재 상태를 파일에 저장한다. 성공하면 True."""
        try:
            self.store.save(self._to_state())
        except OSError as error:
            print(f"⚠️ 데이터 저장에 실패했습니다: {error}")
            return False
        return True
```