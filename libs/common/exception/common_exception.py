class CommonException(Exception):
    def __init__(self, code: int, msg: str):
        super().__init__(msg)
        self.code = code
        self.msg = msg
