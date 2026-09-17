import importlib
import inspect

from models.schemas import DiscoveredObject
from models.search import SearchKind

def discover_callables(
    module_name: str,
) -> list[DiscoveredObject]:
    module = importlib.import_module(module_name)

    callables: list[DiscoveredObject] = []

    for name in dir(module):
        if name.startswith("_"):
            continue

        attribute = getattr(module, name)

        if inspect.isclass(attribute):
            if getattr(attribute, "__module__", None) != module_name:
                continue

            callables.append(
                DiscoveredObject(
                    name=name,
                    kind=SearchKind.CLASS,
                )
            )

        elif inspect.isfunction(attribute) or inspect.isbuiltin(attribute):
            if getattr(attribute, "__module__", None) != module_name:
                continue

            callables.append(
                DiscoveredObject(
                    name=name,
                    kind=SearchKind.FUNCTION,
                )
            )

    callables.sort(key=lambda item: item.name)

    return callables


if __name__ == "__main__":
    result = discover_callables("math")

    print(result)