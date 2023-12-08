import json
from pydantic import BaseModel


class CustomBaseModel(BaseModel):
    """
    Модель используется для наследования во всех последующих моделях вместо BaseModel.
    Переопределяется метод model_dump_json, в котором происходит кодирование в utf-8,
    чтобы можно было передавать в json в теле запроса текст на кириллице
    """

    def model_dump_json(self, *args, **kwargs):
        return json.dumps(self.model_dump(by_alias=True)).encode("utf-8")


class Auth(CustomBaseModel):
    """Авторизация с логином и паролем, используется в фикстурах"""

    login: str
    password: str


class Token(CustomBaseModel):
    """Токен, который получается в результате авторизации и прокидывается в header во всех последующих запросах"""

    token: str
    type: str
