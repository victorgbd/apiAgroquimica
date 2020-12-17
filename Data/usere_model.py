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
    codcli: int
    correo: str
    contrasena: int
    codpais: int
    pais: str
    codciudad: int
    ciudad: str
    coddir: int
    direccion: str
    tipo: str
    numeracion: str
    numerotelf: str
    codusu: int

    @staticmethod
    def from_dict(obj: Any) -> 'UserEModelElement':
        assert isinstance(obj, dict)
        nombre = from_str(obj.get("nombre"))
        apellido = from_str(obj.get("apellido"))
        codcli = int(from_str(obj.get("codcli")))
        correo = from_str(obj.get("correo"))
        contrasena = int(from_str(obj.get("contrasena")))
        codpais = int(from_str(obj.get("codpais")))
        pais = from_str(obj.get("pais"))
        codciudad = int(from_str(obj.get("codciudad")))
        ciudad = from_str(obj.get("ciudad"))
        coddir = int(from_str(obj.get("coddir")))
        direccion = from_str(obj.get("direccion"))
        tipo = from_str(obj.get("tipo"))
        numeracion = from_str(obj.get("numeracion"))
        numerotelf = from_str(obj.get("numerotelf"))
        codusu = int(from_str(obj.get("codusu")))
        return UserEModelElement(nombre, apellido, codcli, correo, contrasena, codpais, pais, codciudad, ciudad, coddir, direccion, tipo, numeracion, numerotelf, codusu)

    def to_dict(self) -> dict:
        result: dict = {}
        result["nombre"] = from_str(self.nombre)
        result["apellido"] = from_str(self.apellido)
        result["codcli"] = from_str(str(self.codcli))
        result["correo"] = from_str(self.correo)
        result["contrasena"] = from_str(str(self.contrasena))
        result["codpais"] = from_str(str(self.codpais))
        result["pais"] = from_str(self.pais)
        result["codciudad"] = from_str(str(self.codciudad))
        result["ciudad"] = from_str(self.ciudad)
        result["coddir"] = from_str(str(self.coddir))
        result["direccion"] = from_str(self.direccion)
        result["tipo"] = from_str(self.tipo)
        result["numeracion"] = from_str(self.numeracion)
        result["numerotelf"] = from_str(self.numerotelf)
        result["codusu"] = from_str(str(self.codusu))
        return result


def user_e_model_from_dict(s: Any) -> List[UserEModelElement]:
    return from_list(UserEModelElement.from_dict, s)


def user_e_model_to_dict(x: List[UserEModelElement]) -> Any:
    return from_list(lambda x: to_class(UserEModelElement, x), x)
