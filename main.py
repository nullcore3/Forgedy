import customtkinter as ctk
from tkinter import filedialog
import random
import re
import clipboard
import ctypes

myappid = 'mycompany.myproduct.subproduct.version' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)




PADX = 12
PADY = 8
BTN_HEIGHT = 40
CORNER = 12

ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("themes/breeze.json")
# ctk.set_default_color_theme(f"themes/{random.choice(['autumn', 'breeze', 'carrot', 'cherry', 'coffee', 'lavender', 'marsh', 'metal', 'midnight', 'orange', 'patina', 'pink', 'red', 'rime', 'rose', 'sky', 'violet', 'yellow'])}.json")

# TODO: When you press 'cntrl + alt + t' it should open the Forgedy application. This should be an option set in the installer.

class seperatorLine(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master, height=4, corner_radius=5)
        self.line = ctk.CTkFrame(self, width=780, height=4, corner_radius=5)
        self.line.grid(row=0, column=0, columnspan=5, padx=0, pady=0, sticky="nsew")
        self.line.grid_propagate(False)
        
class TxtUtils(ctk.CTkScrollableFrame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self._parent_canvas.bind("<ButtonPress-2>", self._start_middle_scroll)
        self._parent_canvas.bind("<B2-Motion>", self._middle_scroll)

        # --- MAIN MENU ---
        self.txtUtilsContainer = ctk.CTkFrame(self)
        self.txtUtilsContainer.columnconfigure((0, 1, 2, 3), weight=1)
        self.txtUtilsContainer.grid(row=0, column=0, columnspan=5, padx=PADX, pady=PADY, sticky="nsew")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # Main buttons
        menu_buttons = [
            ("Text Case Conversion", self.textCaseConversion),
            ("Text Counting", self.textCounting),
            ("Text Manipulation", self.textManipulation)
        ]

        for i, (text, command) in enumerate(menu_buttons):
            ctk.CTkButton(self.txtUtilsContainer, text=text, height=50,
                          command=command).grid(row=0, column=i, padx=PADX, pady=PADY, sticky="ew")

        # Submenu container (hidden unless opened)
        self.currentSubmenu = None

    # -------------------- UNIVERSAL SUBMENU HANDLERS --------------------
    def _start_middle_scroll(self, event):
        self._parent_canvas.scan_mark(event.x, event.y)

    def _middle_scroll(self, event):
        self._parent_canvas.scan_dragto(event.x, event.y, gain=1)

    def copyToClipboard(self):
        if hasattr(self, "outputLabel"):
            text = self.outputLabel.cget("text")
            clipboard.copy(text)

    def get_input_text(self):
        """Handles Entry or Text widget input extraction."""
        if isinstance(self.inputText, ctk.CTkEntry):
            return self.inputText.get()
        else:  # CTkTextbox
            return self.inputText.get("1.0", "end").strip()

    def selectFile(self):
        filename = filedialog.askopenfilename(filetypes=[
            ("Text files", "*.txt"),
            ("All files", "*.*")
        ])

        if filename:
            with open(filename, 'r', encoding='utf-8') as txt:
                content = txt.read()
            if hasattr(self, "inputText"):
                try:
                    self.inputText.delete(0, ctk.END)
                    self.inputText.insert(0, content)
                except:
                    self.inputText.delete("1.0", "end")
                    self.inputText.insert("1.0", content)

    def openSubmenu(self):
        self.txtUtilsContainer.grid_forget()
        if self.currentSubmenu:
            self.currentSubmenu.destroy()

        self.currentSubmenu = ctk.CTkFrame(self)
        self.currentSubmenu.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.currentSubmenu.rowconfigure(99, weight=1)
        self.currentSubmenu.columnconfigure((0, 1, 2, 3), weight=1)
        return self.currentSubmenu

    def closeSubmenu(self):
        if self.currentSubmenu:
            self.currentSubmenu.destroy()
            self.currentSubmenu = None
        self.txtUtilsContainer.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    # -------------------- TEXT CASE CONVERSION --------------------
    def textCaseConversion(self):
        frame = self.openSubmenu()

        main = ctk.CTkFrame(frame, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=20, pady=20)

        card = ctk.CTkFrame(
            main,
            corner_radius=16
        )

        card.pack(fill="both", expand=True)

        for col in range(4):
            frame.columnconfigure(col, weight=1)
        for row in range(10):
            frame.rowconfigure(row, weight=1)

        ctk.CTkButton(card, text="Back", command=self.closeSubmenu)\
            .grid(row=0, column=0, padx=PADX, pady=PADY, sticky="w")

        # Input
        ctk.CTkButton(card, text="Select File", command=self.selectFile)\
            .grid(row=1, column=0, padx=PADX, pady=PADY, sticky="ew")
        ctk.CTkLabel(card, text="or").grid(row=1, column=1, padx=5, pady=PADY)
        self.inputText = ctk.CTkEntry(card, placeholder_text="Enter text here...")
        self.inputText.grid(row=1, column=2, columnspan=2, padx=PADX, pady=PADY, sticky="ew")

        # Conversion buttons
        conversions = [
            ("UPPERCASE", lambda t: t.upper()),
            ("lowercase", lambda t: t.lower()),
            ("Title Case", lambda t: t.title()),
            ("camelCase", self.toCamel),
            ("snake_case", lambda t: "_".join(t.split()).lower()),
            ("kebab-case", lambda t: "-".join(t.split()).lower()),
            ("PascalCase", lambda t: "".join(w.capitalize() for w in t.split())),
            ("flatcase", lambda t: "".join(t.split()).lower()),
            ("CONSTANT_CASE", lambda t: "_".join(t.split()).upper())
        ]

        for i, (label, func) in enumerate(conversions):
            ctk.CTkButton(
                card, text=label,
                command=lambda f=func: self.showOutput(f(self.get_input_text()))
            ).grid(row=2 + i // 3, column=i % 3, padx=PADX, pady=PADY, sticky="ew")

        # Output
        self.outputLabel = ctk.CTkLabel(card, text="")
        self.outputLabel.grid(row=5, column=0, columnspan=3, padx=PADX, pady=PADY, sticky="ew")
        ctk.CTkButton(card, text="Copy", command=self.copyToClipboard)\
            .grid(row=5, column=3, padx=PADX, pady=PADY, sticky="ew")

    def toCamel(self, text):
        words = text.split()
        return words[0].lower() + "".join(w.capitalize() for w in words[1:])

    def showOutput(self, text):
        self.outputLabel.configure(text=text)

    # -------------------- TEXT COUNTING --------------------
    def textCounting(self):
        frame = self.openSubmenu()
        for col in range(4):
            frame.columnconfigure(col, weight=1)
        for row in range(10):
            frame.rowconfigure(row, weight=1)

        main = ctk.CTkFrame(frame, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=20, pady=PADY)

        card = ctk.CTkFrame(
            main,
            corner_radius=16
        )
        card.pack(fill="both", expand=True)

        ctk.CTkButton(card, text="Back", command=self.closeSubmenu)\
            .grid(row=0, column=0, padx=PADX, pady=PADY, sticky="w")
        ctk.CTkButton(card, text="Select File", command=self.selectFile)\
            .grid(row=1, column=0, padx=PADX, pady=PADY, sticky="ew")
        ctk.CTkLabel(card, text="or").grid(row=1, column=1, padx=5, pady=PADY)
        self.inputText = ctk.CTkTextbox(card)
        self.inputText.grid(row=1, column=2, columnspan=2, padx=PADX, pady=PADY, sticky="ew")

        counters = [
            ("Count Characters", lambda t: len(t)),
            ("Count Words", lambda t: len(t.split())),
            ("Count Lines", lambda t: len(t.splitlines()))
        ]

        for i, (label, func) in enumerate(counters):
            ctk.CTkButton(
                card, text=label,
                command=lambda f=func: self.showOutput(f(self.get_input_text()))
            ).grid(row=2, column=i, padx=PADX, pady=PADY, sticky="ew")

        self.outputLabel = ctk.CTkLabel(card, text="")
        self.outputLabel.grid(row=3, column=0, columnspan=3, padx=PADX, pady=PADY, sticky="ew")
        ctk.CTkButton(card, text="Copy", command=self.copyToClipboard)\
            .grid(row=3, column=3, padx=PADX, pady=PADY, sticky="ew")

    # -------------------- TEXT MANIPULATION --------------------
    def textManipulation(self):
        frame = self.openSubmenu()
        for col in range(2):
            frame.columnconfigure(col, weight=1)
        frame.rowconfigure(7, weight=1)

        ctk.CTkButton(frame, text="Back", command=self.closeSubmenu)\
            .grid(row=0, column=0, padx=PADX, pady=PADY, sticky="w")

        # Input
        ctk.CTkLabel(frame, text="Input Text:").grid(row=1, column=0, sticky="w")
        self.inputText = ctk.CTkTextbox(frame, height=150, placeholder_text="Enter text here...")
        self.inputText.grid(row=2, column=0, columnspan=2, padx=PADX, pady=PADY, sticky="nsew")

        # Operation
        ctk.CTkLabel(frame, text="Choose Operation:").grid(row=3, column=0, sticky="w")
        self.operationChoice = ctk.CTkOptionMenu(frame,
            values=["Find & Replace", "Remove Whitespace", "Extract Pattern"]
        )
        self.operationChoice.grid(row=4, column=0, padx=PADX, pady=PADY, sticky="ew")

        # Pattern frame
        self.patternFrame = ctk.CTkFrame(frame)
        self.patternFrame.grid(row=5, column=0, columnspan=2, sticky="ew", padx=PADX, pady=PADY)

        self.findEntry = ctk.CTkEntry(self.patternFrame, placeholder_text="Find")
        self.replaceEntry = ctk.CTkEntry(self.patternFrame, placeholder_text="Replace")
        self.regexEntry = ctk.CTkEntry(self.patternFrame, placeholder_text="Regex")
        self.regexExplanation = ctk.CTkLabel(self.patternFrame, text="Regex example: \\S+@\\S+")

        def updateFields(choice):
            for w in self.patternFrame.winfo_children():
                w.grid_forget()
            if choice == "Find & Replace":
                self.findEntry.grid(row=0, column=0, padx=PADX, pady=PADY)
                self.replaceEntry.grid(row=0, column=1, padx=PADX, pady=PADY)
            elif choice == "Extract Pattern":
                self.regexEntry.grid(row=0, column=0, padx=PADX, pady=PADY)
                self.regexExplanation.grid(row=1, column=0, padx=PADX, pady=PADY)

        self.operationChoice.configure(command=updateFields)
        updateFields("Find & Replace")

        # Output
        ctk.CTkLabel(frame, text="Output:").grid(row=6, column=0, sticky="w")
        self.outputText = ctk.CTkTextbox(frame, height=150)
        self.outputText.grid(row=7, column=0, columnspan=2, padx=PADX, pady=PADY, sticky="nsew")

        ctk.CTkButton(frame, text="Copy Output",
                      command=lambda: clipboard.copy(self.outputText.get("1.0", "end").strip()))\
            .grid(row=7, column=1, padx=PADX, pady=PADY, sticky="ew")

        def process():
            text = self.inputText.get("1.0", "end").strip()
            op = self.operationChoice.get()

            if op == "Find & Replace":
                result = text.replace(self.findEntry.get(), self.replaceEntry.get())
            elif op == "Remove Whitespace":
                result = "".join(text.split())
            else:
                matches = re.findall(self.regexEntry.get(), text)
                result = "\n".join(matches) if matches else "No matches found."

            self.outputText.delete("1.0", "end")
            self.outputText.insert("1.0", result)

        ctk.CTkButton(frame, text="Run", command=process)\
            .grid(row=8, column=0, columnspan=2, padx=PADX, pady=PADY, sticky="ew")    
            
class Forgedy(ctk.CTk):
    def __init__(self): 
        super().__init__()
        self.title("Forgedy")
        self.geometry("800x600")
        self.columnconfigure((0, 1, 2, 3), weight=1)
        self.rowconfigure(2, weight=1)
        
        self.imgUtils = ctk.CTkButton(self, text="Image Utilities", width=100, height=50)
        self.imgUtils.grid(row=0, column=0, padx=PADX, pady=PADY, sticky="ew")
        
        self.txtUtilsButton = ctk.CTkButton(self, text="Text Utilities", width=100, height=50, command=self.openTxtUtils)
        self.txtUtilsButton.grid(row=0, column=1, padx=PADX, pady=PADY, sticky="ew")
        
        self.audioUtils = ctk.CTkButton(self, text="Audio Utilities", width=100, height=50)
        self.audioUtils.grid(row=0, column=2, padx=PADX, pady=PADY, sticky="ew")
        
        self.videoUtils = ctk.CTkButton(self, text="Video Utilities", width=100, height=50)
        self.videoUtils.grid(row=0, column=3, padx=PADX, pady=PADY, sticky="ew")
        
        self.seperatorLineMainScreen = seperatorLine(self)
        self.seperatorLineMainScreen.grid(row=1, column=0, columnspan=5, padx=PADX, pady=PADY, sticky="ew")

    def openTxtUtils(self):
        txt_utils = TxtUtils(self)
        txt_utils.grid(row=2, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

        
if __name__ == "__main__":
    app = Forgedy()
    app.iconbitmap("icon-no-bg.ico")
    app.mainloop()
