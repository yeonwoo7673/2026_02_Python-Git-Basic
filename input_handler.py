<<<<<<< HEAD
```python
=======
>>>>>>> 7d7a35a35fba8f19133b8dece098e4bda9036e37
"""사용자 입력을 받고 검증하는 함수 모음.

공통 입력 기준:
- 앞뒤 공백은 제거한다.
- 빈 입력, 숫자가 아닌 입력, 범위 밖 숫자는 안내 후 다시 입력받는다.
- Ctrl+C(KeyboardInterrupt), 입력 끝(EOFError)은 여기서 잡지 않고
  main.py까지 올려 보내 저장 후 안전하게 종료한다.
"""


def read_line(prompt):
    """한 줄을 입력받아 앞뒤 공백을 제거해 돌려준다."""
    return input(prompt).strip()


def parse_int(text, min_value, max_value):
    """문자열을 범위 안의 정수로 바꾼다.

    성공하면 (정수, None), 실패하면 (None, 안내 메시지)를 돌려준다.
    """
    range_guide = f"{min_value}-{max_value} 사이의 숫자를 입력하세요."
    if text == "":
        return None, f"입력이 비어 있습니다. {range_guide}"
    try:
        value = int(text)
    except ValueError:
        return None, f"잘못된 입력입니다. {range_guide}"
    if not min_value <= value <= max_value:
        return None, f"잘못된 입력입니다. {range_guide}"
    return value, None


def read_int(prompt, min_value, max_value):
    """올바른 범위의 정수가 들어올 때까지 반복해서 입력받는다."""
    while True:
        value, error = parse_int(read_line(prompt), min_value, max_value)
        if error is None:
            return value
        print(f"⚠️ {error}")


def read_text(prompt):
    """비어 있지 않은 문자열이 들어올 때까지 반복해서 입력받는다."""
    while True:
        text = read_line(prompt)
        if text:
            return text
        print("⚠️ 입력이 비어 있습니다. 내용을 입력하세요.")


def read_yes_no(prompt):
    """y/n 질문. y면 True, n이면 False."""
    while True:
        text = read_line(prompt).lower()
        if text in ("y", "yes", "예", "네"):
            return True
        if text in ("n", "no", "아니오", "아니요"):
            return False
        print("⚠️ y 또는 n을 입력하세요.")
<<<<<<< HEAD

```
=======
>>>>>>> 7d7a35a35fba8f19133b8dece098e4bda9036e37
