from typing import TypedDict


class CaptchaState(TypedDict):
    user_id: int
    captcha_code: int
