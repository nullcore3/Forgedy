import customtkinter as ctk
from tkinter import filedialog
import random
import re
import clipboard

ctk.set_default_color_theme(f"themes/{random.choice(['autumn', 'breeze', 'carrot', 'cherry', 'coffee', 'lavender', 'marsh', 'metal', 'midnight', 'orange', 'patina', 'pink', 'red', 'rime', 'rose', 'sky', 'violet', 'yellow'])}.json")

# TODO: When you press 'cntrl + alt + t' it should open the Utoolities application. This should be an option set in the installer.

class seperatorLine(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master)
        self.frame = ctk.CTkFrame(master)
        self.frame.grid(row=1, column=0, columnspan=5, padx=10, pady=10, sticky="ew")
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.configure(fg_color="transparent")
        self.line = ctk.CTkFrame(self.frame, width=780, height=4, corner_radius=5)
        self.line.grid(row=0, column=0, columnspan=5, padx=10, pady=0, sticky="nsew")
        self.frame.columnconfigure(0, weight=1)  # Make the column responsive
        self.line.grid_propagate(False)
        
    
class TxtUtils(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        # --- MAIN MENU ---
        self.txtUtilsContainer = ctk.CTkFrame(self)
        self.txtUtilsContainer.columnconfigure((0, 1, 2, 3), weight=1)
        self.txtUtilsContainer.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Main buttons
        menu_buttons = [
            ("Text Case Conversion", self.textCaseConversion),
            ("Text Counting", self.textCounting),
            ("Text Manipulation", self.textManipulation)
        ]

        for i, (text, command) in enumerate(menu_buttons):
            ctk.CTkButton(self.txtUtilsContainer, text=text, height=50,
                          command=command).grid(row=0, column=i, padx=10, pady=10, sticky="ew")

        # Submenu container (hidden unless opened)
        self.currentSubmenu = None

    # -----------------------------------------------------------
    # UNIVERSAL SUBMENU HANDLERS
    # -----------------------------------------------------------
    
    def selectFile(self):
        """Open a file dialog and load file contents into inputText if it exists."""
        txt = filedialog.askopenfile(mode='r', filetypes=[
            ("Text files", "*.txt"),
            ("All files", "*.*")
        ])

        if txt:
            content = txt.read()

            # inputText can be Entry or Textbox depending on the submenu
            if hasattr(self, "inputText"):
                try:
                    # For Entry widgets
                    self.inputText.delete(0, ctk.END)
                    self.inputText.insert(0, content)
                except:
                    # For Textboxes
                    self.inputText.delete("1.0", "end")
                    self.inputText.insert("1.0", content)

    def openSubmenu(self):
        """Hides main menu and creates a new submenu container."""
        self.txtUtilsContainer.grid_forget()

        # Destroy previous submenu
        if self.currentSubmenu is not None:
            self.currentSubmenu.destroy()

        self.currentSubmenu = ctk.CTkFrame(self)
        self.currentSubmenu.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        return self.currentSubmenu

    def closeSubmenu(self):
        """Return back to main menu."""
        if self.currentSubmenu:
            self.currentSubmenu.destroy()
            self.currentSubmenu = None

        self.txtUtilsContainer.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    # -----------------------------------------------------------
    # TEXT CASE CONVERSION MENU
    # -----------------------------------------------------------

    def textCaseConversion(self):
        frame = self.openSubmenu()

        ctk.CTkButton(frame, text="Back", command=self.closeSubmenu).grid(
            row=0, column=0, padx=10, pady=10, sticky="w"
        )

        # Input row
        ctk.CTkButton(frame, text="Select File", command=self.selectFile)\
            .grid(row=1, column=0, padx=10, pady=10)

        ctk.CTkLabel(frame, text="or").grid(row=1, column=1)
        self.inputText = ctk.CTkEntry(frame)
        self.inputText.grid(row=1, column=2, padx=10, pady=10, sticky="ew")

        # List of conversion buttons
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

        # Auto-generate grid of conversion buttons
        for i, (label, func) in enumerate(conversions, start=2):
            ctk.CTkButton(
                frame, text=label,
                command=lambda f=func: self.showOutput(f(self.inputText.get()))
            ).grid(row=i//3 + 2, column=i % 3, padx=10, pady=10, sticky="ew")

        # Output
        self.outputLabel = ctk.CTkLabel(frame, text="")
        self.outputLabel.grid(row=5, column=0, columnspan=3, padx=10, pady=10)
        ctk.CTkButton(frame, text="Copy", command=self.copyToClipboard)\
            .grid(row=5, column=3, padx=10, pady=10)

    # Helpers for conversions
    def toCamel(self, text):
        words = text.split()
        return words[0].lower() + "".join(w.capitalize() for w in words[1:])

    def showOutput(self, text):
        self.outputLabel.configure(text=text)

    # -----------------------------------------------------------
    # TEXT COUNTING MENU
    # -----------------------------------------------------------

    def textCounting(self):
        frame = self.openSubmenu()
        ctk.CTkButton(frame, text="Back", command=self.closeSubmenu)\
            .grid(row=0, column=0, padx=10, pady=10)

        # Input
        ctk.CTkButton(frame, text="Select File", command=self.selectFile)\
            .grid(row=1, column=0, padx=10, pady=10)

        ctk.CTkLabel(frame, text="or").grid(row=1, column=1)
        self.inputText = ctk.CTkEntry(frame)
        self.inputText.grid(row=1, column=2, padx=10, pady=10, sticky="ew")

        # Counting operations
        counters = [
            ("Count Characters", lambda t: len(t)),
            ("Count Words", lambda t: len(t.split())),
            ("Count Lines", lambda t: len(t.splitlines()))
        ]

        for i, (label, func) in enumerate(counters):
            ctk.CTkButton(
                frame, text=label,
                command=lambda f=func: self.showOutput(f(self.inputText.get()))
            ).grid(row=2, column=i, padx=10, pady=10)

        self.outputLabel = ctk.CTkLabel(frame, text="")
        self.outputLabel.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

        ctk.CTkButton(frame, text="Copy", command=self.copyToClipboard)\
            .grid(row=3, column=3, padx=10, pady=10)

    # -----------------------------------------------------------
    # TEXT MANIPULATION MENU
    # -----------------------------------------------------------

    def textManipulation(self):
        frame = self.openSubmenu()

        ctk.CTkButton(frame, text="Back", command=self.closeSubmenu)\
            .grid(row=0, column=0, padx=10, pady=10)

        # Input
        ctk.CTkLabel(frame, text="Input Text:").grid(row=1, column=0, sticky="w")
        self.inputText = ctk.CTkTextbox(frame, height=150)
        self.inputText.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

        # Operation menu
        ctk.CTkLabel(frame, text="Choose Operation:").grid(row=3, column=0, sticky="w")
        self.operationChoice = ctk.CTkOptionMenu(frame,
            values=["Find & Replace", "Remove Whitespace", "Extract Pattern"]
        )
        self.operationChoice.grid(row=4, column=0, padx=10, pady=5, sticky="ew")

        # Dynamic pattern area
        self.patternFrame = ctk.CTkFrame(frame)
        self.patternFrame.grid(row=5, column=0, sticky="ew")

        # Fields
        self.findEntry = ctk.CTkEntry(self.patternFrame, placeholder_text="Find")
        self.replaceEntry = ctk.CTkEntry(self.patternFrame, placeholder_text="Replace")
        self.regexEntry = ctk.CTkEntry(self.patternFrame, placeholder_text="Regex")
        self.regexExplanation = ctk.CTkLabel(self.patternFrame, text="Regex example: \\S+@\\S+")

        def updateFields(choice):
            for w in self.patternFrame.winfo_children():
                w.grid_forget()

            if choice == "Find & Replace":
                self.findEntry.grid(row=0, column=0, padx=5)
                self.replaceEntry.grid(row=0, column=1, padx=5)

            elif choice == "Extract Pattern":
                self.regexEntry.grid(row=0, column=0, padx=5)
                self.regexExplanation.grid(row=1, column=0)

        self.operationChoice.configure(command=updateFields)
        updateFields("Find & Replace")

        # Output
        ctk.CTkLabel(frame, text="Output:").grid(row=6, column=0, sticky="w")
        self.outputText = ctk.CTkTextbox(frame, height=150)
        self.outputText.grid(row=7, column=0, padx=10, pady=5, sticky="ew")

        ctk.CTkButton(frame, text="Copy Output",
                      command=lambda: clipboard.copy(self.outputText.get("1.0", "end").strip()))\
            .grid(row=7, column=1, padx=10)

        def process():
            text = self.inputText.get("1.0", "end").strip()
            op = self.operationChoice.get()

            if op == "Find & Replace":
                result = text.replace(self.findEntry.get(), self.replaceEntry.get())

            elif op == "Remove Whitespace":
                result = "".join(text.split())

            else:  # Extract Pattern
                matches = re.findall(self.regexEntry.get(), text)
                result = "\n".join(matches) if matches else "No matches found."

            self.outputText.delete("1.0", "end")
            self.outputText.insert("1.0", result)

        ctk.CTkButton(frame, text="Run", command=process)\
            .grid(row=8, column=0, padx=10, pady=10, sticky="ew")

            
            
        
            
class Utoolities(ctk.CTk):
    def __init__(self): 
        super().__init__()
        self.title("Utoolities")
        self.geometry("800x600")
        self.columnconfigure((0, 1, 2, 3), weight=1)
        
        self.imgUtils = ctk.CTkButton(self, text="Image Utilities", width=100, height=50)
        self.imgUtils.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        self.txtUtilsButton = ctk.CTkButton(self, text="Text Utilities", width=100, height=50, command=self.openTxtUtils)
        self.txtUtilsButton.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        self.audioUtils = ctk.CTkButton(self, text="Audio Utilities", width=100, height=50)
        self.audioUtils.grid(row=0, column=2, padx=10, pady=10, sticky="ew")
        
        self.videoUtils = ctk.CTkButton(self, text="Video Utilities", width=100, height=50)
        self.videoUtils.grid(row=0, column=3, padx=10, pady=10, sticky="ew")
        
        self.seperatorLineMainScreen = seperatorLine(self)

    def openTxtUtils(self):
        # Create an instance of TxtUtils and display it
        txt_utils = TxtUtils(self)
        txt_utils.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")
        
if __name__ == "__main__":
    app = Utoolities()
    app.mainloop()