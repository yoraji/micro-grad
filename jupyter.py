# 1. Imports
import os
from graphviz import Digraph
from IPython.display import display

# 2. Fix for Windows PATH (Only needed if you get ExecutableNotFound)
# Uncomment the next line if you still get the "ExecutableNotFound" error
# os.environ["PATH"] += os.pathsep + r"C:\Program Files\Graphviz\bin"

# 3. Graph Visualization Functions
def trace(root):
    nodes, edges = set(), set()
    def build(v):
        if v not in nodes:
            nodes.add(v)
            for child in v._prev:
                edges.add((child, v))
                build(child)
    build(root)
    return nodes, edges

def draw_dot(root):
    dot = Digraph(format='svg', graph_attr={'rankdir': 'LR'})  # LR = Left to Right
    
    nodes, edges = trace(root)
    for n in nodes:
        uid = str(id(n))
        # Create a rectangular record node for the data and grad
        dot.node(name=uid, label="{ data %.4f | grad %.4f }" % (n.data, n.grad), shape='record')
        
        if n._op:
            # Create an operation node (e.g., +, *)
            dot.node(name=uid + n._op, label=n._op)
            dot.edge(uid + n._op, uid)
            
    for n1, n2 in edges:
        # Connect the nodes
        dot.edge(str(id(n1)), str(id(n2)) + n2._op)
                
    return dot

# 4. The Value Class
class Value:
    def __init__(self, data, _children=(), _op=''):
        self.data = data
        self.grad = 0.0              # Added grad for backpropagation later!
        self._prev = set(_children)  
        self._op = _op               

    def __repr__(self): 
        return f"Value(data={self.data}, grad={self.grad})"
        
    def __add__(self, other):
        # Pass (self, other) as children, and '+' as op
        added = Value(self.data + other.data, (self, other), '+')
        return added
        
    def __mul__(self, other):
        # Pass (self, other) as children, and '*' as op
        added = Value(self.data * other.data, (self, other), '*')
        return added

# 5. Testing the Code (The AND gate / Math expression)
a = Value(2.0)
b = Value(-3)
c = Value(10)
d = a * c + b

# 6. Display the graph
display(draw_dot(d))

