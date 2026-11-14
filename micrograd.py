# ============================================================
#  micrograd — Full Autograd Engine + Gradient Check
#  Run in a single Jupyter cell.
# ============================================================

import os
from graphviz import Digraph
from IPython.display import display

# --- Windows PATH fix (safe to leave; harmless on other OSes) ---
graphviz_path = r"C:\Program Files\Graphviz\bin"
if os.path.exists(graphviz_path):
    os.environ["PATH"] += os.pathsep + graphviz_path

# ============================================================
#  1. The Value class (data + graph + local gradient rules)
# ============================================================
class Value:
    def __init__(self, data, _children=(), _op='', label=''):
        self.data = data
        self.grad = 0.0
        self._backward = lambda: None          # no-op by default (leaves)
        self._prev = set(_children)
        self._op = _op
        self.label = label

    def __repr__(self):
        return f"Value(data={self.data}, grad={self.grad})"

    # ---- operations ----
    def __add__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data + other.data, (self, other), '+')
        def _backward():
            self.grad  += 1.0 * out.grad
            other.grad += 1.0 * out.grad
        out._backward = _backward
        return out

    def __mul__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data * other.data, (self, other), '*')
        def _backward():
            self.grad  += other.data * out.grad
            other.grad += self.data  * out.grad
        out._backward = _backward
        return out

    # ---- the backward pass (topological order + chain rule) ----
    def backward(self):
        topo = []
        visited = set()
        def build(v):
            if v not in visited:
                visited.add(v)
                for c in v._prev:
                    build(c)
                topo.append(v)
        build(self)

        self.grad = 1.0                       # seed: dL/dL = 1

        for node in reversed(topo):           # children-first → walk backwards
            node._backward()

# ============================================================
#  2. Graph visualization
# ============================================================
def trace(root):
    nodes, edges = set(), set()
    def build(v):
        if v not in nodes:
            nodes.add(v)
            for c in v._prev:
                edges.add((c, v))
                build(c)
    build(root)
    return nodes, edges

def draw_dot(root):
    dot = Digraph(format='svg', graph_attr={'rankdir': 'LR'})
    nodes, edges = trace(root)
    for n in nodes:
        uid = str(id(n))
        dot.node(name=uid,
                 label="{ %s | data %.4f | grad %.4f }" % (n.label, n.data, n.grad),
                 shape='record')
        if n._op:
            dot.node(name=uid + n._op, label=n._op)
            dot.edge(uid + n._op, uid)
    for n1, n2 in edges:
        dot.edge(str(id(n1)), str(id(n2)) + n2._op)
    return dot

# ============================================================
#  3. Build the expression and run backprop
#     L = ((a * c) + b) * f   with a=2, c=10, b=-3, f=-6
# ============================================================
a = Value(2.0, label='a')
b = Value(-3.0, label='b')
c = Value(10.0, label='c')
e = a * c; e.label = 'e'
d = e + b; d.label = 'd'
f = Value(-6.0, label='f')
L = d * f; L.label = 'L'

L.backward()

print("=== Analytic gradients (micrograd) ===")
for v in [L, d, e, f, b, c, a]:
    print(f"  {v.label}.grad = {v.grad}")

# ============================================================
#  4. Numeric gradient check (finite difference)
# ============================================================
def build_expr(b_val, f_val):
    a_ = Value(2.0);  c_ = Value(10.0)
    b_ = Value(b_val); f_ = Value(f_val)
    return ((a_ * c_) + b_) * f_

def numeric_grad(fn, base, h=1e-6):
    return (fn(base + h).data - fn(base).data) / h

print("\n=== Gradient check (numeric vs analytic) ===")
checks = {
    'b': numeric_grad(lambda x: build_expr(x, -6), -3),
    'f': numeric_grad(lambda x: build_expr(-3, x), -6),
}
for name, num in checks.items():
    ana = getattr({'b': b, 'f': f}[name], 'grad')
    diff = abs(ana - num)
    status = "✅ PASS" if diff < 1e-4 else "❌ FAIL"
    print(f"  ∂L/∂{name}: analytic={ana:+.6f}  numeric={num:+.6f}  diff={diff:.2e}  {status}")

# ============================================================
#  5. Draw the graph
# ============================================================
display(draw_dot(L))