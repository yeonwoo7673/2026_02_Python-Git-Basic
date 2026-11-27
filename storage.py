```python
"""state.json 파일 읽기/쓰기를 담당하는 StateStore 클래스."""

```bash
- 언제 저장하고 실패하면 어떻게 복구할지는 QuizGame 담당
- 파일 없음 → 기본 퀴즈로 시작하고 새로 저장
- 파일 손상 → 안내 후 `state.corrupted-날짜시간.json`으로 백업하고 기본 데이터로 복구
- 저장은 임시 파일에 먼저 쓰고 교체 → 저장 중 끊겨도 기존 파일이 깨지지 않음
- 퀴즈 추가 직후, 게임 종료 직후, 프로그램 종료 시, Ctrl+C 시 저장
```

import json
import os
from datetime import datetime
from pathlib import Path


class StateFileError(Exception):
    """state.json을 읽지 못했을 때 발생하는 예외.

    corrupted=True  : 파일 내용이 손상됨 (JSON 문법 오류, 구조 오류 등)
    corrupted=False : 파일은 멀쩡할 수 있지만 읽기 자체가 실패함 (권한 등)
    """

    def __init__(self, message, corrupted=True):
        super().__init__(message)
        self.corrupted = corrupted


class StateStore:
    """JSON 파일 하나에 게임 상태를 저장하고 불러온다."""

    def __init__(self, path):
        self.path = Path(path)

    def load(self):
        """파일을 읽어 dict로 돌려준다. 파일이 없으면 None."""
        if not self.path.exists():
            return None
        try:
            with self.path.open("r", encoding="utf-8") as file:
                data = json.load(file)
        except json.JSONDecodeError as error:
            raise StateFileError(f"JSON 형식 오류 ({error.lineno}행 {error.colno}열)") from error
        except UnicodeDecodeError as error:
            raise StateFileError("UTF-8로 읽을 수 없는 파일입니다.") from error
        except OSError as error:
            raise StateFileError(f"파일을 읽을 수 없습니다: {error}", corrupted=False) from error

        if not isinstance(data, dict):
            raise StateFileError("최상위 구조가 객체({ ... })가 아닙니다.")
        return data

    def save(self, data):
        """dict를 UTF-8 JSON으로 저장한다. 실패하면 OSError가 발생한다.

        임시 파일에 먼저 쓴 뒤 교체하므로, 저장 도중 문제가 생겨도
        기존 state.json이 반쯤 쓰인 상태로 망가지지 않는다.
        """
        temp_path = self.path.with_name(self.path.name + ".tmp")
        with temp_path.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        os.replace(temp_path, self.path)

    def backup_corrupted(self):
        """손상된 파일을 다른 이름으로 옮겨 둔다. 성공하면 백업 경로, 실패하면 None."""
        if not self.path.exists():
            return None
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup_path = self.path.with_name(f"{self.path.stem}.corrupted-{stamp}.json")
        counter = 1
        while backup_path.exists():  # 같은 초에 여러 번 백업해도 덮어쓰지 않도록
            backup_path = self.path.with_name(f"{self.path.stem}.corrupted-{stamp}-{counter}.json")
            counter += 1
        try:
            os.replace(self.path, backup_path)
        except OSError:
            return None
        return backup_path

```