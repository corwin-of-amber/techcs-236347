from dataclasses import dataclass

from lark import Transformer, v_args, UnexpectedInput

from syntax.utils import make_node, ParseError, _read_grammar


type LambdaExpr = Id | Int | Let | Lambda | App


@dataclass(frozen=True, slots=True)
class Id:
    name: str


@dataclass(frozen=True, slots=True)
class Int:
    n: int


@dataclass(frozen=True, slots=True)
class Let:
    decl: Id
    defn: LambdaExpr
    body: LambdaExpr


@dataclass(frozen=True, slots=True)
class Lambda:
    var: Id
    body: LambdaExpr


@dataclass(frozen=True, slots=True)
class App:
    func: LambdaExpr
    arg: LambdaExpr


@v_args(inline=True)
class NodeFactory(Transformer):
    def var(self, name):
        return make_node(Id, name.value)

    def decl(self, name):
        return make_node(Id, name.value)

    def num(self, value):
        return make_node(Int, int(value.value))

    def let(self, decl, defn, body):
        return make_node(Let, decl, defn, body)

    def abs(self, *args):
        *params, body = args
        for param in reversed(params):
            body = make_node(Lambda, param, body)
        return body

    def app(self, func, arg):
        return make_node(App, func, arg)


_factory = NodeFactory()


def parse(program_text: str) -> LambdaExpr:
    """Parses a lambda calculus program and returns the corresponding expression."""
    parser = _read_grammar("lambda_pure.lark", _factory)
    try:
        return parser.parse(program_text)
    except UnexpectedInput as e:
        raise ParseError() from e


def pretty(expr: LambdaExpr) -> str:
    """Formats an expression for pretty printing."""
    match expr:
        case Id(n):
            return n
        case Int(num):
            return str(num)
        case Let(var, defn, body):
            return f"let {var.name} = {pretty(defn)} in {pretty(body)}"
        case Lambda(var, body):
            return f"\\{var.name}. {pretty(body)}"
        case App(func, arg):
            return f"({pretty(func)} {pretty(arg)})"
        case _:
            raise ValueError(f"Unknown expression type: {type(expr)}")
