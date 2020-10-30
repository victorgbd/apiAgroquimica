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
    pais: str
    ciudad: str
    coddir: str
    direccion: str
    tipo: str
    numeracion: str
    numerotelf: str

    @staticmethod
    def from_dict(obj: Any) -> 'UserEModelElement':
        assert isinstance(obj, dict)
        nombre = from_str(obj.get("nombre"))
        apellido = from_str(obj.get("apellido"))
        correo = from_str(obj.get("correo"))
        contrasena = from_str(obj.get("contrasena"))
        pais = from_str(obj.get("pais"))
        ciudad = from_str(obj.get("ciudad"))
        coddir = from_str(obj.get("coddir"))
        direccion = from_str(obj.get("direccion"))
        tipo = from_str(obj.get("tipo"))
        numeracion = from_str(obj.get("numeracion"))
        numerotelf = from_str(obj.get("numerotelf"))
        return UserEModelElement(nombre, apellido, correo, contrasena, pais, ciudad, coddir, direccion, tipo, numeracion, numerotelf)

    def to_dict(self) -> dict:
        result: dict = {}
        result["nombre"] = from_str(self.nombre)
        result["apellido"] = from_str(self.apellido)
        result["correo"] = from_str(self.correo)
        result["contrasena"] = from_str(self.contrasena)
        result["pais"] = from_str(self.pais)
        result["ciudad"] = from_str(self.ciudad)
        result["coddir"] = from_str(self.coddir)
        result["direccion"] = from_str(self.direccion)
        result["tipo"] = from_str(self.tipo)
        result["numeracion"] = from_str(self.numeracion)
        result["numerotelf"] = from_str(self.numerotelf)
        return result


def user_e_model_from_dict(s: Any) -> List[UserEModelElement]:
    return from_list(UserEModelElement.from_dict, s)


def user_e_model_to_dict(x: List[UserEModelElement]) -> Any:
    return from_list(lambda x: to_class(UserEModelElement, x), x)
