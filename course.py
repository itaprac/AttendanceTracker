class Course:
    def __init__(self, name: str, format: str, un_classes: int = 0) -> None:
        self._name = name
        self._un_classes = max(0, min(un_classes, 3))
        self._format = format

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def un_classes(self) -> int:
        return self._un_classes

    @un_classes.setter
    def un_classes(self, value: int) -> None:
        self._un_classes = max(0, min(value, 3))

    @property
    def format(self) -> str:
        return self._format

    @format.setter
    def format(self, value: str) -> None:
        self._format = value

    def __str__(self) -> str:
        return f"Course: {self.name}, Format: {self.format}, Unattended Classes: {self.un_classes}"

    def __eq__(self, other) -> bool:
        return self.name == other.name and self.format == other.format

    def increment_un_classes(self, amount: int = 1) -> None:
        if amount < 0:
            raise ValueError("Cannot increment by negative values")
        self.un_classes = min(self.un_classes + amount, 3)

    def decrement_un_classes(self, amount: int = 1) -> None:
        if amount < 0:
            raise ValueError("Cannot decrement by negative values")
        self.un_classes = max(self.un_classes - amount, 0)
