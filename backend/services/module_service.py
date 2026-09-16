from discovery.module_discovery import discover_callables


def get_module_metadata(module: str):
    callables = discover_callables(module)

    return {
        "module": module,
        "callables": callables,
    }