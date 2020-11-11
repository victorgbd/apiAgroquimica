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
class ProductosModelElement:
    codproducto: str
    descripcion: str
    codunidad: str
    unidad: str
    cantidad: str
    precio: str
    tipoprod: str
    destipoprod: str
    url: str

    @staticmethod
    def from_dict(obj: Any) -> 'ProductosModelElement':
        assert isinstance(obj, dict)
        codproducto = from_str(obj.get("codproducto"))
        descripcion = from_str(obj.get("descripcion"))
        codunidad = from_str(obj.get("codunidad"))
        unidad = from_str(obj.get("unidad"))
        cantidad = from_str(obj.get("cantidad"))
        precio = from_str(obj.get("precio"))
        tipoprod = from_str(obj.get("tipoprod"))
        destipoprod = from_str(obj.get("destipoprod"))
        url = from_str(obj.get("url"))
        return ProductosModelElement(codproducto, descripcion, codunidad, unidad, cantidad, precio, tipoprod, destipoprod, url)

    def to_dict(self) -> dict:
        result: dict = {}
        result["codproducto"] = from_str(self.codproducto)
        result["descripcion"] = from_str(self.descripcion)
        result["codunidad"] = from_str(self.codunidad)
        result["unidad"] = from_str(self.unidad)
        result["cantidad"] = from_str(self.cantidad)
        result["precio"] = from_str(self.precio)
        result["tipoprod"] = from_str(self.tipoprod)
        result["destipoprod"] = from_str(self.destipoprod)
        result["url"] = from_str(self.url)
        return result


def productos_model_from_dict(s: Any) -> List[ProductosModelElement]:
    return from_list(ProductosModelElement.from_dict, s)


def productos_model_to_dict(x: List[ProductosModelElement]) -> Any:
    return from_list(lambda x: to_class(ProductosModelElement, x), x)
