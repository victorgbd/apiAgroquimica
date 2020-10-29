# This code parses date/times, so please
#
#     pip install python-dateutil
#
# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = factura_model_from_dict(json.loads(json_string))

from dataclasses import dataclass
from datetime import datetime
from typing import Any, List, TypeVar, Callable, Type, cast
import dateutil.parser


T = TypeVar("T")


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_stringified_bool(x: str) -> bool:
    if x == "true":
        return True
    if x == "false":
        return False
    assert False


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


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
class FacturaModelElement:
    numfact: int
    codcli: int
    estado: int
    tipfac: bool
    fecha: datetime
    codemp: int
    balance: float
    total: float

    @staticmethod
    def from_dict(obj: Any) -> 'FacturaModelElement':
        assert isinstance(obj, dict)
        numfact = from_int(obj.get("numfact"))
        codcli = from_int(obj.get("codcli"))
        estado = from_int(obj.get("estado"))
        tipfac = from_stringified_bool(from_str(obj.get("tipfac")))
        fecha = from_datetime(obj.get("fecha"))
        codemp = from_int(obj.get("codemp"))
        balance = from_float(obj.get("balance"))
        total = from_float(obj.get("total"))
        return FacturaModelElement(numfact, codcli, estado, tipfac, fecha, codemp, balance, total)

    def to_dict(self) -> dict:
        result: dict = {}
        result["numfact"] = from_int(self.numfact)
        result["codcli"] = from_int(self.codcli)
        result["estado"] = from_int(self.estado)
        result["tipfac"] = from_str(str(self.tipfac).lower())
        result["fecha"] = self.fecha.isoformat()
        result["codemp"] = from_int(self.codemp)
        result["balance"] = to_float(self.balance)
        result["total"] = to_float(self.total)
        return result


def factura_model_from_dict(s: Any) -> List[FacturaModelElement]:
    return from_list(FacturaModelElement.from_dict, s)


def factura_model_to_dict(x: List[FacturaModelElement]) -> Any:
    return from_list(lambda x: to_class(FacturaModelElement, x), x)
