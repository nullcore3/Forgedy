import ctypes
import re
import sys
from tkinter import filedialog

import clipboard
import customtkinter as ctk

myappid = 'mycompany.myproduct.subproduct.version'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

PADX = 12
PADY = 8
BTN_HEIGHT = 40
CORNER = 12
THEME_PATH = "themes/breeze.json"

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
        ]

        for index, (text, command) in enumerate(menu_buttons):
            ctk.CTkButton(self.txtUtilsContainer, text=text, height=50, command=command).grid(
                row=0, column=index, padx=PADX, pady=PADY, sticky="ew"
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
        self.outputLabel = ctk.CTkLabel(parent, text="")
        self.outputLabel.grid(row=row, column=0, columnspan=3, padx=PADX, pady=PADY, sticky="ew")
        ctk.CTkButton(parent, text="Copy", command=self.copy_to_clipboard).grid(
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
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
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
        filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
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

        ctk.CTkButton(card, text="Back", command=self.close_submenu).grid(
            row=0, column=0, padx=PADX, pady=PADY, sticky="w"
        )

        ctk.CTkButton(card, text="Select File", command=self.select_file).grid(
            row=1, column=0, padx=PADX, pady=PADY, sticky="ew"
        )
        ctk.CTkButton(card, text="Save", command=self.save_input_text).grid(
            row=1, column=1, padx=PADX, pady=PADY, sticky="ew"
        )
        ctk.CTkLabel(card, text="or").grid(row=1, column=2, padx=5, pady=PADY)
        self.inputText = ctk.CTkEntry(card, placeholder_text="Enter text here...")
        self.inputText.grid(row=1, column=3, padx=PADX, pady=PADY, sticky="ew")

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

        ctk.CTkButton(card, text="Back", command=self.close_submenu).grid(
            row=0, column=0, padx=PADX, pady=PADY, sticky="w"
        )
        ctk.CTkButton(card, text="Select File", command=self.select_file).grid(
            row=1, column=0, padx=PADX, pady=PADY, sticky="ew"
        )
        ctk.CTkButton(card, text="Save", command=self.save_input_text).grid(
            row=1, column=1, padx=PADX, pady=PADY, sticky="ew"
        )
        ctk.CTkLabel(card, text="or").grid(row=1, column=2, padx=5, pady=PADY)
        self.inputText = ctk.CTkTextbox(card)
        self.inputText.grid(row=1, column=3, padx=PADX, pady=PADY, sticky="ew")

        counters = [
            ("Count Characters", lambda t: len(t)),
            ("Count Words", lambda t: len(t.split())),
            ("Count Lines", lambda t: len(t.splitlines())),
        ]

        for index, (label, func) in enumerate(counters):
            ctk.CTkButton(
                card,
                text=label,
                command=lambda f=func: self.show_output(f(self.get_input_text())),
            ).grid(row=2, column=index, padx=PADX, pady=PADY, sticky="ew")

        self._configure_output_copy(card, row=3)

    def text_manipulation(self):
        frame = self.open_submenu()
        self._configure_grid(frame, columns=2, rows=8)

        ctk.CTkButton(frame, text="Back", command=self.close_submenu).grid(
            row=0, column=0, padx=PADX, pady=PADY, sticky="w"
        )

        ctk.CTkLabel(frame, text="Input Text:").grid(row=1, column=0, sticky="w")
        self.inputText = ctk.CTkTextbox(frame, height=150)
        self.inputText.grid(row=2, column=0, columnspan=2, padx=PADX, pady=PADY, sticky="nsew")

        ctk.CTkButton(frame, text="Select File", command=self.select_file).grid(
            row=3, column=0, padx=PADX, pady=PADY, sticky="ew"
        )
        ctk.CTkButton(frame, text="Save Output", command=self.save_output_text).grid(
            row=3, column=1, padx=PADX, pady=PADY, sticky="ew"
        )

        ctk.CTkLabel(frame, text="Choose Operation:").grid(row=4, column=0, sticky="w")
        self.operation_choice = ctk.CTkOptionMenu(
            frame,
            values=["Find & Replace", "Remove Whitespace", "Extract Pattern"],
        )
        self.operation_choice.grid(row=5, column=0, padx=PADX, pady=PADY, sticky="ew")

        self.patternFrame = ctk.CTkFrame(frame)
        self.patternFrame.grid(row=6, column=0, columnspan=2, sticky="ew", padx=PADX, pady=PADY)

        self.findEntry = ctk.CTkEntry(self.patternFrame, placeholder_text="Find")
        self.replaceEntry = ctk.CTkEntry(self.patternFrame, placeholder_text="Replace")
        self.regexEntry = ctk.CTkEntry(self.patternFrame, placeholder_text="Regex")
        self.regexExplanation = ctk.CTkLabel(self.patternFrame, text="Regex example: \\S+@\\S+")

        self.operation_handlers = {
            "Find & Replace": self._find_and_replace,
            "Remove Whitespace": self._remove_whitespace,
            "Extract Pattern": self._extract_pattern,
        }

        self.operation_choice.configure(command=self._update_pattern_fields)
        self._update_pattern_fields("Find & Replace")

        ctk.CTkLabel(frame, text="Output:").grid(row=7, column=0, sticky="w")
        self.outputText = ctk.CTkTextbox(frame, height=150)
        self.outputText.grid(row=8, column=0, columnspan=2, padx=PADX, pady=PADY, sticky="nsew")
        self.outputText.configure(state="disabled")

        ctk.CTkButton(
            frame,
            text="Copy Output",
            command=lambda: clipboard.copy(self.outputText.get("1.0", "end").strip()),
        ).grid(row=9, column=0, columnspan=2, padx=PADX, pady=PADY, sticky="ew")

        ctk.CTkButton(frame, text="Run", command=self._process_text_operation).grid(
            row=10, column=0, columnspan=2, padx=PADX, pady=PADY, sticky="ew"
        )

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
