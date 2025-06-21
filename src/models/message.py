class Message:
    def __init__(self, content: str, sender: str):
        self.content = content
        self.sender = sender

    def format_message(self) -> str:
        return f"{self.sender}: {self.content}"