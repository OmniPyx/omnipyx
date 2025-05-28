from importlib.metadata import entry_points


def discover_omnipyx_modules():
    modules = []
    try:
        eps = entry_points()
        print(eps.select(group='omnipyx.modules'))
        for entry_point in eps.select(group='omnipyx.modules'):
            module = entry_point.load()
            modules.append(f"{module.__module__}.{module.__name__}")
    except Exception as e:
        print(f"Error loading module: {e}")
    return modules
