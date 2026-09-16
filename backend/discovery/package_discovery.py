import importlib
import pkgutil

from models.schemas import DiscoveredObject


def discover_modules(package_name: str):
    package = importlib.import_module(package_name)

    if not hasattr(package, "__path__"):
        raise TypeError(
            f"'{package_name}' is not a package"
        )

    modules: list[DiscoveredObject] = []

    for module_info in pkgutil.walk_packages(
        package.__path__,
        package.__name__ + ".",
    ):
        module_name = module_info.name

        if any(
            part.startswith("_")
            for part in module_name.split(".")
        ):
            continue

        modules.append(
            DiscoveredObject(
                name=module_name,
                kind="module",
            )
        )

    modules.sort(key=lambda item: item.name)

    return modules


if __name__ == "__main__":
    result = discover_modules("email")
    print(result)