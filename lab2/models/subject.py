class Subject:
    """Class representing an academic subject or course."""

    def __init__(self, subject_id: str, name: str, credits: int):
        self.subject_id = subject_id
        self.name = name
        self.credits = credits  # количество зачетных единиц (кредитов)