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
class HistorialdispModelElement:
    codusu: str
    fecha_ses: str
    coddisp: str
    latitud: str
    longitud: str

    @staticmethod
    def from_dict(obj: Any) -> 'HistorialdispModelElement':
        assert isinstance(obj, dict)
        codusu = from_str(obj.get("codusu"))
        fecha_ses = from_str(obj.get("fecha_ses"))
        coddisp = from_str(obj.get("coddisp"))
        latitud = from_str(obj.get("latitud"))
        longitud = from_str(obj.get("longitud"))
        return HistorialdispModelElement(codusu, fecha_ses, coddisp, latitud, longitud)

    def to_dict(self) -> dict:
        result: dict = {}
        result["codusu"] = from_str(self.codusu)
        result["fecha_ses"] = from_str(self.fecha_ses)
        result["coddisp"] = from_str(self.coddisp)
        result["latitud"] = from_str(self.latitud)
        result["longitud"] = from_str(self.longitud)
        return result


def historialdisp_model_from_dict(s: Any) -> List[HistorialdispModelElement]:
    return from_list(HistorialdispModelElement.from_dict, s)


def historialdisp_model_to_dict(x: List[HistorialdispModelElement]) -> Any:
    return from_list(lambda x: to_class(HistorialdispModelElement, x), x)
