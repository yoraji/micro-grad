# Yoraji Micrograd Pro 🚀

An advanced, educational scalar autograd engine built from scratch in Python. Expanding on classic micrograd architectures, this project implements full automatic differentiation—including **subtraction**, **division**, **exponentiation (`**`)**, and the **exponential function (`exp`)**—complete with exact chain-rule derivations and computation graph visualization.

---

## 🧠 What is This?

Deep learning frameworks like PyTorch and TensorFlow rely on automatic differentiation to calculate gradients across massive neural networks. This repository demystifies that magic by building a tiny, transparent scalar autograd engine in pure Python. 

It dynamically tracks operations as you write math, constructs a Directed Acyclic Graph (DAG), performs a topological sort, and executes reverse-mode backpropagation using the chain rule.

### Key Features
* **Expanded Mathematical Support:** Implements custom gradient functions for addition, multiplication, subtraction, division, power (`**`), negation, and `exp`.
* **Dynamic Computation Graph:** Automatically traces dependencies via `_prev` sets and local operator closures (`_backward`).
* **Clean & Compact:** Zero heavy machine learning dependencies—built using only standard Python and Graphviz.
* **Graph Visualization:** Renders your computation graph and gradient flow visually using Graphviz SVG diagrams.

---

## 🛠️ Installation & Requirements

To run the engine and render computation graphs, you will need Python and the `graphviz` package.

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/yoraji-micrograd-pro.git](https://github.com/your-username/yoraji-micrograd-pro.git)
   cd yoraji-micrograd-pro