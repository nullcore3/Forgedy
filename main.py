import customtkinter as ctk
from tkinter import filedialog
import random
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
        
        self.txtUtilsContainer = ctk.CTkFrame(self)
        self.txtUtilsContainer.columnconfigure((0, 1, 2, 3), weight=1)
        self.txtUtilsContainer.rowconfigure((0, 1, 2, 3, 4), weight=1)
        self.txtUtilsContainer.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")
        
        self.textConversionLink = ctk.CTkButton(self.txtUtilsContainer, text="Text Case Conversion", width=100, height=50, command=self.textCaseConversion)
        self.textConversionLink.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        self.textCountingLink = ctk.CTkButton(self.txtUtilsContainer, text="Text Counting", width=100, height=50, command=self.textCounting)
        self.textCountingLink.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
    
    def backToTxtUtils(self):
        """
        1. Hide the sub-menu options.
        2. Show the main text utilities options.
        """
        # Hide the text conversion utilities container
        for widget in self.txtConversionUtilsContainer.winfo_children():
            widget.grid_forget()
        self.txtConversionUtilsContainer.grid_forget()

        # Restore the main text utilities container
        self.txtUtilsContainer.configure(fg_color="transparent")  # Ensure the container is visible
        self.txtUtilsContainer.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

        # Re-grid the widgets in the main container
        self.textConversionLink.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.textCountingLink.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
    def selectFile(self):
        """
        Function to select a text file using a file dialog.
        """
        txt = filedialog.askopenfile(mode='r', filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        # If inputText exists, set its text to the content of the selected file
        if txt:
            content = txt.read()
            if hasattr(self, 'inputText'):
                self.inputText.delete(0, ctk.END)
                self.inputText.insert(0, content)  # Insert the content into the inputText widget

    
    def textCaseConversion(self):
        """
        1. Convert text to uppercase.
        2. Convert text to lowercase.
        3. Convert text to title case.
        4. Convert text to camelCase, snake_case, or kebab-case.
        """
        for widget in self.txtUtilsContainer.winfo_children():
            widget.grid_forget()

        self.txtUtilsContainer.configure(fg_color="transparent")
        self.txtUtilsContainer.place_forget()

        # Create a new container for text conversion utilities
        self.txtConversionUtilsContainer = ctk.CTkFrame(self)
        self.txtConversionUtilsContainer.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")
        self.txtConversionUtilsContainer.grid_rowconfigure(0, weight=1)

        # Add the back button to the new container
        self.backButton = ctk.CTkButton(self.txtConversionUtilsContainer, text="Back", width=50, height=25, command=self.backToTxtUtils)
        self.backButton.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Add other widgets to the new container
        self.selectTxtFile = ctk.CTkButton(self.txtConversionUtilsContainer, text="Select Text File", width=100, height=50, command=self.selectFile)
        self.selectTxtFile.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.orLabel = ctk.CTkLabel(self.txtConversionUtilsContainer, text="or", font=("Roboto", 24))
        self.orLabel.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        self.inputText = ctk.CTkEntry(self.txtConversionUtilsContainer, width=200)
        self.inputText.grid(row=1, column=2, padx=10, pady=10, sticky="ew")
        
        self.upperCaseButton = ctk.CTkButton(self.txtConversionUtilsContainer, text="UPPERCASE", width=100, height=50, command=self.convertToUppercase)
        self.upperCaseButton.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        self.lowerCaseButton = ctk.CTkButton(self.txtConversionUtilsContainer, text="lowercase", width=100, height=50, command=self.convertToLowercase)
        self.lowerCaseButton.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        self.titleCaseButton = ctk.CTkButton(self.txtConversionUtilsContainer, text="Title Case", width=100, height=50, command=self.convertToTitleCase)
        self.titleCaseButton.grid(row=2, column=2, padx=10, pady=10, sticky="ew")

        self.camelCaseButton = ctk.CTkButton(self.txtConversionUtilsContainer, text="camelCase", width=100, height=50, command=self.convertToCamelCase)
        self.camelCaseButton.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

        self.snakeCaseButton = ctk.CTkButton(self.txtConversionUtilsContainer, text="snake_case", width=100, height=50, command=self.convertToSnakeCase)
        self.snakeCaseButton.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

        self.kebabCaseButton = ctk.CTkButton(self.txtConversionUtilsContainer, text="kebab-case", width=100, height=50, command=self.convertToKebabCase)
        self.kebabCaseButton.grid(row=3, column=2, padx=10, pady=10, sticky="ew")

        self.pascalCaseButton = ctk.CTkButton(self.txtConversionUtilsContainer, text="PascalCase", width=100, height=50, command=self.convertToPascalCase)
        self.pascalCaseButton.grid(row=4, column=0, padx=10, pady=10, sticky="ew")
        
        self.flatCaseButton = ctk.CTkButton(self.txtConversionUtilsContainer, text="flatcase", width=100, height=50, command=self.convertToFlatCase)
        self.flatCaseButton.grid(row=4, column=1, padx=10, pady=10, sticky="ew")
        
        self.constanstCaseButton = ctk.CTkButton(self.txtConversionUtilsContainer, text="CONSTANT_CASE", width=100, height=50, command=self.convertToConstantCase)
        self.constanstCaseButton.grid(row=4, column=2, padx=10, pady=10, sticky="ew")

        self.outputLabel = ctk.CTkLabel(self.txtConversionUtilsContainer, text="")
        self.outputLabel.grid(row=5, column=0, columnspan=3, padx=10, pady=10, sticky="ew")
        
        self.copyButton = ctk.CTkButton(self.txtConversionUtilsContainer, text="Copy", width=50, height=35, command=self.copyToClipboard)
        self.copyButton.grid(row=5, column=3, padx=10, pady=10, sticky="ew")

    def convertToUppercase(self):
        input_text = self.inputText.get()
        self.outputLabel.configure(text=input_text.upper())

    def convertToLowercase(self):
        input_text = self.inputText.get()
        self.outputLabel.configure(text=input_text.lower())

    def convertToTitleCase(self):
        input_text = self.inputText.get()
        self.outputLabel.configure(text=input_text.title())

    def convertToCamelCase(self):
        input_text = self.inputText.get()
        words = input_text.split()
        camel_case = words[0].lower() + ''.join(word.capitalize() for word in words[1:])
        self.outputLabel.configure(text=camel_case)

    def convertToSnakeCase(self):
        input_text = self.inputText.get()
        snake_case = '_'.join(input_text.split()).lower()
        self.outputLabel.configure(text=snake_case)

    def convertToKebabCase(self):
        input_text = self.inputText.get()
        kebab_case = '-'.join(input_text.split()).lower()
        self.outputLabel.configure(text=kebab_case)
    
    def convertToPascalCase(self):
        input_text = self.inputText.get()
        words = input_text.split()
        pascal_case = ''.join(word.capitalize() for word in words)
        self.outputLabel.configure(text=pascal_case)
        
    def convertToFlatCase(self):
        input_text = self.inputText.get()
        flat_case = ''.join(input_text.split()).lower()
        self.outputLabel.configure(text=flat_case)
        
    def convertToConstantCase(self):
        input_text = self.inputText.get()
        constant_case = '_'.join(input_text.split()).upper()
        self.outputLabel.configure(text=constant_case) 
    
    def copyToClipboard(self):
        output_text = self.outputLabel.cget("text")
        clipboard.copy(output_text)
        
    def textCounting(self):
        """
        1. Count characters in a text file.
        2. Count words in a text file.
        3. Count lines in a text file.
        """        
        for widget in self.txtUtilsContainer.winfo_children():
            widget.grid_forget()

        self.txtUtilsContainer.configure(fg_color="transparent")
        self.txtUtilsContainer.place_forget()

        # Create a new container for text conversion utilities
        self.txtConversionUtilsContainer = ctk.CTkFrame(self)
        self.txtConversionUtilsContainer.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")
        self.txtConversionUtilsContainer.grid_rowconfigure(0, weight=1)

        # Add the back button to the new container
        self.backButton = ctk.CTkButton(self.txtConversionUtilsContainer, text="Back", width=50, height=25, command=self.backToTxtUtils)
        self.backButton.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Add other widgets to the new container
        self.selectTxtFile = ctk.CTkButton(self.txtConversionUtilsContainer, text="Select Text File", width=100, height=50, command=self.selectFile)
        self.selectTxtFile.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.orLabel = ctk.CTkLabel(self.txtConversionUtilsContainer, text="or", font=("Roboto", 24))
        self.orLabel.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        self.inputText = ctk.CTkEntry(self.txtConversionUtilsContainer, width=200)
        self.inputText.grid(row=1, column=2, padx=10, pady=10, sticky="ew")
        
        self.countCharactersButton = ctk.CTkButton(self.txtConversionUtilsContainer, text="Count Characters", width=100, height=50, command=self.countCharacters)
        self.countCharactersButton.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        
        self.countWordsButton = ctk.CTkButton(self.txtConversionUtilsContainer, text="Count Words", width=100, height=50, command=self.countWords)
        self.countWordsButton.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        
        self.countLinesButton = ctk.CTkButton(self.txtConversionUtilsContainer, text="Count Lines", width=100, height=50, command=self.countLines)
        self.countLinesButton.grid(row=2, column=2, padx=10, pady=10, sticky="ew")
        
        self.outputLabel = ctk.CTkLabel(self.txtConversionUtilsContainer, text="")
        self.outputLabel.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="ew")
        
        self.copyButton = ctk.CTkButton(self.txtConversionUtilsContainer, text="Copy", width=50, height=35, command=self.copyToClipboard)
        self.copyButton.grid(row=3, column=3, padx=10, pady=10, sticky="ew")
        
    def countCharacters(self):
        input_text = self.inputText.get()
        if not input_text:
            self.outputLabel.configure(text="Please enter some text or select a file.")
            return
        char_count = len(input_text)
        self.outputLabel.configure(text=f"Character Count: {char_count}")
    
    def countWords(self):
        input_text = self.inputText.get()
        if not input_text:
            self.outputLabel.configure(text="Please enter some text or select a file.")
            return
        word_count = len(input_text.split())
        self.outputLabel.configure(text=f"Word Count: {word_count}")
    
    def countLines(self):
        input_text = self.inputText.get()
        if not input_text:
            self.outputLabel.configure(text="Please enter some text or select a file.")
            return
        line_count = len(input_text.splitlines())
        self.outputLabel.configure(text=f"Line Count: {line_count}")
                
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