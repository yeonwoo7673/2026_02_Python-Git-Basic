```python 
"""개별 퀴즈 한 문제를 표현하는 Quiz 클래스."""


class Quiz:
    """문제, 선택지 4개, 정답 번호(1~4)를 가진 퀴즈."""

    CHOICE_COUNT = 4

    def __init__(self, question, choices, answer):
        if not isinstance(question, str) or not question.strip():
            raise ValueError("문제가 비어 있습니다.")
        if (
            not isinstance(choices, list)
            or len(choices) != self.CHOICE_COUNT
            or not all(isinstance(c, str) and c.strip() for c in choices)
        ):
            raise ValueError(f"선택지는 비어 있지 않은 문자열 {self.CHOICE_COUNT}개여야 합니다.")
        # bool은 int의 하위 타입이라 True가 1로 통과하지 않도록 따로 막는다.
        if isinstance(answer, bool) or not isinstance(answer, int):
            raise ValueError("정답은 정수여야 합니다.")
        if not 1 <= answer <= self.CHOICE_COUNT:
            raise ValueError(f"정답은 1~{self.CHOICE_COUNT} 사이여야 합니다.")

        self.question = question.strip()
        self.choices = [c.strip() for c in choices]
        self.answer = answer

    @property
    def answer_text(self):
        """정답 번호에 해당하는 선택지 내용."""
        return self.choices[self.answer - 1]

    def display(self, number):
        """문제와 선택지를 화면에 출력한다."""
        print(f"[문제 {number}]")
        print(self.question)
        print()
        for index, choice in enumerate(self.choices, start=1):
            print(f"{index}. {choice}")
        print()

    def is_correct(self, user_answer):
        return user_answer == self.answer

    def to_dict(self):
        """state.json에 저장할 수 있는 dict로 변환한다."""
        return {
            "question": self.question,
            "choices": list(self.choices),
            "answer": self.answer,
        }

    @classmethod
    def from_dict(cls, data):
        """state.json에서 읽은 dict로 Quiz를 만든다. 형식이 틀리면 ValueError."""
        if not isinstance(data, dict):
            raise ValueError("퀴즈 데이터가 객체 형식이 아닙니다.")
        try:
            return cls(data["question"], data["choices"], data["answer"])
        except KeyError as error:
            raise ValueError(f"퀴즈 데이터에 '{error.args[0]}' 항목이 없습니다.") from error
```
