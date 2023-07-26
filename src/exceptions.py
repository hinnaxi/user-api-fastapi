import http
from typing import Sequence, Any, Optional


class ApiException(Exception):
    def __init__(self, status_code: int, msg: str, code: Optional[str] = None, errors: Sequence[Any] = None):
        if code is None:
            code = http.HTTPStatus(status_code).phrase
        self.status_code = status_code
        self.code = code
        self.message = msg
        self._errors = errors

    def errors(self) -> Sequence[Any]:
        return self._errors
