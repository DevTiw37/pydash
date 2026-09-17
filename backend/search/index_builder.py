import importlib
from models.search import SearchResult
from discovery.package_discovery import discover_modules
from discovery.module_discovery import discover_callables
from discovery.class_discovery import discover_methods
from discovery.object_loader import load_class
from search.endpoint_builder import (
    build_class_endpoint,
    build_function_endpoint,
    build_method_endpoint,
    build_module_endpoint,
)


def get_description(obj) -> str | None:
    from metadata.extractor import parse_docstring

    parsed = parse_docstring(obj)

    if parsed is None:
        return None

    for section in parsed.parsed:
        if type(section).__name__ == "DocstringSectionText":
            description = section.value.strip()

            if description:
                summary = description.split("\n\n")[0]
                return " ".join(summary.split())

    return None


def build_index(package_name: str) -> list[SearchResult]:
    modules = discover_modules(package_name)

    results = []

    for module in modules:
        module_object = importlib.import_module(module.name)
        results.append(
            SearchResult(
                name=module.name,
                qualified_name=module.name,
                kind=module.kind,
                module=module.name,
                endpoint=build_module_endpoint(module.name),
                description=get_description(module_object),
            )
            
        )

        callables = discover_callables(module.name)


        for callable_object in callables:
            actual_object = getattr(module_object, callable_object.name)
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
                    endpoint=(
                        build_class_endpoint(
                            module.name,
                            callable_object.name,
                        )
                        if callable_object.kind == "class"
                        else build_function_endpoint(
                            module.name,
                            callable_object.name,
                        )
                    ),
                    description=get_description(actual_object),
                )
                
            )

            if callable_object.kind == "class":
                class_object = load_class(
                    module.name,
                    callable_object.name,
                )

                methods = discover_methods(class_object)

                for method in methods:
                    method_object = getattr(class_object, method.name)
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
                            endpoint=build_method_endpoint(
                                module.name,
                                callable_object.name,
                                method.name,
                            ),
                            description=get_description(method_object),
                        )
                    )

    return results