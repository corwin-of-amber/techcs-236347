import copy
import weakref


class Path(list):
    @property
    def start(self):
        return self.node_at(0)

    @property
    def end(self):
        return self.node_at(-1)

    def __init__(self, list_of_tree_nodes=()):
        super().__init__(map(weakref.ref, list_of_tree_nodes))

    def node_at(self, i):
        return self[i]()

    def __add__(self, cont):
        plus = copy.copy(self)
        plus += cont
        return plus

    def __iadd__(self, cont):
        if not isinstance(cont, Path):
            cont = Path(cont)
        return super(Path, self).__iadd__(cont)

    def __getitem__(self, k: int | slice) -> "Path":
        p = Path()
        p.extend(super()[k])
        return p

    def up(self):
        return self[:-1]

    def startswith(self, other_path: "Path") -> bool:
        if len(other_path) > len(self):
            return False
        for i in range(len(other_path)):
            if self.node_at(i) is not other_path.node_at(i):
                return False
        return True

    def __eq__(self, other):
        if isinstance(other, Path):
            return len(self) == len(other) and self.startswith(other)
        else:
            return NotImplemented

    def __repr__(self):
        return " -> ".join(repr(x()) for x in self)
