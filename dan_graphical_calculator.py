#!/usr/bin/env python3
"""
dan_graphical_calculator.py
Mini-readme: Provides Dan, a green-themed graphical calculator application with
optional function graphing.
Structure:
    - safe_eval: Safely evaluates arithmetic expressions using Python's AST and
      optional variable substitution.
    - CalculatorApp: Handles GUI creation, user interactions, and plotting.
    - main: Parses command-line arguments and launches GUI or CLI evaluation.
Usage:
    - python dan_graphical_calculator.py                  # Launches GUI
    - python dan_graphical_calculator.py --expression "2+2"  # CLI evaluation
"""

from __future__ import annotations

import argparse
import ast
import logging
import operator
import sys
import tkinter as tk
from tkinter import messagebox, ttk

import matplotlib.pyplot as plt

# Configure logging for both console and file outputs
logger = logging.getLogger("dan_calculator")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
if not logger.handlers:
    file_handler = logging.FileHandler("dan_calculator.log")
    file_handler.setFormatter(formatter)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

# Allowed operators for safe evaluation
_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
}


def safe_eval(expression: str, variables: dict[str, float] | None = None) -> float:
    """Safely evaluate a mathematical expression.

    Args:
        expression: String containing the expression to evaluate.
        variables: Mapping of variable names to values for substitution.

    Returns:
        The numerical result of the expression.

    Raises:
        ValueError: If the expression contains unsupported operations or
            undefined variables.
    """

    variables = variables or {}

    def _eval(node: ast.AST) -> float:
        if isinstance(node, ast.BinOp):
            op_type = type(node.op)
            if op_type in _ALLOWED_OPERATORS:
                left = _eval(node.left)
                right = _eval(node.right)
                return _ALLOWED_OPERATORS[op_type](left, right)
            raise ValueError(f"Operator {op_type} is not allowed")
        if isinstance(node, ast.UnaryOp):
            op_type = type(node.op)
            if op_type in _ALLOWED_OPERATORS:
                operand = _eval(node.operand)
                return _ALLOWED_OPERATORS[op_type](operand)
            raise ValueError(f"Unary operator {op_type} is not allowed")
        if isinstance(node, ast.Name):
            if node.id in variables:
                return variables[node.id]
            raise ValueError(f"Use of undefined variable '{node.id}'")
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported expression element: {ast.dump(node)}")

    logger.debug("Evaluating expression: %s with variables %s", expression, variables)
    tree = ast.parse(expression, mode="eval")
    return _eval(tree.body)


class CalculatorApp:
    """Main application class for Dan calculator."""

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Dan - Green Calculator")
        self.root.configure(bg="#ccffcc")  # Light green background
        self.expression_var = tk.StringVar()
        self._create_widgets()
        self.root.bind("<Key>", self._on_keypress)

    def _create_widgets(self) -> None:
        """Create and layout widgets."""
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Dan.TButton", background="#006400", foreground="white", padding=10, font=("Helvetica", 12))
        style.map("Dan.TButton", background=[("active", "#228B22")])
        style.configure("Dan.TLabel", background="#ccffcc", foreground="black", font=("Helvetica", 14))
        style.configure("Dan.TEntry", fieldbackground="#e0ffe0", foreground="black", font=("Helvetica", 16))

        info = ttk.Label(
            self.root,
            text="Welcome to Dan. Use buttons or keyboard; '=' evaluates, 'C' clears, 'Graph' plots y.",
            style="Dan.TLabel",
        )
        info.grid(row=0, column=0, columnspan=4, pady=(10, 5))

        entry = ttk.Entry(self.root, textvariable=self.expression_var, justify="right", style="Dan.TEntry")
        entry.grid(row=1, column=0, columnspan=4, padx=10, pady=5, sticky="nsew")

        buttons = [
            ("7", 2, 0), ("8", 2, 1), ("9", 2, 2), ("/", 2, 3),
            ("4", 3, 0), ("5", 3, 1), ("6", 3, 2), ("*", 3, 3),
            ("1", 4, 0), ("2", 4, 1), ("3", 4, 2), ("-", 4, 3),
            ("0", 5, 0), (".", 5, 1), ("C", 5, 2), ("+", 5, 3),
        ]

        for (text, row, col) in buttons:
            cmd = lambda t=text: self._on_button_press(t)
            ttk.Button(self.root, text=text, command=cmd, style="Dan.TButton").grid(
                row=row, column=col, padx=5, pady=5, sticky="nsew"
            )

        ttk.Button(
            self.root,
            text="=",
            command=lambda: self._on_button_press("="),
            style="Dan.TButton",
        ).grid(row=6, column=0, padx=5, pady=5, sticky="nsew")

        ttk.Button(
            self.root,
            text="Graph",
            command=self._graph_expression,
            style="Dan.TButton",
        ).grid(row=6, column=1, columnspan=3, padx=5, pady=5, sticky="nsew")

        # Expand grid cells
        for i in range(4):
            self.root.columnconfigure(i, weight=1)
        for i in range(7):
            self.root.rowconfigure(i, weight=1)

    def _on_button_press(self, symbol: str) -> None:
        """Handle button presses."""
        logger.debug("Button pressed: %s", symbol)
        if symbol == "C":
            self._clear()
        elif symbol == "=":
            self._evaluate()
        else:
            current = self.expression_var.get()
            self.expression_var.set(current + symbol)

    def _on_keypress(self, event: tk.Event) -> None:
        """Handle keyboard input."""
        char = event.char
        if char in "0123456789.+-*/":
            self.expression_var.set(self.expression_var.get() + char)
        elif event.keysym == "Return":
            self._evaluate()
        elif event.keysym == "Escape":
            self._clear()
        elif event.keysym.lower() == "g":
            self._graph_expression()

    def _evaluate(self) -> None:
        """Evaluate current expression."""
        expr = self.expression_var.get()
        try:
            result = safe_eval(expr)
            self.expression_var.set(str(result))
            logger.info("Evaluated: %s = %s", expr, result)
        except Exception as exc:  # pragma: no cover - GUI feedback
            logger.exception("Evaluation error for %s", expr)
            self.expression_var.set("Error")

    def _clear(self) -> None:
        """Clear the expression."""
        logger.debug("Clearing expression")
        self.expression_var.set("")

    def _graph_expression(self) -> None:
        """Plot the current expression as y=f(x) using matplotlib."""
        expr = self.expression_var.get()
        xs = [x / 10 for x in range(-100, 101)]  # -10 to 10 step 0.1
        ys: list[float] = []
        for x in xs:
            try:
                ys.append(safe_eval(expr, {"x": x}))
            except Exception as exc:  # pragma: no cover - GUI feedback
                logger.exception("Graphing error for %s at x=%s", expr, x)
                messagebox.showerror("Graph error", f"Cannot graph expression: {exc}")
                return

        plt.figure("Dan Graph")
        plt.plot(xs, ys)
        plt.title(f"y = {expr}")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.grid(True)
        plt.show()
        logger.info("Graphed expression: %s", expr)

    def run(self) -> None:
        """Start Tkinter main loop."""
        self.root.mainloop()


def main() -> None:
    """Entry point for command-line and GUI usage."""
    parser = argparse.ArgumentParser(description="Dan graphical calculator")
    parser.add_argument("--expression", help="Evaluate expression without GUI")
    args = parser.parse_args()

    if args.expression:
        try:
            result = safe_eval(args.expression)
            print(result)
            logger.info("CLI evaluation: %s = %s", args.expression, result)
        except Exception as exc:  # pragma: no cover - CLI feedback
            logger.exception("CLI evaluation error for %s", args.expression)
            print(f"Error: {exc}", file=sys.stderr)
            sys.exit(1)
    else:
        app = CalculatorApp()
        app.run()


if __name__ == "__main__":
    main()
