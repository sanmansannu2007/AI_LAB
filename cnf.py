import re


# --- 1. Expression Tree Nodes ---
class Var:

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class Not:

    def __init__(self, expr):
        self.expr = expr

    def __str__(self):
        return f"~{self.expr}"


class And:

    def __init__(self, left, right):
        self.left, self.right = left, right

    def __str__(self):
        return f"({self.left} ^ {self.right})"


class Or:

    def __init__(self, left, right):
        self.left, self.right = left, right

    def __str__(self):
        return f"({self.left} v {self.right})"


class Implies:

    def __init__(self, left, right):
        self.left, self.right = left, right


class Iff:

    def __init__(self, left, right):
        self.left, self.right = left, right


# --- 2. Simple Recursive Descent Parser ---
# Precedence (highest to lowest): ~ , ^ , v , -> , <->
def parse(formula_str):
    tokens = re.findall(r"<->|->|[~^v()]|[A-Za-z0-9_]+", formula_str)
    pos = 0

    def peek():
        return tokens[pos] if pos < len(tokens) else None

    def consume():
        nonlocal pos
        tok = tokens[pos]
        pos += 1
        return tok

    def parse_iff():
        node = parse_implies()
        while peek() == "<->":
            consume()
            node = Iff(node, parse_implies())
        return node

    def parse_implies():
        node = parse_or()
        if peek() == "->":
            consume()
            node = Implies(node, parse_implies())  # Right-associative
        return node

    def parse_or():
        node = parse_and()
        while peek() == "v":
            consume()
            node = Or(node, parse_and())
        return node

    def parse_and():
        node = parse_not()
        while peek() == "^":
            consume()
            node = And(node, parse_not())
        return node

    def parse_not():
        if peek() == "~":
            consume()
            return Not(parse_not())
        if peek() == "(":
            consume()
            node = parse_iff()
            consume()  # ')'
            return node
        return Var(consume())

    return parse_iff()


# --- 3. CNF Conversion Steps ---
def eliminate_implications(expr):
    if isinstance(expr, Var):
        return expr
    if isinstance(expr, Not):
        return Not(eliminate_implications(expr.expr))
    if isinstance(expr, And):
        return And(
            eliminate_implications(expr.left),
            eliminate_implications(expr.right),
        )
    if isinstance(expr, Or):
        return Or(
            eliminate_implications(expr.left),
            eliminate_implications(expr.right),
        )
    if isinstance(expr, Implies):
        return Or(
            Not(eliminate_implications(expr.left)),
            eliminate_implications(expr.right),
        )
    if isinstance(expr, Iff):
        a = eliminate_implications(expr.left)
        b = eliminate_implications(expr.right)
        return And(Or(Not(a), b), Or(Not(b), a))


def move_negations_inward(expr):
    if isinstance(expr, Var):
        return expr
    if isinstance(expr, Not):
        sub = expr.expr
        if isinstance(sub, Not):
            return move_negations_inward(sub.expr)  # ~~A -> A
        if isinstance(sub, And):
            return Or(
                move_negations_inward(Not(sub.left)),
                move_negations_inward(Not(sub.right)),
            )
        if isinstance(sub, Or):
            return And(
                move_negations_inward(Not(sub.left)),
                move_negations_inward(Not(sub.right)),
            )
        return Not(move_negations_inward(sub))
    if isinstance(expr, And):
        return And(
            move_negations_inward(expr.left), move_negations_inward(expr.right)
        )
    if isinstance(expr, Or):
        return Or(
            move_negations_inward(expr.left), move_negations_inward(expr.right)
        )


def distribute_or_over_and(expr):
    if isinstance(expr, (Var, Not)):
        return expr
    if isinstance(expr, And):
        return And(
            distribute_or_over_and(expr.left),
            distribute_or_over_and(expr.right),
        )
    if isinstance(expr, Or):
        a = distribute_or_over_and(expr.left)
        b = distribute_or_over_and(expr.right)
        if isinstance(b, And):
            return And(
                distribute_or_over_and(Or(a, b.left)),
                distribute_or_over_and(Or(a, b.right)),
            )
        if isinstance(a, And):
            return And(
                distribute_or_over_and(Or(a.left, b)),
                distribute_or_over_and(Or(a.right, b)),
            )
        return Or(a, b)


def to_cnf(formula_str):
    tree = parse(formula_str)
    step1 = eliminate_implications(tree)
    step2 = move_negations_inward(step1)
    step3 = distribute_or_over_and(step2)
    return step3


# --- 4. Sample Test Cases & Output ---
formulas = [
    "P -> Q",
    "~(P v Q)",
    "(P -> Q) -> R",
    "P <-> (Q ^ R)",
]

for f in formulas:
    print(f"Input : {f}")
    print(f"Output: {to_cnf(f)}\n")