from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QTextEdit, 
                             QVBoxLayout, QHBoxLayout, QGridLayout, QMessageBox)
from PyQt5.QtCore import Qt
from utilities.list_of_ingredients_handler import ListfIngredientsHandler
from utilities.styles import load_cookbook_style

class IngredientListWindow(QWidget):
    def __init__(self, second_window):
        """
        When the App runs, this is how this window is created from the start by creatigns its User Interface
        
        Class that is calling to handle the convertion
        class ListfIngredientsHandler
            def main_function(self, ing_list: str):
        
        This Window is for loading a list of ingredients:
        
        """
        super().__init__()
        
        self.second_window = second_window  # keep reference to the previous window
        
        self.setWindowTitle("Load Ingredient List")

        load_cookbook_style(self)
        
        self.resize(800, 400)
        
        #---- Objects -----
        # Label and Text Box
        self.ing_list_label = QLabel("Paste List of Ingredients bellow in this format: (Quantity, Unit, Name) e.g. 2 cups warm milk")
        self.ing_list_line = QTextEdit()
        
        # Buttons
        self.rules_button = QPushButton("?")
        self.rules_button.setMinimumWidth(20)
        self.rules_button.setMaximumWidth(25)
        self.rules_button.clicked.connect(self.display_rules)
        
        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.add_ingredient_list)
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.cancel_window)
        
        #---- Layout -----
        
        # Row 1
        self.row1 = QHBoxLayout()
        self.row1.addWidget(self.ing_list_label)
        
        # Row 2
        self.row2 = QHBoxLayout()
        self.row2.addWidget(self.ing_list_line)
        
        # Row 3
        self.row3 = QGridLayout()
        self.row3.addWidget(self.add_button, 0, 0)
        self.row3.addWidget(self.cancel_button, 0, 1)
        self.row3.addWidget(self.rules_button, 0, 2, Qt.AlignBottom | Qt.AlignRight)
        
        # Master Layout
        self.master_layout = QVBoxLayout()
        
        self.master_layout.addLayout(self.row1)
        self.master_layout.addLayout(self.row2)
        self.master_layout.addLayout(self.row3)
        
        self.setLayout(self.master_layout)
        
    def add_ingredient_list(self):
        ing_list_string = self.ing_list_line.toPlainText() # Reference the text containing the ingredients
        ing_list_handler = ListfIngredientsHandler() # Reference the Handler class

        try:
            ing_list_list = ing_list_handler.main_function(ing_list_string) # Calls the Handler's main function to convert the string into 
                                                       #a lsit of ingredients
            print(ing_list_list)
            for ing in ing_list_list:    
                new_dic = {} 
                # Stores inside a dictionary
                new_dic["i_quantity"] = ing[0]
                new_dic["i_unit"] = ing[1]
                new_dic["i_name"] = ing[2]
                new_dic["i_category"] = ""

                self.second_window.load_ing_data(new_dic) # Calls the function from CreateWindow to add the new ingredient
        
            self.ing_list_line.clear()
            self.hide()
        except TypeError:
            QMessageBox.warning(self, "Error converting the list", "Please add it correctly")

        
    def cancel_window(self):
        self.ing_list_line.clear()
        self.hide()
        
    def display_rules(self):
        message_title = "List Rules"
        message_information = """

        Please add the list of ingredients in this format: (Quantity, Unit, Name)
        e.g.        2 cups warm milk
               1/2 teaspoon salt
               3 large eggs
               1 tablespoon sugar
               2 1/2 cups all-purpose flour
               1 tablespoon baking powder
               1/2 cup unsalted butter, melted
               """
        QMessageBox.information(self, message_title, message_information, QMessageBox.Ok)