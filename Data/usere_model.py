# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = user_e_model_from_dict(json.loads(json_string))

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
class UserEModelElement:
    nombre: str
    apellido: str
    correo: str
    contrasena: str
    region: str
    provincia: str
    municipio: str
    sector: str
    calle: str
    referencia: str
    tipodoc: str
    numeracion: str
    numerotel: str

    @staticmethod
    def from_dict(obj: Any) -> 'UserEModelElement':
        assert isinstance(obj, dict)
        nombre = from_str(obj.get("nombre"))
        apellido = from_str(obj.get("apellido"))
        correo = from_str(obj.get("correo"))
        contrasena = from_str(obj.get("contrasena"))
        region = from_str(obj.get("region"))
        provincia = from_str(obj.get("provincia"))
        municipio = from_str(obj.get("municipio"))
        sector = from_str(obj.get("sector"))
        calle = from_str(obj.get("calle"))
        referencia = from_str(obj.get("referencia"))
        tipodoc = from_str(obj.get("tipodoc"))
        numeracion = from_str(obj.get("numeracion"))
        numerotel = from_str(obj.get("numerotel"))
        return UserEModelElement(nombre, apellido, correo, contrasena, region, provincia, municipio, sector, calle, referencia, tipodoc, numeracion, numerotel)

    def to_dict(self) -> dict:
        result: dict = {}
        result["nombre"] = from_str(self.nombre)
        result["apellido"] = from_str(self.apellido)
        result["correo"] = from_str(self.correo)
        result["contrasena"] = from_str(self.contrasena)
        result["region"] = from_str(self.region)
        result["provincia"] = from_str(self.provincia)
        result["municipio"] = from_str(self.municipio)
        result["sector"] = from_str(self.sector)
        result["calle"] = from_str(self.calle)
        result["referencia"] = from_str(self.referencia)
        result["tipodoc"] = from_str(self.tipodoc)
        result["numeracion"] = from_str(self.numeracion)
        result["numerotel"] = from_str(self.numerotel)
        return result


def user_e_model_from_dict(s: Any) -> List[UserEModelElement]:
    return from_list(UserEModelElement.from_dict, s)


def user_e_model_to_dict(x: List[UserEModelElement]) -> Any:
    return from_list(lambda x: to_class(UserEModelElement, x), x)
