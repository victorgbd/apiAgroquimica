# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = user_model_from_dict(json.loads(json_string))

from dataclasses import dataclass
from typing import Any, List, TypeVar, Callable, Type, cast


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class UserModelElement:
    nickname: str
    contrasena: str
    tipoacceso: int
    codusuario: int

    @staticmethod
    def from_dict(obj: Any) -> 'UserModelElement':
        assert isinstance(obj, dict)
        nickname = from_str(obj.get("nickname"))
        contrasena = from_str(obj.get("contrasena"))
        tipoacceso = int(from_str(obj.get("tipoacceso")))
        codusuario = int(from_str(obj.get("codusuario")))
        return UserModelElement(nickname, contrasena, tipoacceso, codusuario)

    def to_dict(self) -> dict:
        result: dict = {}
        result["nickname"] = from_str(self.nickname)
        result["contrasena"] = from_str(self.contrasena)
        result["tipoacceso"] = from_str(str(self.tipoacceso))
        result["codusuario"] = from_str(str(self.codusuario))
        return result


def user_model_from_dict(s: Any) -> List[UserModelElement]:
    return from_list(UserModelElement.from_dict, s)


def user_model_to_dict(x: List[UserModelElement]) -> Any:
    return from_list(lambda x: to_class(UserModelElement, x), x)
