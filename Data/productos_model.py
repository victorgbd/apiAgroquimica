# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = productos_model_from_dict(json.loads(json_string))

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
class Unidad:
    
    coduni: int
    desunidad: str
    precio: str
    cantidad: int

    @staticmethod
    def from_dict(obj: Any) -> 'Unidad':
        assert isinstance(obj, dict)
        desunidad = from_str(obj.get("desunidad"))
        coduni = int(from_str(obj.get("coduni")))
        cantidad = int(from_str(obj.get("cantidad")))
        precio = from_str(obj.get("precio"))
        return Unidad(desunidad, coduni, cantidad, precio)

    def to_dict(self) -> dict:
        result: dict = {}
        result["desunidad"] = from_str(self.desunidad)
        result["coduni"] = from_str(str(self.coduni))
        result["cantidad"] = from_str(str(self.cantidad))
        result["precio"] = from_str(self.precio)
        return result


@dataclass
class ProductosModelElement:
    codproducto: int
    descripcion: str
    tipoprod: int
    destipoprod: str
    url: str
    unidad: List[Unidad]
    codunidad: int

    @staticmethod
    def from_dict(obj: Any) -> 'ProductosModelElement':
        assert isinstance(obj, dict)
        codproducto = int(from_str(obj.get("codproducto")))
        descripcion = from_str(obj.get("descripcion"))
        codunidad = int(from_str(obj.get("codunidad")))
        unidad = from_list(Unidad.from_dict, obj.get("unidad"))
        tipoprod = int(from_str(obj.get("tipoprod")))
        destipoprod = from_str(obj.get("destipoprod"))
        url = from_str(obj.get("url"))
        return ProductosModelElement(codproducto, descripcion, codunidad, unidad, tipoprod, destipoprod, url)

    def to_dict(self) -> dict:
        result: dict = {}
        result["codproducto"] = from_str(str(self.codproducto))
        result["descripcion"] = from_str(self.descripcion)
        result["codunidad"] = from_str(str(self.codunidad))
        result["unidad"] = from_list(lambda x: to_class(Unidad, x), self.unidad)
        result["tipoprod"] = from_str(str(self.tipoprod))
        result["destipoprod"] = from_str(self.destipoprod)
        result["url"] = from_str(self.url)
        return result


def productos_model_from_dict(s: Any) -> List[ProductosModelElement]:
    return from_list(ProductosModelElement.from_dict, s)


def productos_model_to_dict(x: List[ProductosModelElement]) -> Any:
    return from_list(lambda x: to_class(ProductosModelElement, x), x)
