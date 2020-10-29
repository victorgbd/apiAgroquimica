# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = detallefact_model_from_dict(json.loads(json_string))

from dataclasses import dataclass
from typing import Any, List, TypeVar, Callable, Type, cast


T = TypeVar("T")


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class DetallefactModelElement:
    numfac: int
    codproducto: int
    cantvent: int
    precvent: float
    coduni: int

    @staticmethod
    def from_dict(obj: Any) -> 'DetallefactModelElement':
        assert isinstance(obj, dict)
        numfac = from_int(obj.get("numfac"))
        codproducto = from_int(obj.get("codproducto"))
        cantvent = from_int(obj.get("cantvent"))
        precvent = from_float(obj.get("precvent"))
        coduni = from_int(obj.get("coduni"))
        return DetallefactModelElement(numfac, codproducto, cantvent, precvent, coduni)

    def to_dict(self) -> dict:
        result: dict = {}
        result["numfac"] = from_int(self.numfac)
        result["codproducto"] = from_int(self.codproducto)
        result["cantvent"] = from_int(self.cantvent)
        result["precvent"] = to_float(self.precvent)
        result["coduni"] = from_int(self.coduni)
        return result


def detallefact_model_from_dict(s: Any) -> List[DetallefactModelElement]:
    return from_list(DetallefactModelElement.from_dict, s)


def detallefact_model_to_dict(x: List[DetallefactModelElement]) -> Any:
    return from_list(lambda x: to_class(DetallefactModelElement, x), x)
