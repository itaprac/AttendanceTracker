class Course:
    """
    A class to represent a course.
    """

    def __init__(self, name: str, format: str, un_classes=0) -> None:
        """
        Constructs all the necessary attributes for the course object.
        """
        self._name = name
        self._un_classes = max(0, min(un_classes, 3))
        self._format = format

    @property
    def name(self) -> str:
        """Gets the name of the course."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """Sets the name of the course."""
        self._name = value

    @property
    def un_classes(self) -> int:
        """Gets the number of unattended classes."""
        return self._un_classes

    @un_classes.setter
    def un_classes(self, value: int) -> None:
        """Sets the number of unattended classes, constrained between 0 and 3."""
        self._un_classes = max(0, min(value, 3))

    @property
    def format(self) -> str:
        """Gets the format of the course."""
        return self._format

    @format.setter
    def format(self, value: str) -> None:
        """Sets the format of the course."""
        self._format = value

    def __str__(self) -> str:
        """Returns a string representation of the course."""
        return f"Course: {self.name}, Format: {self.format}, Unattended Classes: {self.un_classes}"

    def increment_un_classes(self, amount=1) -> None:
        """
        Increments the number of unattended classes by a specified amount.
        """
        if amount < 0:
            raise ValueError("Cannot increment by negative values")
        self.un_classes = min(self.un_classes + amount, 3)

    def decrement_un_classes(self, amount=1) -> None:
        """
        Decrements the number of unattended classes by a specified amount.
        """
        if amount < 0:
            raise ValueError("Cannot decrement by negative values")
        self.un_classes = max(self.un_classes - amount, 0)
