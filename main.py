import ctypes
import difflib
import html
import json
import math
import re
import secrets
import string
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
STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "but", "by", "for", "from", "has", "have", "he", "her",
    "his", "i", "in", "is", "it", "its", "of", "on", "or", "our", "she", "that", "the", "their", "they",
    "this", "to", "was", "we", "were", "with", "you", "your",
}

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
            ("Text Generation", self.textGeneration),
            ("Text Validation", self.textValidation),
            ("Text Search", self.textSearch),
            ("Text Sorting", self.textSorting),
            ("Text Merging", self.textMerging),
            ("Text Noise Removal", self.textNoiseRemoval),
            ("Text Escaping", self.textEscaping),
            ("Text Metrics", self.textMetrics),
            ("Text Styling", self.textStyling),
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

    # -------------------- TEXT GENERATION --------------------
    def textGeneration(self):
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

        ctk.CTkLabel(frame, text="Generation Type:", font=LABEL_FONT).grid(row=1, column=0, sticky="w")
        self.generation_choice = ctk.CTkOptionMenu(
            frame,
            values=["Random String", "Password", "Lorem Ipsum", "Template / Pattern"],
            font=BUTTON_FONT,
        )
        self.generation_choice.grid(row=2, column=0, padx=PADX, pady=PADY, sticky="ew")

        self.generationOptionsFrame = ctk.CTkFrame(frame)
        self.generationOptionsFrame.grid(row=3, column=0, columnspan=2, sticky="ew", padx=PADX, pady=PADY)

        self.generationLengthEntry = ctk.CTkEntry(self.generationOptionsFrame, placeholder_text="Length", width=90, font=INPUT_FONT)
        self.generationCountEntry = ctk.CTkEntry(self.generationOptionsFrame, placeholder_text="Count", width=90, font=INPUT_FONT)
        self.generationTemplateEntry = ctk.CTkEntry(
            self.generationOptionsFrame,
            placeholder_text="Template: user-{number}-{word}",
            font=INPUT_FONT,
        )
        self.generationLengthLabel = ctk.CTkLabel(self.generationOptionsFrame, text="characters", font=LABEL_FONT)
        self.generationCountLabel = ctk.CTkLabel(self.generationOptionsFrame, text="items", font=LABEL_FONT)
        self.generationTemplateLabel = ctk.CTkLabel(
            self.generationOptionsFrame,
            text="tokens: {word}, {number}, {letter}, {char}",
            font=LABEL_FONT,
        )
        self.generationLengthEntry.insert(0, "16")
        self.generationCountEntry.insert(0, "5")
        self.generationTemplateEntry.insert(0, "item-{number}-{word}")

        self.generation_choice.configure(command=self._update_generation_fields)
        self._update_generation_fields("Random String")

        ctk.CTkButton(
            frame,
            text="Generate",
            command=self._process_text_generation,
            height=BTN_HEIGHT,
            font=BUTTON_FONT,
        ).grid(row=4, column=0, columnspan=2, padx=PADX, pady=PADY, sticky="ew")

        ctk.CTkLabel(frame, text="Output:", font=LABEL_FONT).grid(row=5, column=0, sticky="w")
        self.outputText = ctk.CTkTextbox(frame, height=220, font=FORMAT_TEXT_FONT, wrap="none")
        self.outputText.grid(row=6, column=0, columnspan=2, padx=PADX, pady=PADY, sticky="nsew")
        self.outputText.configure(state="disabled")

        output_buttons = ctk.CTkFrame(frame, fg_color="transparent")
        output_buttons.grid(row=7, column=0, columnspan=2, padx=PADX, pady=PADY, sticky="ew")
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

    def _update_generation_fields(self, choice):
        for widget in self.generationOptionsFrame.winfo_children():
            widget.grid_forget()

        self.generationCountEntry.grid(row=0, column=0, padx=(PADX, 6), pady=PADY, sticky="w")
        self.generationCountLabel.grid(row=0, column=1, padx=(0, PADX), pady=PADY, sticky="w")

        if choice in ("Random String", "Password"):
            self.generationLengthEntry.grid(row=0, column=2, padx=(0, 6), pady=PADY, sticky="w")
            self.generationLengthLabel.grid(row=0, column=3, padx=(0, PADX), pady=PADY, sticky="w")
        elif choice == "Lorem Ipsum":
            self.generationCountLabel.configure(text="paragraphs")
        else:
            self.generationCountLabel.configure(text="items")
            self.generationTemplateEntry.grid(row=1, column=0, columnspan=4, padx=PADX, pady=(0, 4), sticky="ew")
            self.generationTemplateLabel.grid(row=2, column=0, columnspan=4, padx=PADX, pady=(0, PADY), sticky="w")

        if choice != "Lorem Ipsum":
            self.generationCountLabel.configure(text="items")

    def _process_text_generation(self):
        choice = self.generation_choice.get()
        count = self._get_positive_int(self.generationCountEntry.get(), 5)
        length = self._get_positive_int(self.generationLengthEntry.get(), 16)

        if choice == "Password":
            result = self._generate_passwords(length, count)
        elif choice == "Lorem Ipsum":
            result = self._generate_lorem_ipsum(count)
        elif choice == "Template / Pattern":
            result = self._generate_from_template(self.generationTemplateEntry.get(), count)
        else:
            result = self._generate_random_strings(length, count)

        self.outputText.configure(state="normal")
        self.outputText.delete("1.0", "end")
        self.outputText.insert("1.0", result)
        self.outputText.configure(state="disabled")

    def _generate_random_strings(self, length, count):
        alphabet = string.ascii_letters + string.digits
        return "\n".join("".join(secrets.choice(alphabet) for _ in range(length)) for _ in range(count))

    def _generate_passwords(self, length, count):
        alphabet = string.ascii_letters + string.digits + string.punctuation
        return "\n".join("".join(secrets.choice(alphabet) for _ in range(length)) for _ in range(count))

    def _generate_lorem_ipsum(self, paragraph_count):
        words = (
            "lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod tempor incididunt "
            "ut labore et dolore magna aliqua ut enim ad minim veniam quis nostrud exercitation"
        ).split()
        paragraphs = []
        for _ in range(paragraph_count):
            paragraph_words = [secrets.choice(words) for _ in range(70)]
            paragraph = " ".join(paragraph_words).capitalize() + "."
            paragraphs.append(textwrap.fill(paragraph, width=80))
        return "\n\n".join(paragraphs)

    def _generate_from_template(self, template, count):
        template = template.strip() or "item-{number}-{word}"
        return "\n".join(self._fill_template(template, index) for index in range(1, count + 1))

    def _fill_template(self, template, number):
        words = ["alpha", "bravo", "charlie", "delta", "echo", "forge", "spark", "vector"]
        replacements = {
            "{word}": secrets.choice(words),
            "{number}": str(number),
            "{letter}": secrets.choice(string.ascii_letters),
            "{char}": secrets.choice(string.ascii_letters + string.digits),
        }

        for token, value in replacements.items():
            template = template.replace(token, value)
        return template

    # -------------------- TEXT VALIDATION --------------------
    def textValidation(self):
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

        ctk.CTkLabel(frame, text="Validation Type:", font=LABEL_FONT).grid(row=4, column=0, sticky="w")
        self.validation_choice = ctk.CTkOptionMenu(
            frame,
            values=["Email Addresses", "Phone Numbers", "URLs"],
            font=BUTTON_FONT,
        )
        self.validation_choice.grid(row=5, column=0, padx=PADX, pady=PADY, sticky="ew")

        ctk.CTkButton(
            frame,
            text="Validate",
            command=self._process_text_validation,
            height=BTN_HEIGHT,
            font=BUTTON_FONT,
        ).grid(row=6, column=0, columnspan=2, padx=PADX, pady=PADY, sticky="ew")

        ctk.CTkLabel(frame, text="Validation Report:", font=LABEL_FONT).grid(row=7, column=0, sticky="w")
        self.outputText = ctk.CTkTextbox(frame, height=180, font=FORMAT_TEXT_FONT, wrap="none")
        self.outputText.grid(row=8, column=0, columnspan=2, padx=PADX, pady=PADY, sticky="nsew")
        self.outputText.configure(state="disabled")

        output_buttons = ctk.CTkFrame(frame, fg_color="transparent")
        output_buttons.grid(row=9, column=0, columnspan=2, padx=PADX, pady=PADY, sticky="ew")
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

    def _process_text_validation(self):
        text = self.inputText.get("1.0", "end-1c")
        choice = self.validation_choice.get()

        if choice == "Phone Numbers":
            validator = self._is_valid_phone
        elif choice == "URLs":
            validator = self._is_valid_url
        else:
            validator = self._is_valid_email

        # Validate each non-empty line so files or pasted lists produce useful reports.
        values = [line.strip() for line in text.splitlines() if line.strip()]
        if not values:
            self._show_validation_report("No values to validate.")
            return

        report_lines = []
        valid_count = 0
        for value in values:
            is_valid = validator(value)
            valid_count += 1 if is_valid else 0
            status = "VALID" if is_valid else "INVALID"
            report_lines.append(f"{status}: {value}")

        report_lines.insert(0, f"{choice}: {valid_count}/{len(values)} valid")
        report_lines.insert(1, "")
        self._show_validation_report("\n".join(report_lines))

    def _is_valid_email(self, value):
        pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
        return re.fullmatch(pattern, value) is not None

    def _is_valid_phone(self, value):
        pattern = r"^\+?[0-9][0-9\s().-]{6,}[0-9]$"
        return re.fullmatch(pattern, value) is not None

    def _is_valid_url(self, value):
        pattern = r"^https?://[A-Za-z0-9.-]+\.[A-Za-z]{2,}(/[^\s]*)?$"
        return re.fullmatch(pattern, value) is not None

    def _show_validation_report(self, report):
        self.outputText.configure(state="normal")
        self.outputText.delete("1.0", "end")
        self.outputText.insert("1.0", report)

        self.outputText.tag_config("valid_line", foreground="#5ad66f")
        self.outputText.tag_config("invalid_line", foreground="#ff6b6b")

        for line_number, line in enumerate(report.splitlines(), start=1):
            if line.startswith("VALID:"):
                self.outputText.tag_add("valid_line", f"{line_number}.0", f"{line_number}.end")
            elif line.startswith("INVALID:"):
                self.outputText.tag_add("invalid_line", f"{line_number}.0", f"{line_number}.end")

        self.outputText.configure(state="disabled")

    # -------------------- TEXT SEARCH --------------------
    def textSearch(self):
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

        ctk.CTkLabel(frame, text="Source Text:", font=LABEL_FONT).grid(row=1, column=0, sticky="w")
        self.inputText = ctk.CTkTextbox(frame, height=140, font=FORMAT_TEXT_FONT, wrap="none")
        self.inputText.grid(row=2, column=0, columnspan=2, padx=PADX, pady=PADY, sticky="nsew")

        search_controls = ctk.CTkFrame(frame, fg_color="transparent")
        search_controls.grid(row=3, column=0, columnspan=2, padx=PADX, pady=PADY, sticky="ew")
        search_controls.columnconfigure(1, weight=1)

        ctk.CTkButton(
            search_controls,
            text="Select File",
            command=self.select_file,
            width=BTN_WIDTH,
            height=BTN_HEIGHT,
            font=BUTTON_FONT,
        ).grid(row=0, column=0, padx=(0, 6), pady=0, sticky="w")
        self.searchEntry = ctk.CTkEntry(search_controls, placeholder_text="Search keyword or regex", font=INPUT_FONT)
        self.searchEntry.grid(row=0, column=1, padx=(6, 6), pady=0, sticky="ew")
        self.searchMode = ctk.CTkOptionMenu(search_controls, values=["Keyword", "Regex"], font=BUTTON_FONT)
        self.searchMode.grid(row=0, column=2, padx=(6, 0), pady=0, sticky="ew")

        ctk.CTkButton(
            frame,
            text="Search",
            command=self._process_text_search,
            height=BTN_HEIGHT,
            font=BUTTON_FONT,
        ).grid(row=4, column=0, columnspan=2, padx=PADX, pady=PADY, sticky="ew")

        ctk.CTkLabel(frame, text="Highlighted Source:", font=LABEL_FONT).grid(row=5, column=0, sticky="w")
        self.searchPreviewText = ctk.CTkTextbox(frame, height=140, font=FORMAT_TEXT_FONT, wrap="none")
        self.searchPreviewText.grid(row=6, column=0, columnspan=2, padx=PADX, pady=PADY, sticky="nsew")
        self.searchPreviewText.configure(state="disabled")

        ctk.CTkLabel(frame, text="Search Results:", font=LABEL_FONT).grid(row=7, column=0, sticky="w")
        self.outputText = ctk.CTkTextbox(frame, height=130, font=FORMAT_TEXT_FONT, wrap="none")
        self.outputText.grid(row=8, column=0, columnspan=2, padx=PADX, pady=PADY, sticky="nsew")
        self.outputText.configure(state="disabled")

        output_buttons = ctk.CTkFrame(frame, fg_color="transparent")
        output_buttons.grid(row=9, column=0, columnspan=2, padx=PADX, pady=PADY, sticky="ew")
        output_buttons.columnconfigure((0, 1), weight=1)

        ctk.CTkButton(
            output_buttons,
            text="Copy Results",
            height=BTN_HEIGHT,
            font=BUTTON_FONT,
            command=lambda: clipboard.copy(self.outputText.get("1.0", "end-1c")),
        ).grid(row=0, column=0, padx=(0, 6), pady=0, sticky="ew")
        ctk.CTkButton(
            output_buttons,
            text="Save Results",
            command=self.save_output_text,
            height=BTN_HEIGHT,
            font=BUTTON_FONT,
        ).grid(row=0, column=1, padx=(6, 0), pady=0, sticky="ew")

    def _process_text_search(self):
        text = self.inputText.get("1.0", "end-1c")
        query = self.searchEntry.get()
        use_regex = self.searchMode.get() == "Regex"

        if not query:
            self._show_search_results(text, [], "Enter a search keyword or regex.")
            return

        try:
            matches = self._find_text_matches(text, query, use_regex)
        except re.error as error:
            self._show_search_results(text, [], f"Invalid regex: {error}")
            return

        report = self._build_search_report(text, matches)
        self._show_search_results(text, matches, report)

    def _find_text_matches(self, text, query, use_regex):
        flags = re.MULTILINE
        pattern = query if use_regex else re.escape(query)
        return list(re.finditer(pattern, text, flags))

    def _build_search_report(self, text, matches):
        if not matches:
            return "No matches found."

        lines = text.splitlines(keepends=True)
        line_starts = []
        position = 0
        for line in lines:
            line_starts.append(position)
            position += len(line)

        report_lines = [f"Found {len(matches)} match(es).", ""]
        for match in matches:
            line_number = self._line_number_for_index(line_starts, match.start())
            line_text = lines[line_number - 1].strip()
            report_lines.append(f"Line {line_number}, columns {match.start() - line_starts[line_number - 1] + 1}-{match.end() - line_starts[line_number - 1]}: {match.group(0)}")
            report_lines.append(f"    {line_text}")

        return "\n".join(report_lines)

    def _line_number_for_index(self, line_starts, index):
        line_number = 1
        for current_line, start in enumerate(line_starts, start=1):
            if start > index:
                break
            line_number = current_line
        return line_number

    def _show_search_results(self, text, matches, report):
        self.searchPreviewText.configure(state="normal")
        self.searchPreviewText.delete("1.0", "end")
        self.searchPreviewText.insert("1.0", text)
        self.searchPreviewText.tag_config("search_match", background="#ffd166", foreground="#1f1f1f")

        for match in matches:
            start = f"1.0 + {match.start()} chars"
            end = f"1.0 + {match.end()} chars"
            self.searchPreviewText.tag_add("search_match", start, end)

        self.searchPreviewText.configure(state="disabled")

        self.outputText.configure(state="normal")
        self.outputText.delete("1.0", "end")
        self.outputText.insert("1.0", report)
        self.outputText.configure(state="disabled")

    # -------------------- TEXT SORTING --------------------
    def textSorting(self):
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
        self.inputText = ctk.CTkTextbox(frame, height=170, font=FORMAT_TEXT_FONT, wrap="none")
        self.inputText.grid(row=2, column=0, columnspan=2, padx=PADX, pady=PADY, sticky="nsew")

        sort_controls = ctk.CTkFrame(frame, fg_color="transparent")
        sort_controls.grid(row=3, column=0, columnspan=2, padx=PADX, pady=PADY, sticky="ew")
        sort_controls.columnconfigure((1, 2), weight=1)

        ctk.CTkButton(
            sort_controls,
            text="Select File",
            command=self.select_file,
            width=BTN_WIDTH,
            height=BTN_HEIGHT,
            font=BUTTON_FONT,
        ).grid(row=0, column=0, padx=(0, 6), pady=0, sticky="w")
        self.sort_choice = ctk.CTkOptionMenu(
            sort_controls,
            values=["Alphabetically", "Numerically", "By Length"],
            font=BUTTON_FONT,
        )
        self.sort_choice.grid(row=0, column=1, padx=(6, 6), pady=0, sticky="ew")
        self.sort_order_choice = ctk.CTkOptionMenu(
            sort_controls,
            values=["Ascending", "Descending"],
            font=BUTTON_FONT,
        )
        self.sort_order_choice.grid(row=0, column=2, padx=(6, 0), pady=0, sticky="ew")

        ctk.CTkButton(
            frame,
            text="Sort",
            command=self._process_text_sorting,
            height=BTN_HEIGHT,
            font=BUTTON_FONT,
        ).grid(row=4, column=0, columnspan=2, padx=PADX, pady=PADY, sticky="ew")

        ctk.CTkLabel(frame, text="Output:", font=LABEL_FONT).grid(row=5, column=0, sticky="w")
        self.outputText = ctk.CTkTextbox(frame, height=220, font=FORMAT_TEXT_FONT, wrap="none")
        self.outputText.grid(row=6, column=0, columnspan=2, padx=PADX, pady=PADY, sticky="nsew")
        self.outputText.configure(state="disabled")

        output_buttons = ctk.CTkFrame(frame, fg_color="transparent")
        output_buttons.grid(row=7, column=0, columnspan=2, padx=PADX, pady=PADY, sticky="ew")
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

    def _process_text_sorting(self):
        text = self.inputText.get("1.0", "end-1c")
        lines = text.splitlines()
        choice = self.sort_choice.get()
        reverse_sort = self.sort_order_choice.get() == "Descending"

        # Keep blank lines out of the sort so pasted lists produce clean output.
        sortable_lines = [line for line in lines if line.strip()]
        if choice == "Numerically":
            sorted_lines = sorted(sortable_lines, key=self._numeric_sort_key, reverse=reverse_sort)
        elif choice == "By Length":
            sorted_lines = sorted(sortable_lines, key=lambda line: (len(line), line.lower()), reverse=reverse_sort)
        else:
            sorted_lines = sorted(sortable_lines, key=str.lower, reverse=reverse_sort)

        self.outputText.configure(state="normal")
        self.outputText.delete("1.0", "end")
        self.outputText.insert("1.0", "\n".join(sorted_lines))
        self.outputText.configure(state="disabled")

    def _numeric_sort_key(self, line):
        match = re.search(r"-?\d+(?:\.\d+)?", line)
        if not match:
            return (1, 0, line.lower())
        return (0, float(match.group()), line.lower())

    # -------------------- TEXT MERGING --------------------
    def textMerging(self):
        frame = self.open_submenu()
        self._configure_grid(frame, columns=2, rows=8)

        self.mergeFiles = []

        ctk.CTkButton(
            frame,
            text="Back",
            command=self.close_submenu,
            width=BTN_WIDTH,
            height=BTN_HEIGHT,
            font=BUTTON_FONT,
        ).grid(row=0, column=0, padx=PADX, pady=PADY, sticky="w")

        ctk.CTkLabel(frame, text="Manual Source Text:", font=LABEL_FONT).grid(row=1, column=0, sticky="w")
        self.inputText = ctk.CTkTextbox(frame, height=130, font=FORMAT_TEXT_FONT, wrap="none")
        self.inputText.grid(row=2, column=0, columnspan=2, padx=PADX, pady=PADY, sticky="nsew")

        merge_controls = ctk.CTkFrame(frame, fg_color="transparent")
        merge_controls.grid(row=3, column=0, columnspan=2, padx=PADX, pady=PADY, sticky="ew")
        merge_controls.columnconfigure(1, weight=1)

        ctk.CTkButton(
            merge_controls,
            text="Select Files",
            command=self._select_merge_files,
            width=BTN_WIDTH,
            height=BTN_HEIGHT,
            font=BUTTON_FONT,
        ).grid(row=0, column=0, padx=(0, 6), pady=0, sticky="w")
        self.mergeFilesLabel = ctk.CTkLabel(merge_controls, text="No files selected", font=LABEL_FONT, anchor="w")
        self.mergeFilesLabel.grid(row=0, column=1, padx=(6, 0), pady=0, sticky="ew")

        options = ctk.CTkFrame(frame, fg_color="transparent")
        options.grid(row=4, column=0, columnspan=2, padx=PADX, pady=PADY, sticky="ew")
        options.columnconfigure((0, 1), weight=1)

        self.merge_mode_choice = ctk.CTkOptionMenu(
            options,
            values=["Append Sources", "Combine Lines"],
            font=BUTTON_FONT,
        )
        self.merge_mode_choice.grid(row=0, column=0, padx=(0, 6), pady=0, sticky="ew")
        self.merge_duplicate_choice = ctk.CTkOptionMenu(
            options,
            values=["Keep Duplicates", "Remove Duplicates"],
            font=BUTTON_FONT,
        )
        self.merge_duplicate_choice.grid(row=0, column=1, padx=(6, 0), pady=0, sticky="ew")

        ctk.CTkButton(
            frame,
            text="Merge",
            command=self._process_text_merging,
            height=BTN_HEIGHT,
            font=BUTTON_FONT,
        ).grid(row=5, column=0, columnspan=2, padx=PADX, pady=PADY, sticky="ew")

        ctk.CTkLabel(frame, text="Merged Output:", font=LABEL_FONT).grid(row=6, column=0, sticky="w")
        self.outputText = ctk.CTkTextbox(frame, height=220, font=FORMAT_TEXT_FONT, wrap="none")
        self.outputText.grid(row=7, column=0, columnspan=2, padx=PADX, pady=PADY, sticky="nsew")
        self.outputText.configure(state="disabled")

        output_buttons = ctk.CTkFrame(frame, fg_color="transparent")
        output_buttons.grid(row=8, column=0, columnspan=2, padx=PADX, pady=PADY, sticky="ew")
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

    def _select_merge_files(self):
        filenames = filedialog.askopenfilenames(filetypes=TEXT_FILETYPES)
        if not filenames:
            return

        self.mergeFiles = list(filenames)
        self.mergeFilesLabel.configure(text=f"{len(self.mergeFiles)} files selected")

    def _process_text_merging(self):
        sources = self._get_merge_sources()
        if not sources:
            self._show_merge_output("Add manual text or select files before merging.")
            return

        if self.merge_mode_choice.get() == "Combine Lines":
            merged_text = self._merge_sources_by_line(sources)
        else:
            merged_text = "\n\n".join(source for source in sources if source)

        if self.merge_duplicate_choice.get() == "Remove Duplicates":
            merged_text = self._remove_duplicate_lines(merged_text)

        self._show_merge_output(merged_text)

    def _get_merge_sources(self):
        sources = []
        manual_text = self.inputText.get("1.0", "end-1c")
        if manual_text.strip():
            sources.append(manual_text)

        for filename in self.mergeFiles:
            with open(filename, "r", encoding="utf-8") as text_file:
                sources.append(text_file.read())
        return sources

    def _merge_sources_by_line(self, sources):
        line_groups = [source.splitlines() for source in sources]
        max_lines = max((len(lines) for lines in line_groups), default=0)
        merged_lines = []

        # Interleave matching line numbers from each source to combine related rows together.
        for line_index in range(max_lines):
            for lines in line_groups:
                if line_index < len(lines):
                    merged_lines.append(lines[line_index])
        return "\n".join(merged_lines)

    def _remove_duplicate_lines(self, text):
        seen = set()
        unique_lines = []
        for line in text.splitlines():
            if line in seen:
                continue
            seen.add(line)
            unique_lines.append(line)
        return "\n".join(unique_lines)

    def _show_merge_output(self, text):
        self.outputText.configure(state="normal")
        self.outputText.delete("1.0", "end")
        self.outputText.insert("1.0", text)
        self.outputText.configure(state="disabled")

    # -------------------- TEXT NOISE REMOVAL --------------------
    def textNoiseRemoval(self):
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
        self.inputText = ctk.CTkTextbox(frame, height=170, font=FORMAT_TEXT_FONT, wrap="none")
        self.inputText.grid(row=2, column=0, columnspan=2, padx=PADX, pady=PADY, sticky="nsew")

        noise_controls = ctk.CTkFrame(frame, fg_color="transparent")
        noise_controls.grid(row=3, column=0, columnspan=2, padx=PADX, pady=PADY, sticky="ew")
        noise_controls.columnconfigure(1, weight=1)

        ctk.CTkButton(
            noise_controls,
            text="Select File",
            command=self.select_file,
            width=BTN_WIDTH,
            height=BTN_HEIGHT,
            font=BUTTON_FONT,
        ).grid(row=0, column=0, padx=(0, 6), pady=0, sticky="w")
        self.noise_choice = ctk.CTkOptionMenu(
            noise_controls,
            values=["Remove HTML Tags", "Remove Comments", "Filter Stopwords", "Remove All Noise"],
            font=BUTTON_FONT,
        )
        self.noise_choice.grid(row=0, column=1, padx=(6, 0), pady=0, sticky="ew")

        ctk.CTkButton(
            frame,
            text="Clean Text",
            command=self._process_text_noise_removal,
            height=BTN_HEIGHT,
            font=BUTTON_FONT,
        ).grid(row=4, column=0, columnspan=2, padx=PADX, pady=PADY, sticky="ew")

        ctk.CTkLabel(frame, text="Cleaned Output:", font=LABEL_FONT).grid(row=5, column=0, sticky="w")
        self.outputText = ctk.CTkTextbox(frame, height=220, font=FORMAT_TEXT_FONT, wrap="none")
        self.outputText.grid(row=6, column=0, columnspan=2, padx=PADX, pady=PADY, sticky="nsew")
        self.outputText.configure(state="disabled")

        output_buttons = ctk.CTkFrame(frame, fg_color="transparent")
        output_buttons.grid(row=7, column=0, columnspan=2, padx=PADX, pady=PADY, sticky="ew")
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

    def _process_text_noise_removal(self):
        text = self.inputText.get("1.0", "end-1c")
        choice = self.noise_choice.get()

        if choice == "Remove HTML Tags":
            cleaned_text = self._remove_html_tags(text)
        elif choice == "Remove Comments":
            cleaned_text = self._remove_comments(text)
        elif choice == "Filter Stopwords":
            cleaned_text = self._filter_stopwords(text)
        else:
            cleaned_text = self._remove_html_tags(text)
            cleaned_text = self._remove_comments(cleaned_text)
            cleaned_text = self._filter_stopwords(cleaned_text)

        self._show_noise_output(cleaned_text)

    def _remove_html_tags(self, text):
        text = re.sub(r"(?is)<(script|style).*?>.*?</\1>", "", text)
        text = re.sub(r"(?s)<[^>]+>", "", text)
        return html.unescape(text)

    def _remove_comments(self, text):
        text = re.sub(r"(?s)<!--.*?-->", "", text)
        text = re.sub(r"(?s)/\*.*?\*/", "", text)
        text = re.sub(r"(?m)^\s*#.*$", "", text)
        text = re.sub(r"(?m)//.*$", "", text)
        return text

    def _filter_stopwords(self, text):
        def replace_word(match):
            word = match.group(0)
            return "" if word.lower() in STOPWORDS else word

        text = re.sub(r"\b[A-Za-z]+\b", replace_word, text)
        text = re.sub(r"[ \t]{2,}", " ", text)
        text = re.sub(r"(?m)^[ \t]+|[ \t]+$", "", text)
        return text

    def _show_noise_output(self, text):
        self.outputText.configure(state="normal")
        self.outputText.delete("1.0", "end")
        self.outputText.insert("1.0", text)
        self.outputText.configure(state="disabled")

    # -------------------- TEXT ESCAPING --------------------
    def textEscaping(self):
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
        self.inputText = ctk.CTkTextbox(frame, height=170, font=FORMAT_TEXT_FONT, wrap="none")
        self.inputText.grid(row=2, column=0, columnspan=2, padx=PADX, pady=PADY, sticky="nsew")

        escape_controls = ctk.CTkFrame(frame, fg_color="transparent")
        escape_controls.grid(row=3, column=0, columnspan=2, padx=PADX, pady=PADY, sticky="ew")
        escape_controls.columnconfigure(1, weight=1)

        ctk.CTkButton(
            escape_controls,
            text="Select File",
            command=self.select_file,
            width=BTN_WIDTH,
            height=BTN_HEIGHT,
            font=BUTTON_FONT,
        ).grid(row=0, column=0, padx=(0, 6), pady=0, sticky="w")
        self.escape_choice = ctk.CTkOptionMenu(
            escape_controls,
            values=["Escape HTML", "Escape JSON", "Escape XML"],
            font=BUTTON_FONT,
        )
        self.escape_choice.grid(row=0, column=1, padx=(6, 0), pady=0, sticky="ew")

        ctk.CTkButton(
            frame,
            text="Escape Text",
            command=self._process_text_escaping,
            height=BTN_HEIGHT,
            font=BUTTON_FONT,
        ).grid(row=4, column=0, columnspan=2, padx=PADX, pady=PADY, sticky="ew")

        ctk.CTkLabel(frame, text="Escaped Output:", font=LABEL_FONT).grid(row=5, column=0, sticky="w")
        self.outputText = ctk.CTkTextbox(frame, height=220, font=FORMAT_TEXT_FONT, wrap="none")
        self.outputText.grid(row=6, column=0, columnspan=2, padx=PADX, pady=PADY, sticky="nsew")
        self.outputText.configure(state="disabled")

        output_buttons = ctk.CTkFrame(frame, fg_color="transparent")
        output_buttons.grid(row=7, column=0, columnspan=2, padx=PADX, pady=PADY, sticky="ew")
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

    def _process_text_escaping(self):
        text = self.inputText.get("1.0", "end-1c")
        choice = self.escape_choice.get()

        if choice == "Escape JSON":
            escaped_text = self._escape_json(text)
        elif choice == "Escape XML":
            escaped_text = self._escape_xml(text)
        else:
            escaped_text = self._escape_html(text)

        self._show_escape_output(escaped_text)

    def _escape_html(self, text):
        return html.escape(text, quote=True)

    def _escape_json(self, text):
        return json.dumps(text)[1:-1]

    def _escape_xml(self, text):
        return html.escape(text, quote=True).replace("&#x27;", "&apos;")

    def _show_escape_output(self, text):
        self.outputText.configure(state="normal")
        self.outputText.delete("1.0", "end")
        self.outputText.insert("1.0", text)
        self.outputText.configure(state="disabled")

    # -------------------- TEXT METRICS --------------------
    def textMetrics(self):
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

        ctk.CTkLabel(frame, text="Text A:", font=LABEL_FONT).grid(row=1, column=0, sticky="w")
        ctk.CTkLabel(frame, text="Text B:", font=LABEL_FONT).grid(row=1, column=1, sticky="w")
        self.metricsTextOne = ctk.CTkTextbox(frame, height=150, font=FORMAT_TEXT_FONT, wrap="none")
        self.metricsTextTwo = ctk.CTkTextbox(frame, height=150, font=FORMAT_TEXT_FONT, wrap="none")
        self.metricsTextOne.grid(row=2, column=0, padx=PADX, pady=PADY, sticky="nsew")
        self.metricsTextTwo.grid(row=2, column=1, padx=PADX, pady=PADY, sticky="nsew")

        file_buttons = ctk.CTkFrame(frame, fg_color="transparent")
        file_buttons.grid(row=3, column=0, columnspan=2, padx=PADX, pady=PADY, sticky="ew")
        file_buttons.columnconfigure((0, 1), weight=1)

        ctk.CTkButton(
            file_buttons,
            text="Select Text A",
            command=lambda: self._select_metrics_file(self.metricsTextOne),
            height=BTN_HEIGHT,
            font=BUTTON_FONT,
        ).grid(row=0, column=0, padx=(0, 6), pady=0, sticky="ew")
        ctk.CTkButton(
            file_buttons,
            text="Select Text B",
            command=lambda: self._select_metrics_file(self.metricsTextTwo),
            height=BTN_HEIGHT,
            font=BUTTON_FONT,
        ).grid(row=0, column=1, padx=(6, 0), pady=0, sticky="ew")

        metric_controls = ctk.CTkFrame(frame, fg_color="transparent")
        metric_controls.grid(row=4, column=0, columnspan=2, padx=PADX, pady=PADY, sticky="ew")
        metric_controls.columnconfigure(0, weight=1)

        self.metric_choice = ctk.CTkOptionMenu(
            metric_controls,
            values=["All Metrics", "Levenshtein Similarity", "Jaccard Similarity", "Text Entropy"],
            font=BUTTON_FONT,
        )
        self.metric_choice.grid(row=0, column=0, padx=(0, 6), pady=0, sticky="ew")

        ctk.CTkButton(
            metric_controls,
            text="Calculate",
            command=self._process_text_metrics,
            height=BTN_HEIGHT,
            font=BUTTON_FONT,
        ).grid(row=0, column=1, padx=(6, 0), pady=0, sticky="ew")

        ctk.CTkLabel(frame, text="Metrics Report:", font=LABEL_FONT).grid(row=5, column=0, sticky="w")
        self.outputText = ctk.CTkTextbox(frame, height=190, font=FORMAT_TEXT_FONT, wrap="none")
        self.outputText.grid(row=6, column=0, columnspan=2, padx=PADX, pady=PADY, sticky="nsew")
        self.outputText.configure(state="disabled")

        output_buttons = ctk.CTkFrame(frame, fg_color="transparent")
        output_buttons.grid(row=7, column=0, columnspan=2, padx=PADX, pady=PADY, sticky="ew")
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

    def _select_metrics_file(self, text_box):
        filename = filedialog.askopenfilename(filetypes=TEXT_FILETYPES)
        if not filename:
            return

        with open(filename, "r", encoding="utf-8") as text_file:
            content = text_file.read()

        text_box.delete("1.0", "end")
        text_box.insert("1.0", content)

    def _process_text_metrics(self):
        text_one = self.metricsTextOne.get("1.0", "end-1c")
        text_two = self.metricsTextTwo.get("1.0", "end-1c")
        choice = self.metric_choice.get()
        report_lines = []

        if choice in ("All Metrics", "Levenshtein Similarity"):
            distance, similarity = self._levenshtein_similarity(text_one, text_two)
            report_lines.append(f"Levenshtein distance: {distance}")
            report_lines.append(f"Levenshtein similarity: {similarity:.2%}")

        if choice in ("All Metrics", "Jaccard Similarity"):
            similarity = self._jaccard_similarity(text_one, text_two)
            report_lines.append(f"Jaccard similarity: {similarity:.2%}")

        if choice in ("All Metrics", "Text Entropy"):
            report_lines.append(f"Text A entropy: {self._text_entropy(text_one):.4f} bits/character")
            report_lines.append(f"Text B entropy: {self._text_entropy(text_two):.4f} bits/character")

        self._show_metrics_report("\n".join(report_lines))

    def _levenshtein_similarity(self, first_text, second_text):
        distance = self._levenshtein_distance(first_text, second_text)
        longest_length = max(len(first_text), len(second_text))
        similarity = 1.0 if longest_length == 0 else 1 - (distance / longest_length)
        return distance, similarity

    def _levenshtein_distance(self, first_text, second_text):
        if len(first_text) < len(second_text):
            first_text, second_text = second_text, first_text

        previous_row = list(range(len(second_text) + 1))
        for first_index, first_char in enumerate(first_text, start=1):
            current_row = [first_index]
            for second_index, second_char in enumerate(second_text, start=1):
                insert_cost = current_row[second_index - 1] + 1
                delete_cost = previous_row[second_index] + 1
                replace_cost = previous_row[second_index - 1] + (first_char != second_char)
                current_row.append(min(insert_cost, delete_cost, replace_cost))
            previous_row = current_row
        return previous_row[-1]

    def _jaccard_similarity(self, first_text, second_text):
        first_words = set(re.findall(r"\b\w+\b", first_text.lower()))
        second_words = set(re.findall(r"\b\w+\b", second_text.lower()))
        if not first_words and not second_words:
            return 1.0
        return len(first_words & second_words) / len(first_words | second_words)

    def _text_entropy(self, text):
        if not text:
            return 0.0

        # Shannon entropy measures how unpredictable the character distribution is.
        return -sum((text.count(char) / len(text)) * math.log2(text.count(char) / len(text)) for char in set(text))

    def _show_metrics_report(self, report):
        self.outputText.configure(state="normal")
        self.outputText.delete("1.0", "end")
        self.outputText.insert("1.0", report)
        self.outputText.configure(state="disabled")

    # -------------------- TEXT STYLING --------------------
    def textStyling(self):
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
        self.inputText = ctk.CTkTextbox(frame, height=170, font=FORMAT_TEXT_FONT, wrap="none")
        self.inputText.grid(row=2, column=0, columnspan=2, padx=PADX, pady=PADY, sticky="nsew")

        styling_controls = ctk.CTkFrame(frame, fg_color="transparent")
        styling_controls.grid(row=3, column=0, columnspan=2, padx=PADX, pady=PADY, sticky="ew")
        styling_controls.columnconfigure((1, 2), weight=1)

        ctk.CTkButton(
            styling_controls,
            text="Select File",
            command=self.select_file,
            width=BTN_WIDTH,
            height=BTN_HEIGHT,
            font=BUTTON_FONT,
        ).grid(row=0, column=0, padx=(0, 6), pady=0, sticky="w")
        self.styling_format_choice = ctk.CTkOptionMenu(
            styling_controls,
            values=["Markdown", "HTML", "BBCode"],
            font=BUTTON_FONT,
        )
        self.styling_format_choice.grid(row=0, column=1, padx=(6, 6), pady=0, sticky="ew")
        self.styling_style_choice = ctk.CTkOptionMenu(
            styling_controls,
            values=["Bold", "Italic", "Underline", "Heading", "Quote", "Code", "List"],
            font=BUTTON_FONT,
        )
        self.styling_style_choice.grid(row=0, column=2, padx=(6, 0), pady=0, sticky="ew")

        ctk.CTkButton(
            frame,
            text="Apply Styling",
            command=self._process_text_styling,
            height=BTN_HEIGHT,
            font=BUTTON_FONT,
        ).grid(row=4, column=0, columnspan=2, padx=PADX, pady=PADY, sticky="ew")

        ctk.CTkLabel(frame, text="Styled Output:", font=LABEL_FONT).grid(row=5, column=0, sticky="w")
        self.outputText = ctk.CTkTextbox(frame, height=220, font=FORMAT_TEXT_FONT, wrap="none")
        self.outputText.grid(row=6, column=0, columnspan=2, padx=PADX, pady=PADY, sticky="nsew")
        self.outputText.configure(state="disabled")

        output_buttons = ctk.CTkFrame(frame, fg_color="transparent")
        output_buttons.grid(row=7, column=0, columnspan=2, padx=PADX, pady=PADY, sticky="ew")
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

    def _process_text_styling(self):
        text = self.inputText.get("1.0", "end-1c")
        output_format = self.styling_format_choice.get()
        style = self.styling_style_choice.get()

        if output_format == "HTML":
            styled_text = self._style_as_html(text, style)
        elif output_format == "BBCode":
            styled_text = self._style_as_bbcode(text, style)
        else:
            styled_text = self._style_as_markdown(text, style)

        self._show_styling_output(styled_text)

    def _style_as_markdown(self, text, style):
        if style == "Bold":
            return f"**{text}**"
        if style == "Italic":
            return f"*{text}*"
        if style == "Underline":
            return f"<u>{html.escape(text)}</u>"
        if style == "Heading":
            return "\n".join(f"# {line}" if line else line for line in text.splitlines())
        if style == "Quote":
            return "\n".join(f"> {line}" if line else ">" for line in text.splitlines())
        if style == "Code":
            return f"```\n{text}\n```"
        return "\n".join(f"- {line}" if line else line for line in text.splitlines())

    def _style_as_html(self, text, style):
        escaped_text = html.escape(text)
        if style == "Bold":
            return f"<strong>{escaped_text}</strong>"
        if style == "Italic":
            return f"<em>{escaped_text}</em>"
        if style == "Underline":
            return f"<u>{escaped_text}</u>"
        if style == "Heading":
            return f"<h1>{escaped_text}</h1>"
        if style == "Quote":
            return f"<blockquote>{escaped_text}</blockquote>"
        if style == "Code":
            return f"<pre><code>{escaped_text}</code></pre>"
        items = "\n".join(f"  <li>{html.escape(line)}</li>" for line in text.splitlines() if line)
        return f"<ul>\n{items}\n</ul>"

    def _style_as_bbcode(self, text, style):
        if style == "Bold":
            return f"[b]{text}[/b]"
        if style == "Italic":
            return f"[i]{text}[/i]"
        if style == "Underline":
            return f"[u]{text}[/u]"
        if style == "Heading":
            return f"[size=150][b]{text}[/b][/size]"
        if style == "Quote":
            return f"[quote]{text}[/quote]"
        if style == "Code":
            return f"[code]{text}[/code]"
        items = "\n".join(f"[*]{line}" for line in text.splitlines() if line)
        return f"[list]\n{items}\n[/list]"

    def _show_styling_output(self, text):
        self.outputText.configure(state="normal")
        self.outputText.delete("1.0", "end")
        self.outputText.insert("1.0", text)
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
