from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QComboBox, QPushButton, QVBoxLayout, 
                             QGridLayout, QSizePolicy)

class IngredientWindow(QWidget):
    def __init__(self, second_window):
        """
        When the App runs, this is how this window is created from the start by creatigns its User Interface
        
        This Window is for the an Individual ingredient where you can type.:
        
        - Qtd: Quantity of the ingredient
        - Unit: Type of Measurement for this ignredient
        - Name: Name of the ingredient
        - Category: Theres a lsit of category you can choose to give to this specific ingredient
        
        When it has all of its fields written, they will be stored in a dictionary containing a key : value of that
        specific ingredient.
        
        Example:
        Fields = Qtd: 2, Unit: Slabs, Name: Beef, Category: Meats
        self.ing_dict = {'i_quantity': 2, 'i_unit': "Slabs", 'i_name': "Beef", "i_category": "Meats"}
        
        Then a function in The Creation/Update window is called to store this ingredient dictioanry inside a list
        """
        super().__init__()
        
        self.second_window = second_window  # keep reference to the previous window
        
        self.setWindowTitle("Ingredient")
        
        category_list = ['Meats', 'Vegetables', 'Dairy', 'Grains', 'Fats & Oils', 'Spices & Seasonings', 'Pantry Staples']
        self.ing_dict = {}
        
        ###------- Objects --------###
        
        # Quantity
        self.quantity_label = QLabel("Qtd.")
        self.quantity_line = QLineEdit()
        self.quantity_line.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.quantity_line.setMaximumWidth(40)
        
        # Unit
        self.unit_label = QLabel("Unit")
        self.unit_line = QLineEdit()
        self.unit_line.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.unit_line.setMaximumWidth(70)
        
        # Name
        self.name_label = QLabel("Name")
        self.name_line = QLineEdit()
        self.name_line.setMinimumWidth(200)
        
        # Category
        self.category_label = QLabel("Category")
        self.category_box = QComboBox()
        self.category_box.addItems(category_list)
        
        # Buttons
        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.add_ingredient)
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.cancel_window)
        
        ###------- Layout --------###
        self.master_layout = QVBoxLayout()
        
        # Row 1
        self.quant_group = QVBoxLayout()
        self.quant_group.addWidget(self.quantity_label)
        self.quant_group.addWidget(self.quantity_line)
        
        self.unit_group = QVBoxLayout()
        self.unit_group.addWidget(self.unit_label)
        self.unit_group.addWidget(self.unit_line)
        
        self.name_group = QVBoxLayout()
        self.name_group.addWidget(self.name_label)
        self.name_group.addWidget(self.name_line)
        
        self.cat_group = QVBoxLayout()
        self.cat_group.addWidget(self.category_label)
        self.cat_group.addWidget(self.category_box)
        
        # Grid Layout
        self.grid_layout = QGridLayout()
        
        self.grid_layout.addLayout(self.quant_group,0,0)
        self.grid_layout.addLayout(self.unit_group,0,1)
        self.grid_layout.addLayout(self.name_group,0,2,1,3) # Take up 1 row and 2 columns
        self.grid_layout.addLayout(self.cat_group,0,5)
        self.grid_layout.addWidget(self.add_button,1,4)
        self.grid_layout.addWidget(self.cancel_button,1,5)
        
        self.setLayout(self.grid_layout)
        
    def add_ingredient(self):
        """
        Function called by the Add button that stores the information from the fields into a dictioanry to easilly track
        what each value corresponds to. Then it call a fucntion from the Create/Update window to store this dictioanry inside
        a list. Then call the clear_ing_field() fucntion clean up the fields. Then clsoe the Ingredienst Window.
        """
        new_dic = {} 
        # Stores inside a dictionary
        new_dic["i_quantity"] = self.quantity_line.text()
        new_dic["i_unit"] = self.unit_line.text()
        new_dic["i_name"] = self.name_line.text()
        new_dic["i_category"] = self.category_box.currentText()
        
        
        self.second_window.load_ing_data(new_dic) # Calls the function from CreateWindow to add the new ingredient
        
        self.clear_ing_field()
        self.hide()
        
    def cancel_window(self):
        """
        Simple function called by the cancel button that calls the clear_ing_field() fucntion and then closes/hides the 
        Ingredient window without any changes.
        """
        self.clear_ing_field()
        self.hide()
        
    def clear_ing_field(self):
        """
        Function to reset to default version of the Ingredienst window by clearing any text in the fields.
        """
        self.quantity_line.clear()
        self.unit_line.clear()
        self.name_line.clear()
        self.category_box.setCurrentIndex(0)
        
        self.ing_dict.clear()