import importlib
import pkgutil

def load_package(package):
    for _, name, _ in pkgutil.iter_modules(package.__path__):
        importlib.import_module(f"{package.__name__}.{name}")
