import ctypes
import difflib
import re
import sys
import textwrap
from tkinter import filedialog

import clipboard
import customtkinter as ctk

myappid = 'mycompany.myproduct.subproduct.version'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

PADX = 12
PADY = 8
BTN_HEIGHT = 40
BTN_WIDTH = 140
CORNER = 12
THEME_PATH = "themes/breeze.json"
FONT_FAMILY = "Arial"
FONT_SIZE = 13
LABEL_FONT = (FONT_FAMILY, FONT_SIZE)
BUTTON_FONT = (FONT_FAMILY, FONT_SIZE)
INPUT_FONT = (FONT_FAMILY, FONT_SIZE)
OR_LABEL_FONT = (FONT_FAMILY, 16)
FORMAT_TEXT_FONT = ("Consolas", FONT_SIZE)
TEXT_FILETYPES = [
    (
        "Text files",
        "*.txt *.md *.csv *.tsv *.json *.xml *.html *.css *.js *.py *.log *.ini *.cfg *.yaml *.yml",
    ),
    ("All files", "*.*"),
]

ctk.set_appearance_mode("System")
ctk.set_default_color_theme(THEME_PATH)


class SeparatorLine(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master, height=4, corner_radius=5)
        line = ctk.CTkFrame(self, width=780, height=4, corner_radius=5)
        line.grid(row=0, column=0, sticky="nsew")
        line.grid_propagate(False)


class TxtUtils(ctk.CTkScrollableFrame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self._shift_pressed = False
        self._middle_scroll_active = False
        self._middle_last_y = 0
        self.currentSubmenu = None

        self._bind_scroll_events()
        self._create_main_menu()

    def _bind_scroll_events(self):
        self.bind_all("<ButtonPress-2>", self._start_middle_scroll, add="+")
        self.bind_all("<B2-Motion>", self._middle_scroll, add="+")
        self.bind_all("<ButtonRelease-2>", self._end_middle_scroll, add="+")
        self.bind_all("<Button-4>", self._mouse_wheel_all, add="+")
        self.bind_all("<Button-5>", self._mouse_wheel_all, add="+")
        self.bind_all("<Shift_L>", self._set_shift_active, add="+")
        self.bind_all("<Shift_R>", self._set_shift_active, add="+")
        self.bind_all("<KeyRelease-Shift_L>", self._set_shift_inactive, add="+")
        self.bind_all("<KeyRelease-Shift_R>", self._set_shift_inactive, add="+")

        self._parent_canvas.bind("<ButtonPress-2>", self._start_middle_scroll, add="+")
        self._parent_canvas.bind("<B2-Motion>", self._middle_scroll, add="+")
        self._parent_canvas.bind("<ButtonRelease-2>", self._end_middle_scroll, add="+")
        self._parent_canvas.bind("<Button-4>", self._mouse_wheel_all, add="+")
        self._parent_canvas.bind("<Button-5>", self._mouse_wheel_all, add="+")

    def _set_shift_active(self, event=None):
        self._shift_pressed = True

    def _set_shift_inactive(self, event=None):
        self._shift_pressed = False

    def _start_middle_scroll(self, event):
        self._middle_scroll_active = True
        self._middle_last_y = event.y_root
        try:
            self._parent_canvas.grab_set_global()
        except Exception:
            pass

    def _middle_scroll(self, event):
        if not self._middle_scroll_active:
            return

        dy = event.y_root - self._middle_last_y
        self._middle_last_y = event.y_root
        if dy == 0:
            return

        units = max(1, abs(int(dy / 2))) * 12
        direction = -1 if dy > 0 else 1
        self._parent_canvas.yview_scroll(direction * units, "units")

    def _end_middle_scroll(self, event):
        self._middle_scroll_active = False
        try:
            self._parent_canvas.grab_release()
        except Exception:
            pass

    def _event_inside_scrollable_area(self, event):
        widget = self.winfo_containing(event.x_root, event.y_root)
        while widget is not None:
            if widget in (self, self._parent_canvas):
                return True
            widget = getattr(widget, "master", None)
        return False

    def _mouse_wheel_all(self, event):
        if not self._event_inside_scrollable_area(event):
            return

        if sys.platform.startswith("win"):
            delta = int(event.delta / 120) if event.delta else 0
        elif sys.platform == "darwin":
            delta = int(event.delta)
        elif hasattr(event, "num") and event.num in (4, 5):
            delta = 1 if event.num == 4 else -1
        else:
            delta = int(event.delta / 120) if event.delta else 0

        if delta == 0:
            return

        scroll_units = -delta * 16
        if self._shift_pressed:
            if self._parent_canvas.xview() != (0.0, 1.0):
                self._parent_canvas.xview_scroll(scroll_units, "units")
        else:
            if self._parent_canvas.yview() != (0.0, 1.0):
                self._parent_canvas.yview_scroll(scroll_units, "units")

    def _create_main_menu(self):
        self.txtUtilsContainer = ctk.CTkFrame(self)
        self.txtUtilsContainer.columnconfigure((0, 1, 2, 3), weight=1)
        self.txtUtilsContainer.grid(row=0, column=0, columnspan=5, padx=PADX, pady=PADY, sticky="nsew")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        menu_buttons = [
            ("Text Case Conversion", self.text_case_conversion),
            ("Text Counting", self.text_counting),
            ("Text Manipulation", self.text_manipulation),
            ("Text Formating", self.textFormating),
            ("Text Comparison", self.textComparison),
        ]

        for index, (text, command) in enumerate(menu_buttons):
            ctk.CTkButton(self.txtUtilsContainer, text=text, height=50, font=BUTTON_FONT, command=command).grid(
                row=index // 4, column=index % 4, padx=PADX, pady=PADY, sticky="ew"
            )

    def _configure_grid(self, frame, columns=0, rows=0):
        for col in range(columns):
            frame.columnconfigure(col, weight=1)
        for row in range(rows):
            frame.rowconfigure(row, weight=1)

    def _create_card(self, parent):
        card = ctk.CTkFrame(parent, corner_radius=16)
        card.pack(fill="both", expand=True)
        return card

    def _configure_output_copy(self, parent, row):
        self.outputLabel = ctk.CTkLabel(parent, text="", font=LABEL_FONT)
        self.outputLabel.grid(row=row, column=0, columnspan=3, padx=PADX, pady=PADY, sticky="ew")
        ctk.CTkButton(parent, text="Copy", command=self.copy_to_clipboard, height=BTN_HEIGHT, font=BUTTON_FONT).grid(
            row=row, column=3, padx=PADX, pady=PADY, sticky="ew"
        )

    def copy_to_clipboard(self):
        if hasattr(self, "outputText"):
            text = self.outputText.get("1.0", "end").strip()
        elif hasattr(self, "outputLabel"):
            text = self.outputLabel.cget("text")
        else:
            return
        clipboard.copy(text)

    def get_input_text(self):
        try:
            return self.inputText.get("1.0", "end").strip()
        except Exception:
            return self.inputText.get().strip()

    def get_input_text_raw(self):
        if not hasattr(self, "inputText"):
            return ""
        try:
            return self.inputText.get("1.0", "end")
        except Exception:
            return self.inputText.get()

    def save_text(self, text):
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=TEXT_FILETYPES,
        )
        if not filename:
            return

        with open(filename, "w", encoding="utf-8") as txt_file:
            txt_file.write(text)

    def save_input_text(self):
        self.save_text(self.get_input_text_raw())

    def save_output_text(self):
        if not hasattr(self, "outputText"):
            return
        self.save_text(self.outputText.get("1.0", "end"))

    def select_file(self):
        filename = filedialog.askopenfilename(filetypes=TEXT_FILETYPES)
        if not filename:
            return

        with open(filename, "r", encoding="utf-8") as txt:
            content = txt.read()

        try:
            self.inputText.delete(0, ctk.END)
            self.inputText.insert(0, content)
        except Exception:
            self.inputText.delete("1.0", "end")
            self.inputText.insert("1.0", content)

    def open_submenu(self):
        self.txtUtilsContainer.grid_forget()
        if self.currentSubmenu:
            self.currentSubmenu.destroy()

        self.currentSubmenu = ctk.CTkFrame(self)
        self.currentSubmenu.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.currentSubmenu.rowconfigure(99, weight=1)
        self.currentSubmenu.columnconfigure((0, 1, 2, 3), weight=1)
        return self.currentSubmenu

    def close_submenu(self):
        if self.currentSubmenu:
            self.currentSubmenu.destroy()
            self.currentSubmenu = None
        self.txtUtilsContainer.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    def text_case_conversion(self):
        frame = self.open_submenu()
        self._configure_grid(frame, columns=4, rows=10)

        main = ctk.CTkFrame(frame, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=20, pady=20)
        card = self._create_card(main)

        ctk.CTkButton(card, text="Back", command=self.close_submenu, width=BTN_WIDTH, height=BTN_HEIGHT, font=BUTTON_FONT).grid(
            row=0, column=0, padx=PADX, pady=PADY, sticky="w"
        )

        ctk.CTkButton(card, text="Select File", command=self.select_file, width=BTN_WIDTH, height=BTN_HEIGHT, font=BUTTON_FONT).grid(
            row=1, column=0, padx=(PADX, 6), pady=(4, 4)
        )
        ctk.CTkButton(card, text="Save", command=self.save_input_text, width=BTN_WIDTH, height=BTN_HEIGHT, font=BUTTON_FONT).grid(
            row=1, column=1, padx=(6, 6), pady=(4, 4)
        )
        ctk.CTkLabel(card, text="or", font=OR_LABEL_FONT, anchor="center").grid(row=1, column=2, padx=(6, 6), pady=(4, 4), sticky="ns")
        self.inputText = ctk.CTkEntry(card, placeholder_text="Enter text here...", height=BTN_HEIGHT, font=INPUT_FONT)
        self.inputText.grid(row=1, column=3, padx=(6, PADX), pady=(4, 4), sticky="ew")

        conversions = [
            ("UPPERCASE", lambda t: t.upper()),
            ("lowercase", lambda t: t.lower()),
            ("Title Case", lambda t: t.title()),
            ("camelCase", self.to_camel_case),
            ("snake_case", lambda t: "_".join(t.split()).lower()),
            ("kebab-case", lambda t: "-".join(t.split()).lower()),
            ("PascalCase", lambda t: "".join(w.capitalize() for w in t.split())),
            ("flatcase", lambda t: "".join(t.split()).lower()),
            ("CONSTANT_CASE", lambda t: "_".join(t.split()).upper()),
        ]

        for index, (label, func) in enumerate(conversions):
            ctk.CTkButton(
                card,
                text=label,
                height=BTN_HEIGHT,
                font=BUTTON_FONT,
                command=lambda f=func: self.show_output(f(self.get_input_text())),
            ).grid(row=2 + index // 3, column=index % 3, padx=PADX, pady=PADY, sticky="ew")

        self._configure_output_copy(card, row=5)

    def to_camel_case(self, text):
        words = text.split()
        if not words:
            return ""
        return words[0].lower() + "".join(w.capitalize() for w in words[1:])

    def show_output(self, text):
        self.outputLabel.configure(text=text)

    def text_counting(self):
        frame = self.open_submenu()
        self._configure_grid(frame, columns=4, rows=10)

        main = ctk.CTkFrame(frame, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=20, pady=PADY)
        card = self._create_card(main)

        ctk.CTkButton(card, text="Back", command=self.close_submenu, width=BTN_WIDTH, height=BTN_HEIGHT, font=BUTTON_FONT).grid(
            row=0, column=0, padx=PADX, pady=PADY, sticky="w"
        )
        ctk.CTkButton(card, text="Select File", command=self.select_file, width=BTN_WIDTH, height=BTN_HEIGHT, font=BUTTON_FONT).grid(
            row=1, column=0, padx=(PADX, 6), pady=(4, 4)
        )
        ctk.CTkButton(card, text="Save", command=self.save_input_text, width=BTN_WIDTH, height=BTN_HEIGHT, font=BUTTON_FONT).grid(
            row=1, column=1, padx=(6, 6), pady=(4, 4)
        )
        ctk.CTkLabel(card, text="or", font=OR_LABEL_FONT, anchor="center").grid(row=1, column=2, padx=(6, 6), pady=(4, 4), sticky="ns")
        self.inputText = ctk.CTkTextbox(card, height=BTN_HEIGHT, font=INPUT_FONT)
        self.inputText.grid(row=1, column=3, padx=(6, PADX), pady=(4, 4), sticky="ew")

        counters = [
            ("Count Characters", lambda t: len(t)),
            ("Count Words", lambda t: len(t.split())),
            ("Count Lines", lambda t: len(t.splitlines())),
        ]

        for index, (label, func) in enumerate(counters):
            ctk.CTkButton(
                card,
                text=label,
                height=BTN_HEIGHT,
                font=BUTTON_FONT,
                command=lambda f=func: self.show_output(f(self.get_input_text())),
            ).grid(row=2, column=index, padx=PADX, pady=PADY, sticky="ew")

        self._configure_output_copy(card, row=3)

    def text_manipulation(self):
        frame = self.open_submenu()
        self._configure_grid(frame, columns=2, rows=8)

        ctk.CTkButton(
            frame,
            text="Back",
            command=self.close_submenu,
            width=BTN_WIDTH,
            height=BTN_HEIGHT,
            font=BUTTON_FONT,
        ).grid(
            row=0, column=0, padx=PADX, pady=PADY, sticky="w"
        )

        ctk.CTkLabel(frame, text="Input Text:", font=LABEL_FONT).grid(row=1, column=0, sticky="w")
        self.inputText = ctk.CTkTextbox(frame, height=150, font=INPUT_FONT)
        self.inputText.grid(row=2, column=0, columnspan=2, padx=PADX, pady=PADY, sticky="nsew")

        file_buttons = ctk.CTkFrame(frame, fg_color="transparent")
        file_buttons.grid(row=3, column=0, columnspan=2, padx=PADX, pady=PADY, sticky="w")

        ctk.CTkButton(
            file_buttons,
            text="Select File",
            command=self.select_file,
            width=BTN_WIDTH,
            height=BTN_HEIGHT,
            font=BUTTON_FONT,
        ).grid(row=0, column=0, padx=(0, 6), pady=0)
        ctk.CTkButton(
            file_buttons,
            text="Save Output",
            command=self.save_output_text,
            width=BTN_WIDTH,
            height=BTN_HEIGHT,
            font=BUTTON_FONT,
        ).grid(row=0, column=1, padx=(6, 0), pady=0)

        ctk.CTkLabel(frame, text="Choose Operation:", font=LABEL_FONT).grid(row=4, column=0, sticky="w")
        self.operation_choice = ctk.CTkOptionMenu(
            frame,
            values=["Find & Replace", "Remove Whitespace", "Extract Pattern"],
            font=BUTTON_FONT,
        )
        self.operation_choice.grid(row=5, column=0, padx=PADX, pady=PADY, sticky="ew")

        self.patternFrame = ctk.CTkFrame(frame)
        self.patternFrame.grid(row=6, column=0, columnspan=2, sticky="ew", padx=PADX, pady=PADY)

        self.findEntry = ctk.CTkEntry(self.patternFrame, placeholder_text="Find", font=INPUT_FONT)
        self.replaceEntry = ctk.CTkEntry(self.patternFrame, placeholder_text="Replace", font=INPUT_FONT)
        self.regexEntry = ctk.CTkEntry(self.patternFrame, placeholder_text="Regex", font=INPUT_FONT)
        self.regexExplanation = ctk.CTkLabel(self.patternFrame, text="Regex example: \\S+@\\S+", font=LABEL_FONT)

        self.operation_handlers = {
            "Find & Replace": self._find_and_replace,
            "Remove Whitespace": self._remove_whitespace,
            "Extract Pattern": self._extract_pattern,
        }

        self.operation_choice.configure(command=self._update_pattern_fields)
        self._update_pattern_fields("Find & Replace")

        ctk.CTkLabel(frame, text="Output:", font=LABEL_FONT).grid(row=7, column=0, sticky="w")
        self.outputText = ctk.CTkTextbox(frame, height=150, font=INPUT_FONT)
        self.outputText.grid(row=8, column=0, columnspan=2, padx=PADX, pady=PADY, sticky="nsew")
        self.outputText.configure(state="disabled")

        ctk.CTkButton(
            frame,
            text="Copy Output",
            height=BTN_HEIGHT,
            font=BUTTON_FONT,
            command=lambda: clipboard.copy(self.outputText.get("1.0", "end").strip()),
        ).grid(row=9, column=0, columnspan=2, padx=PADX, pady=PADY, sticky="ew")

        ctk.CTkButton(frame, text="Run", command=self._process_text_operation, height=BTN_HEIGHT, font=BUTTON_FONT).grid(
            row=10, column=0, columnspan=2, padx=PADX, pady=PADY, sticky="ew"
        )

    # -------------------- TEXT FORMATING --------------------
    def textFormating(self):
        frame = self.open_submenu()
        self._configure_grid(frame, columns=2, rows=8)

        ctk.CTkButton(
            frame,
            text="Back",
            command=self.close_submenu,
            width=BTN_WIDTH,
            height=BTN_HEIGHT,
            font=BUTTON_FONT,
        ).grid(row=0, column=0, padx=PADX, pady=PADY, sticky="w")

        ctk.CTkLabel(frame, text="Input Text:", font=LABEL_FONT).grid(row=1, column=0, sticky="w")
        self.inputText = ctk.CTkTextbox(frame, height=150, font=FORMAT_TEXT_FONT, wrap="none")
        self.inputText.grid(row=2, column=0, columnspan=2, padx=PADX, pady=PADY, sticky="nsew")

        file_buttons = ctk.CTkFrame(frame, fg_color="transparent")
        file_buttons.grid(row=3, column=0, columnspan=2, padx=PADX, pady=PADY, sticky="w")

        ctk.CTkButton(
            file_buttons,
            text="Select File",
            command=self.select_file,
            width=BTN_WIDTH,
            height=BTN_HEIGHT,
            font=BUTTON_FONT,
        ).grid(row=0, column=0, padx=(0, 6), pady=0)

        ctk.CTkLabel(frame, text="Choose Format:", font=LABEL_FONT).grid(row=4, column=0, sticky="w")
        self.format_choice = ctk.CTkOptionMenu(
            frame,
            values=["Indent Text", "Align Left", "Align Center", "Align Right", "Wrap Text"],
            font=BUTTON_FONT,
        )
        self.format_choice.grid(row=5, column=0, padx=PADX, pady=PADY, sticky="ew")

        self.formatOptionsFrame = ctk.CTkFrame(frame)
        self.formatOptionsFrame.grid(row=6, column=0, columnspan=2, sticky="ew", padx=PADX, pady=PADY)

        self.indentEntry = ctk.CTkEntry(self.formatOptionsFrame, placeholder_text="Indent", width=90, font=INPUT_FONT)
        self.widthEntry = ctk.CTkEntry(self.formatOptionsFrame, placeholder_text="Width", width=90, font=INPUT_FONT)
        self.indentUnitLabel = ctk.CTkLabel(self.formatOptionsFrame, text="spaces", font=LABEL_FONT)
        self.widthUnitLabel = ctk.CTkLabel(self.formatOptionsFrame, text="characters", font=LABEL_FONT)
        self.alignInfoLabel = ctk.CTkLabel(self.formatOptionsFrame, text="Uses output box width", font=LABEL_FONT)
        self.indentEntry.insert(0, "4")
        self.widthEntry.insert(0, "80")

        self.format_choice.configure(command=self._update_format_fields)
        self._update_format_fields("Indent Text")

        ctk.CTkLabel(frame, text="Output:", font=LABEL_FONT).grid(row=7, column=0, sticky="w")
        self.outputText = ctk.CTkTextbox(frame, height=150, font=FORMAT_TEXT_FONT, wrap="none")
        self.outputText.grid(row=8, column=0, columnspan=2, padx=PADX, pady=PADY, sticky="nsew")
        self.outputText.configure(state="disabled")

        output_buttons = ctk.CTkFrame(frame, fg_color="transparent")
        output_buttons.grid(row=9, column=0, columnspan=2, padx=PADX, pady=PADY, sticky="ew")
        output_buttons.columnconfigure((0, 1), weight=1)

        ctk.CTkButton(
            output_buttons,
            text="Copy Output",
            height=BTN_HEIGHT,
            font=BUTTON_FONT,
            command=lambda: clipboard.copy(self.outputText.get("1.0", "end-1c")),
        ).grid(row=0, column=0, padx=(0, 6), pady=0, sticky="ew")
        ctk.CTkButton(
            output_buttons,
            text="Save Output",
            command=self.save_output_text,
            height=BTN_HEIGHT,
            font=BUTTON_FONT,
        ).grid(row=0, column=1, padx=(6, 0), pady=0, sticky="ew")

        ctk.CTkButton(frame, text="Run", command=self._process_text_format, height=BTN_HEIGHT, font=BUTTON_FONT).grid(
            row=10, column=0, columnspan=2, padx=PADX, pady=PADY, sticky="ew"
        )

    def _update_format_fields(self, choice):
        for widget in self.formatOptionsFrame.winfo_children():
            widget.grid_forget()

        if choice == "Indent Text":
            self.indentEntry.grid(row=0, column=0, padx=(PADX, 6), pady=PADY, sticky="w")
            self.indentUnitLabel.grid(row=0, column=1, padx=(0, PADX), pady=PADY, sticky="w")
        elif choice == "Wrap Text":
            self.widthEntry.grid(row=0, column=0, padx=(PADX, 6), pady=PADY, sticky="w")
            self.widthUnitLabel.grid(row=0, column=1, padx=(0, PADX), pady=PADY, sticky="w")
        elif choice in ("Align Left", "Align Center", "Align Right"):
            self.alignInfoLabel.grid(row=0, column=0, padx=PADX, pady=PADY, sticky="w")

    def _process_text_format(self):
        text = self.inputText.get("1.0", "end-1c")
        choice = self.format_choice.get()

        # Read user values with sensible defaults if the entry is blank or invalid.
        indent_spaces = self._get_positive_int(self.indentEntry.get(), 4)
        width = self._get_positive_int(self.widthEntry.get(), 80)

        if choice == "Indent Text":
            result = self._indent_text(text, indent_spaces)
            self._show_format_output(result)
        elif choice == "Align Center":
            result = self._align_text(text)
            self._show_format_output(result, "center")
        elif choice == "Align Right":
            result = self._align_text(text)
            self._show_format_output(result, "right")
        elif choice == "Wrap Text":
            result = self._wrap_text(text, width)
            self._show_format_output(result)
        else:
            result = self._align_text(text)
            self._show_format_output(result, "left")

    def _show_format_output(self, text, alignment=None):
        self.outputText.configure(state="normal")
        self.outputText.configure(wrap="word" if alignment else "none")
        self.outputText.delete("1.0", "end")
        self.outputText.insert("1.0", text)
        if alignment:
            self.outputText.tag_config("aligned_text", justify=alignment)
            self.outputText.tag_add("aligned_text", "1.0", "end")
        self.outputText.configure(state="disabled")

    def _get_positive_int(self, value, default):
        try:
            number = int(value)
        except ValueError:
            return default
        return number if number > 0 else default

    def _indent_text(self, text, spaces):
        indent = " " * spaces
        return "\n".join(indent + line if line else line for line in text.splitlines())

    def _align_text(self, text):
        return "\n".join(line.strip() for line in text.splitlines())

    def _wrap_text(self, text, width):
        wrapped_blocks = []
        for block in text.splitlines():
            wrapped_blocks.append(textwrap.fill(block, width=width) if block else "")
        return "\n".join(wrapped_blocks)

    # -------------------- TEXT COMPARISON --------------------
    def textComparison(self):
        frame = self.open_submenu()
        self._configure_grid(frame, columns=2, rows=8)

        self.comparisonFileOne = ""
        self.comparisonFileTwo = ""

        ctk.CTkButton(
            frame,
            text="Back",
            command=self.close_submenu,
            width=BTN_WIDTH,
            height=BTN_HEIGHT,
            font=BUTTON_FONT,
        ).grid(row=0, column=0, padx=PADX, pady=PADY, sticky="w")

        ctk.CTkLabel(frame, text="Text Files:", font=LABEL_FONT).grid(row=1, column=0, sticky="w")
        file_buttons = ctk.CTkFrame(frame, fg_color="transparent")
        file_buttons.grid(row=2, column=0, columnspan=2, padx=PADX, pady=PADY, sticky="ew")
        file_buttons.columnconfigure((1, 3), weight=1)

        ctk.CTkButton(
            file_buttons,
            text="Select Original",
            command=lambda: self._select_comparison_file(1),
            width=BTN_WIDTH,
            height=BTN_HEIGHT,
            font=BUTTON_FONT,
        ).grid(row=0, column=0, padx=(0, 6), pady=(0, PADY), sticky="w")
        self.comparisonFileOneLabel = ctk.CTkLabel(file_buttons, text="No file selected", font=LABEL_FONT, anchor="w")
        self.comparisonFileOneLabel.grid(row=0, column=1, padx=(0, PADX), pady=(0, PADY), sticky="ew")

        ctk.CTkButton(
            file_buttons,
            text="Select Modified",
            command=lambda: self._select_comparison_file(2),
            width=BTN_WIDTH,
            height=BTN_HEIGHT,
            font=BUTTON_FONT,
        ).grid(row=1, column=0, padx=(0, 6), pady=0, sticky="w")
        self.comparisonFileTwoLabel = ctk.CTkLabel(file_buttons, text="No file selected", font=LABEL_FONT, anchor="w")
        self.comparisonFileTwoLabel.grid(row=1, column=1, padx=(0, PADX), pady=0, sticky="ew")

        ctk.CTkButton(
            frame,
            text="Generate Diff Report",
            command=self._process_text_comparison,
            height=BTN_HEIGHT,
            font=BUTTON_FONT,
        ).grid(row=3, column=0, columnspan=2, padx=PADX, pady=PADY, sticky="ew")

        ctk.CTkLabel(frame, text="Diff Report:", font=LABEL_FONT).grid(row=4, column=0, sticky="w")
        self.outputText = ctk.CTkTextbox(frame, height=260, font=FORMAT_TEXT_FONT, wrap="none")
        self.outputText.grid(row=5, column=0, columnspan=2, padx=PADX, pady=PADY, sticky="nsew")
        self.outputText.configure(state="disabled")

        output_buttons = ctk.CTkFrame(frame, fg_color="transparent")
        output_buttons.grid(row=6, column=0, columnspan=2, padx=PADX, pady=PADY, sticky="ew")
        output_buttons.columnconfigure((0, 1), weight=1)

        ctk.CTkButton(
            output_buttons,
            text="Copy Report",
            height=BTN_HEIGHT,
            font=BUTTON_FONT,
            command=lambda: clipboard.copy(self.outputText.get("1.0", "end-1c")),
        ).grid(row=0, column=0, padx=(0, 6), pady=0, sticky="ew")
        ctk.CTkButton(
            output_buttons,
            text="Save Report",
            command=self.save_output_text,
            height=BTN_HEIGHT,
            font=BUTTON_FONT,
        ).grid(row=0, column=1, padx=(6, 0), pady=0, sticky="ew")

    def _select_comparison_file(self, file_number):
        filename = filedialog.askopenfilename(filetypes=TEXT_FILETYPES)
        if not filename:
            return

        if file_number == 1:
            self.comparisonFileOne = filename
            self.comparisonFileOneLabel.configure(text=filename)
        else:
            self.comparisonFileTwo = filename
            self.comparisonFileTwoLabel.configure(text=filename)

    def _process_text_comparison(self):
        if not self.comparisonFileOne or not self.comparisonFileTwo:
            self._show_comparison_report("Select two text files before generating a report.")
            return

        with open(self.comparisonFileOne, "r", encoding="utf-8") as first_file:
            original_lines = first_file.read().splitlines()
        with open(self.comparisonFileTwo, "r", encoding="utf-8") as second_file:
            modified_lines = second_file.read().splitlines()

        report_lines = self._build_diff_report(original_lines, modified_lines)
        self._show_comparison_report("\n".join(report_lines))

    def _build_diff_report(self, original_lines, modified_lines):
        matcher = difflib.SequenceMatcher(None, original_lines, modified_lines)
        report_lines = ["Text Comparison Report", ""]

        for tag, original_start, original_end, modified_start, modified_end in matcher.get_opcodes():
            if tag == "equal":
                continue

            # Convert SequenceMatcher opcodes into readable added, removed, and modified sections.
            if tag == "insert":
                for index, line in enumerate(modified_lines[modified_start:modified_end], start=modified_start + 1):
                    report_lines.append(f"+ Added line {index}: {line}")
            elif tag == "delete":
                for index, line in enumerate(original_lines[original_start:original_end], start=original_start + 1):
                    report_lines.append(f"- Removed line {index}: {line}")
            elif tag == "replace":
                original_block = original_lines[original_start:original_end]
                modified_block = modified_lines[modified_start:modified_end]
                for offset, (old_line, new_line) in enumerate(zip(original_block, modified_block)):
                    report_lines.append(f"* Modified line {original_start + offset + 1}:")
                    report_lines.append(f"-   Original: {old_line}")
                    report_lines.append(f"+   Modified: {new_line}")
                for index, line in enumerate(original_block[len(modified_block):], start=original_start + len(modified_block) + 1):
                    report_lines.append(f"- Removed line {index}: {line}")
                for index, line in enumerate(modified_block[len(original_block):], start=modified_start + len(original_block) + 1):
                    report_lines.append(f"+ Added line {index}: {line}")

        if len(report_lines) == 2:
            report_lines.append("No differences found.")

        return report_lines

    def _show_comparison_report(self, report):
        self.outputText.configure(state="normal")
        self.outputText.delete("1.0", "end")
        self.outputText.insert("1.0", report)

        self.outputText.tag_config("added_line", foreground="#5ad66f")
        self.outputText.tag_config("removed_line", foreground="#ff6b6b")
        self.outputText.tag_config("modified_line", foreground="#ffd166")

        for line_number, line in enumerate(report.splitlines(), start=1):
            if line.startswith("+"):
                self.outputText.tag_add("added_line", f"{line_number}.0", f"{line_number}.end")
            elif line.startswith("-"):
                self.outputText.tag_add("removed_line", f"{line_number}.0", f"{line_number}.end")
            elif line.startswith("*"):
                self.outputText.tag_add("modified_line", f"{line_number}.0", f"{line_number}.end")

        self.outputText.configure(state="disabled")

    def _update_pattern_fields(self, choice):
        for widget in self.patternFrame.winfo_children():
            widget.grid_forget()
        if choice == "Find & Replace":
            self.findEntry.grid(row=0, column=0, padx=PADX, pady=PADY)
            self.replaceEntry.grid(row=0, column=1, padx=PADX, pady=PADY)
        elif choice == "Extract Pattern":
            self.regexEntry.grid(row=0, column=0, padx=PADX, pady=PADY)
            self.regexExplanation.grid(row=1, column=0, padx=PADX, pady=PADY)

    def _find_and_replace(self, text):
        return text.replace(self.findEntry.get(), self.replaceEntry.get())

    def _remove_whitespace(self, text):
        return "".join(text.split())

    def _extract_pattern(self, text):
        matches = re.findall(self.regexEntry.get(), text)
        return "\n".join(matches) if matches else "No matches found."

    def _process_text_operation(self):
        text = self.inputText.get("1.0", "end").strip()
        handler = self.operation_handlers.get(self.operation_choice.get())
        if handler is None:
            return
        result = handler(text)
        self.outputText.configure(state="normal")
        self.outputText.delete("1.0", "end")
        self.outputText.insert("1.0", result)
        self.outputText.configure(state="disabled")


class Forgedy(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Forgedy")
        self.geometry("800x600")
        self.columnconfigure((0, 1, 2, 3), weight=1)
        self.rowconfigure(2, weight=1)
        self.txt_utils_frame = None

        self._create_top_buttons()
        self.separator = SeparatorLine(self)
        self.separator.grid(row=1, column=0, columnspan=4, padx=PADX, pady=PADY, sticky="ew")

    def _create_top_buttons(self):
        buttons = [
            ("Image Utilities", None),
            ("Text Utilities", self.open_txt_utils),
            ("Audio Utilities", None),
            ("Video Utilities", None),
        ]

        for index, (text, command) in enumerate(buttons):
            button = ctk.CTkButton(
                self,
                text=text,
                width=100,
                height=50,
                font=BUTTON_FONT,
                command=command if command else lambda: None,
            )
            button.grid(row=0, column=index, padx=PADX, pady=PADY, sticky="ew")

    def open_txt_utils(self):
        if self.txt_utils_frame:
            self.txt_utils_frame.destroy()

        self.txt_utils_frame = TxtUtils(self)
        self.txt_utils_frame.grid(row=2, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")


if __name__ == "__main__":
    app = Forgedy()
    app.iconbitmap("icon-no-bg.ico")
    app.mainloop()
