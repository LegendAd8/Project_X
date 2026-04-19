import tkinter as tk
import math


class ScientificCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Scientific Calculator")
        self.root.geometry("420x600")
        self.root.resizable(False, False)

        self.expression = ""
        self.input_text = tk.StringVar()

        self.create_display()
        self.create_buttons()

    def create_display(self):
        entry = tk.Entry(
            self.root,
            font=("Arial", 24),
            textvariable=self.input_text,
            bd=10,
            insertwidth=2,
            width=20,
            borderwidth=4,
            relief="ridge",
            justify="right",
        )
        entry.grid(row=0, column=0, columnspan=5, ipadx=8, ipady=20, padx=10, pady=20)

    def create_buttons(self):
        buttons = [
            ('C', 1, 0), ('(', 1, 1), (')', 1, 2), ('⌫', 1, 3), ('/', 1, 4),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('*', 2, 3), ('sqrt', 2, 4),
            ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('-', 3, 3), ('^', 3, 4),
            ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('+', 4, 3), ('log', 4, 4),
            ('0', 5, 0), ('.', 5, 1), ('pi', 5, 2), ('sin', 5, 3), ('cos', 5, 4),
            ('tan', 6, 0), ('e', 6, 1), ('ln', 6, 2), ('%', 6, 3), ('=', 6, 4),
        ]

        for (text, row, col) in buttons:
            button = tk.Button(
                self.root,
                text=text,
                padx=18,
                pady=18,
                font=("Arial", 16, "bold"),
                command=lambda value=text: self.on_button_click(value),
            )
            button.grid(row=row, column=col, sticky="nsew", padx=4, pady=4)

        for i in range(7):
            self.root.grid_rowconfigure(i, weight=1)
        for i in range(5):
            self.root.grid_columnconfigure(i, weight=1)

    def on_button_click(self, value):
        if value == 'C':
            self.expression = ""
        elif value == '⌫':
            self.expression = self.expression[:-1]
        elif value == '=':
            self.calculate_result()
            return
        elif value == 'sqrt':
            self.expression += 'sqrt('
        elif value in ['sin', 'cos', 'tan', 'log', 'ln']:
            self.expression += value + '('
        elif value == 'pi':
            self.expression += 'pi'
        elif value == 'e':
            self.expression += 'e'
        elif value == '^':
            self.expression += '**'
        elif value == '%':
            self.expression += '/100'
        else:
            self.expression += value

        self.input_text.set(self.expression)

    def calculate_result(self):
        try:
            expr = self.expression
            allowed_names = {
                'sqrt': math.sqrt,
                'sin': lambda x: math.sin(math.radians(x)),
                'cos': lambda x: math.cos(math.radians(x)),
                'tan': lambda x: math.tan(math.radians(x)),
                'log': math.log10,
                'ln': math.log,
                'pi': math.pi,
                'e': math.e,
            }
            result = eval(expr, {"__builtins__": None}, allowed_names)
            self.expression = str(result)
            self.input_text.set(self.expression)
        except Exception:
            self.expression = ""
            self.input_text.set("Error")


if __name__ == "__main__":
    root = tk.Tk()
    app = ScientificCalculator(root)
    root.mainloop()
