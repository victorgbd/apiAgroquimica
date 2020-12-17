# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = dispositivo_model_from_dict(json.loads(json_string))

from dataclasses import dataclass
from typing import Any, List, TypeVar, Callable, Type, cast


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_stringified_bool(x: str) -> bool:
    if x == "true":
        return True
    if x == "false":
        return False
    assert False


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class DispositivoModelElement:
    coddisp: str
    descripcion: str
    imei: str
    codusu: str
    estado: bool

    @staticmethod
    def from_dict(obj: Any) -> 'DispositivoModelElement':
        assert isinstance(obj, dict)
        coddisp = from_str(obj.get("coddisp"))
        descripcion = from_str(obj.get("descripcion"))
        imei = from_str(obj.get("imei"))
        codusu = from_str(obj.get("codusu"))
        estado = from_stringified_bool(from_str(obj.get("estado")))
        return DispositivoModelElement(coddisp, descripcion, imei, codusu, estado)

    def to_dict(self) -> dict:
        result: dict = {}
        result["coddisp"] = from_str(self.coddisp)
        result["descripcion"] = from_str(self.descripcion)
        result["imei"] = from_str(self.imei)
        result["codusu"] = from_str(self.codusu)
        result["estado"] = from_str(str(self.estado).lower())
        return result


def dispositivo_model_from_dict(s: Any) -> List[DispositivoModelElement]:
    return from_list(DispositivoModelElement.from_dict, s)


def dispositivo_model_to_dict(x: List[DispositivoModelElement]) -> Any:
    return from_list(lambda x: to_class(DispositivoModelElement, x), x)
