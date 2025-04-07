from functools import lru_cache
from lark import Lark, Transformer
from importlib_resources import files


class ParseError(Exception):
    pass


@lru_cache(maxsize=None)
def make_node[T](cls: type[T], *args, **kwargs) -> T:
    """Maintains a pool of allocated object, so equality tests are fast.
    cls(*args, **kwargs) must be recursively-immutable for correctness."""
    assert cls.__dataclass_params__.frozen
    return cls(*args, **kwargs)


@lru_cache(maxsize=None)
def _read_grammar(filename: str, factory: Transformer, start="start") -> Lark:
    """Reads the grammar from the file."""

    grammar = files("syntax").joinpath(filename).read_text()
    return Lark(grammar, parser="lalr", transformer=factory, start=start)


# Install a pretty printer for the given classes
def _install_str_hook(*classes):
    def decorator(pretty_func):
        for cls in classes:
            cls.__str__ = pretty_func
        return pretty_func

    return decorator
