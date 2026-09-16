from models.search import SearchResult
from discovery.package_discovery import discover_modules
from discovery.module_discovery import discover_callables
from discovery.class_discovery import discover_methods
from discovery.object_loader import load_class


def build_index(package_name: str) -> list[SearchResult]:
    modules = discover_modules(package_name)

    results = []

    for module in modules:
        results.append(

            SearchResult(
                name=module.name,
                qualified_name=module.name,
                kind=module.kind,
                module=module.name,
            )
            
        )

        callables = discover_callables(module.name)


        for callable_object in callables:
            results.append(
                SearchResult(
                    name=callable_object.name,
                    qualified_name=f"{module.name}.{callable_object.name}",
                    kind=callable_object.kind,
                    module=module.name,
                    class_name=(
                        callable_object.name
                        if callable_object.kind == "class"
                        else None
                    ),
                )
                
            )

            if callable_object.kind == "class":
                class_object = load_class(
                    module.name,
                    callable_object.name,
                )

                methods = discover_methods(class_object)

                for method in methods:
                    results.append(
                        SearchResult(
                            name=method.name,
                            qualified_name=(
                                f"{module.name}."
                                f"{callable_object.name}."
                                f"{method.name}"
                            ),
                            kind=method.kind,
                            module=module.name,
                            class_name=callable_object.name,
                        )
                    )

    return results