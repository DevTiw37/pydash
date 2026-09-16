import importlib
import pkgutil

from models.schemas import DiscoveredObject

def discover_modules(package_name: str) -> list[DiscoveredObject]:
    package = importlib.import_module(package_name)

    if not hasattr(package, "__path__"):
        raise TypeError(f"'{package_name}' is not a package")

    results = [
        DiscoveredObject(
            name=package_name,
            kind="module",
        )
    ]

    for module_info in pkgutil.walk_packages(
        package.__path__,
        prefix=f"{package_name}.",
    ):
        module_name = module_info.name

        if any(
            part.startswith("_")
            for part in module_name.split(".")
        ):
            continue

        results.append(
            DiscoveredObject(
                name=module_name,
                kind="module",
            )
        )

    results.sort(key=lambda item: item.name)

    return results

if __name__ == "__main__":
    result = discover_modules("email")
    print(result)