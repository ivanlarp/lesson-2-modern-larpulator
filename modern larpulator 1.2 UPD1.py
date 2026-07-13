import tkinter as tk


class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Калькулятор")
        self.root.geometry("320x500")
        self.root.resizable(False, False)
        self.root.configure(bg="#1a1a1a")

        # Состояние калькулятора
        self.current = "0"      # Текущее число на дисплее
        self.previous = None    # Предыдущее число
        self.operation = None   # Текущая операция
        self.reset_next = False # Флаг сброса дисплея при следующем вводе

        # ===== ДИСПЛЕЙ =====
        display_frame = tk.Frame(root, bg="#000000", height=120)
        display_frame.pack(fill="x", padx=0, pady=0)
        display_frame.pack_propagate(False)

        self.display = tk.Label(
            display_frame,
            text="0",
            font=("Segoe UI", 42, "bold"),
            bg="#000000",
            fg="#ffffff",
            anchor="e",
            padx=20
        )
        self.display.pack(fill="both", expand=True)

        # ===== КНОПКИ =====
        buttons_frame = tk.Frame(root, bg="#1a1a1a")
        buttons_frame.pack(fill="both", expand=True, padx=8, pady=8)

        # Настройка сетки 4 колонки
        for i in range(4):
            buttons_frame.columnconfigure(i, weight=1, uniform="col")
        for i in range(5):
            buttons_frame.rowconfigure(i, weight=1, uniform="row")

        # Определение кнопок: (текст, ряд, колонка, colspan, цвет_фона, цвет_текста, команда)
        buttons = [
            # Ряд 1: AC, ⌫, ÷
            ("AC",   0, 0, 1, "#8a8a8a", "#000000", self.clear_all),
            ("⌫",    0, 1, 1, "#8a8a8a", "#000000", self.backspace),
            ("÷",    0, 2, 2, "#e8870e", "#ffffff", lambda: self.set_op("/")),

            # Ряд 2: 7, 8, 9, ×
            ("7",    1, 0, 1, "#3a3a3a", "#ffffff", lambda: self.add_digit("7")),
            ("8",    1, 1, 1, "#3a3a3a", "#ffffff", lambda: self.add_digit("8")),
            ("9",    1, 2, 1, "#3a3a3a", "#ffffff", lambda: self.add_digit("9")),
            ("×",    1, 3, 1, "#e8870e", "#ffffff", lambda: self.set_op("*")),

            # Ряд 3: 4, 5, 6, −
            ("4",    2, 0, 1, "#3a3a3a", "#ffffff", lambda: self.add_digit("4")),
            ("5",    2, 1, 1, "#3a3a3a", "#ffffff", lambda: self.add_digit("5")),
            ("6",    2, 2, 1, "#3a3a3a", "#ffffff", lambda: self.add_digit("6")),
            ("−",    2, 3, 1, "#e8870e", "#ffffff", lambda: self.set_op("-")),

            # Ряд 4: 1, 2, 3, +
            ("1",    3, 0, 1, "#3a3a3a", "#ffffff", lambda: self.add_digit("1")),
            ("2",    3, 1, 1, "#3a3a3a", "#ffffff", lambda: self.add_digit("2")),
            ("3",    3, 2, 1, "#3a3a3a", "#ffffff", lambda: self.add_digit("3")),
            ("+",    3, 3, 1, "#e8870e", "#ffffff", lambda: self.set_op("+")),

            # Ряд 5: 0 (широкая), ., =
            ("0",    4, 0, 2, "#3a3a3a", "#ffffff", lambda: self.add_digit("0")),
            (".",    4, 2, 1, "#3a3a3a", "#ffffff", lambda: self.add_digit(".")),
            ("=",    4, 3, 1, "#4CAF50", "#ffffff", self.calculate),
        ]

        for text, row, col, colspan, bg, fg, cmd in buttons:
            btn = tk.Button(
                buttons_frame,
                text=text,
                font=("Segoe UI", 22, "bold"),
                bg=bg,
                fg=fg,
                activebackground=self.lighten(bg),
                activeforeground=fg,
                bd=0,
                cursor="hand2",
                command=cmd,
                highlightthickness=0
            )
            btn.grid(row=row, column=col, columnspan=colspan,
                     sticky="nsew", padx=3, pady=3)

        # Поддержка клавиатуры
        self.root.bind("0", lambda e: self.add_digit("0"))
        self.root.bind("1", lambda e: self.add_digit("1"))
        self.root.bind("2", lambda e: self.add_digit("2"))
        self.root.bind("3", lambda e: self.add_digit("3"))
        self.root.bind("4", lambda e: self.add_digit("4"))
        self.root.bind("5", lambda e: self.add_digit("5"))
        self.root.bind("6", lambda e: self.add_digit("6"))
        self.root.bind("7", lambda e: self.add_digit("7"))
        self.root.bind("8", lambda e: self.add_digit("8"))
        self.root.bind("9", lambda e: self.add_digit("9"))
        self.root.bind(".", lambda e: self.add_digit("."))
        self.root.bind(",", lambda e: self.add_digit("."))
        self.root.bind("+", lambda e: self.set_op("+"))
        self.root.bind("-", lambda e: self.set_op("-"))
        self.root.bind("*", lambda e: self.set_op("*"))
        self.root.bind("/", lambda e: self.set_op("/"))
        self.root.bind("<Return>", lambda e: self.calculate())
        self.root.bind("<BackSpace>", lambda e: self.backspace())
        self.root.bind("<Escape>", lambda e: self.clear_all())

    def lighten(self, color):
        """Возвращает более светлый оттенок цвета для эффекта нажатия"""
        color = color.lstrip("#")
        r, g, b = int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16)
        r = min(255, r + 30)
        g = min(255, g + 30)
        b = min(255, b + 30)
        return f"#{r:02x}{g:02x}{b:02x}"

    def update_display(self):
        """Обновление дисплея с адаптивным размером шрифта"""
        text = self.current
        # Адаптивный размер шрифта
        if len(text) > 12:
            size = 24
        elif len(text) > 9:
            size = 30
        elif len(text) > 6:
            size = 36
        else:
            size = 42
        self.display.config(text=text, font=("Segoe UI", size, "bold"))

    def add_digit(self, digit):
        """Добавление цифры на дисплей"""
        if self.reset_next:
            self.current = "0"
            self.reset_next = False

        if digit == "." and "." in self.current:
            return  # Только одна точка

        if self.current == "0" and digit != ".":
            self.current = digit
        else:
            if len(self.current) < 15:  # Ограничение длины
                self.current += digit

        self.update_display()

    def set_op(self, op):
        """Установка операции"""
        try:
            value = float(self.current)
        except ValueError:
            return

        if self.previous is not None and not self.reset_next:
            # Если уже есть предыдущее число и операция - сначала вычисляем
            self.calculate()
            value = float(self.current)

        self.previous = value
        self.operation = op
        self.reset_next = True

    def calculate(self):
        """Вычисление результата"""
        if self.previous is None or self.operation is None:
            return

        try:
            current = float(self.current)
        except ValueError:
            self.current = "Ошибка"
            self.update_display()
            return

        try:
            if self.operation == "+":
                result = self.previous + current
            elif self.operation == "-":
                result = self.previous - current
            elif self.operation == "*":
                result = self.previous * current
            elif self.operation == "/":
                if current == 0:
                    self.current = "Ошибка"
                    self.update_display()
                    self.previous = None
                    self.operation = None
                    self.reset_next = True
                    return
                result = self.previous / current
            else:
                return

            # Округление для избежания проблем с плавающей точкой
            result = round(result, 10)
            if result == int(result):
                result = int(result)

            self.current = str(result)
            self.previous = None
            self.operation = None
            self.reset_next = True
            self.update_display()

        except Exception:
            self.current = "Ошибка"
            self.update_display()
            self.previous = None
            self.operation = None
            self.reset_next = True

    def clear_all(self):
        """Полная очистка (AC)"""
        self.current = "0"
        self.previous = None
        self.operation = None
        self.reset_next = False
        self.update_display()

    def backspace(self):
        """Удаление последнего символа (⌫)"""
        if self.reset_next:
            return
        if len(self.current) > 1:
            self.current = self.current[:-1]
        else:
            self.current = "0"
        self.update_display()


if __name__ == "__main__":
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()
