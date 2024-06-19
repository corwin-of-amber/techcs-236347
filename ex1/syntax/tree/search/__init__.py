from syntax.tree.paths import Path
from syntax.tree.walk import RichTreeWalk


class ScanFor:

    class Visitor(RichTreeWalk.Visitor):
        def __init__(self, criterion, applies_to):
            self.criterion = criterion
            self.applies_to = applies_to
            self.path = Path()
            self.collect = []

        def enter(self, node, prune):
            self.path = self.path + [node]
            if self.criterion(self.applies_to(self.path)):
                self.collect.append(self.path)

        def leave(self, node):
            self.path = self.path.up()

        def done(self, root, final):
            return self.collect

    PATH = lambda path: path
    NODE = lambda path: path.end
    VALUE = lambda path: path.end.root

    def __init__(self, criterion, applies_to=NODE):
        self.criterion = criterion
        self.applies_to = applies_to

    def __call__(self, tree):
        visitor = self.Visitor(self.criterion, self.applies_to)
        return RichTreeWalk(visitor)(tree)

    PATH = staticmethod(PATH)
    NODE = staticmethod(NODE)
    VALUE = staticmethod(VALUE)


if __name__ == "__main__":
    from syntax.tree.build import TreeAssistant

    t = TreeAssistant.build((1, [2, 3]))
    print(ScanFor(lambda x: x % 2, applies_to=ScanFor.VALUE)(t))
