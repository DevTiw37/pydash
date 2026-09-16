from discovery.package_discovery import discover_modules


def get_package_metadata(package: str):
    modules = discover_modules(package)

    return {
        "package": package,
        "modules": modules,
    }