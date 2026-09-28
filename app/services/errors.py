class ServiceError(Exception):
    """Foydalanuvchiga ko'rsatish mumkin bo'lgan xizmat xatosi."""

    def __init__(self, user_message: str) -> None:
        super().__init__(user_message)
        self.user_message = user_message
