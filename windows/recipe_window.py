from pdf_generator import PDFGenerator

from PyQt5.QtWidgets import (QWidget, QLabel, QVBoxLayout, QHBoxLayout, 
                             QPlainTextEdit, QListWidget, QPushButton, QLineEdit, QMessageBox)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class RecipeWindow(QWidget):
    
    def __init__(self, main_window):
        super().__init__()
        
        self.main_window = main_window  # keep reference to the previous window
        
        self.setWindowTitle("Recipe Window")
        
        self.resize(1600, 900)

        self.current_recipe = {}
        
        ###------- Objects --------###
        
        # title
        #self.rec_title_label = QLabel("Title")
        self.rec_title = QLabel("Recipe Title")
        self.rec_title.setStyleSheet("font-size: 16pt; font-weight: bold; margin: 5px;")
        
        # Image
        self.rec_image = QLabel("Image")
        self.rec_image.setMaximumWidth(400)
        self.rec_image.setMaximumHeight(280)
        self.rec_image.setMinimumWidth(380)
        self.rec_image.setMinimumHeight(260)
        
        # description
        #self.rec_description_label = QLabel("Description")
        self.rec_description = QLabel("Recipe Description")
        self.rec_description.setStyleSheet("font-size: 14pt; margin: 2px;")
        
        # instructions
        self.rec_instructions_label = QLabel("Instructions")
        self.rec_instructions = QPlainTextEdit()
        self.rec_instructions.setPlainText("Recipe Instructions")
        
        # Ingredients
        self.rec_ingredients_label = QLabel("Ingredients")
        self.rec_ingredients_list = QListWidget()
        self.rec_ingredients_list.addItems(["Ing One", "Ing Two", "Ing Three"])
        
        # prep_time
        self.rec_prep_label = QLabel("Prep Time in Minutes: ")
        self.rec_prep = QLabel("10")
        
        # cook_time
        self.rec_cook_label = QLabel("Cook Time in Minutes: ")
        self.rec_cook = QLabel("30")
        
        # servings
        self.rec_servings_label = QLabel("Servings: ")
        self.rec_servings = QLabel("2")
        
        # difficulty
        self.rec_difficulty_label = QLabel("Difficulty: ")
        self.rec_difficulty = QLabel("1 - Easy")
        
        # Category
        self.rec_category_label = QLabel("Categories")
        self.rec_category_list = QListWidget()
        self.rec_category_list.addItems(["Cat One", "Cat Two"])
        
        ##---Buttons---##
        self.rec_close_btn = QPushButton("Close")
        self.rec_close_btn.clicked.connect(self.close_window)
        
        self.rec_download_btn = QPushButton("Download")
        self.rec_download_btn.clicked.connect(self.download_recipe)
        
        ###------- Layout --------###
        self.master_layout = QHBoxLayout()
        
        # Col 1 - All Other Information
        self.main_col1 = QVBoxLayout()
        
        self.col1_group1 = QHBoxLayout()
        self.col1_group2 = QHBoxLayout()
        
        # Ingredient objects group
        self.col1_ing_group = QVBoxLayout()
        self.col1_ing_group.addWidget(self.rec_ingredients_label)
        self.col1_ing_group.addWidget(self.rec_ingredients_list)
        
        # Preparations time objects group
        self.col1_prep_group = QHBoxLayout()
        self.col1_prep_group.addWidget(self.rec_prep_label)
        self.col1_prep_group.addWidget(self.rec_prep)
        
        # Cooking Time objects group
        self.col1_cook_group = QHBoxLayout()
        self.col1_cook_group.addWidget(self.rec_cook_label)
        self.col1_cook_group.addWidget(self.rec_cook)
        
        # Servings objects group
        self.col1_serv_group = QHBoxLayout()
        self.col1_serv_group.addWidget(self.rec_servings_label)
        self.col1_serv_group.addWidget(self.rec_servings)
        
        # Difficulty objects group
        self.col1_dif_group = QHBoxLayout()
        self.col1_dif_group.addWidget(self.rec_difficulty_label)
        self.col1_dif_group.addWidget(self.rec_difficulty)
        
        # Category objects group
        self.col1_cat_group = QVBoxLayout()
        self.col1_cat_group.addWidget(self.rec_category_label)
        self.col1_cat_group.addWidget(self.rec_category_list)
        
        # Buttons Group
        self.col1_btn_group = QHBoxLayout()
        self.col1_btn_group.addWidget(self.rec_close_btn)
        self.col1_btn_group.addWidget(self.rec_download_btn)
        
        self.col1_group1.addLayout(self.col1_prep_group)
        self.col1_group1.addLayout(self.col1_cook_group)
        self.col1_group2.addLayout(self.col1_serv_group)
        self.col1_group2.addLayout(self.col1_dif_group)
        
        self.main_col1.addWidget(self.rec_title)
        self.main_col1.addWidget(self.rec_image)
        self.main_col1.addWidget(self.rec_description)
        self.main_col1.addLayout(self.col1_ing_group)
        self.main_col1.addLayout(self.col1_group1)
        self.main_col1.addLayout(self.col1_group2)
        self.main_col1.addLayout(self.col1_cat_group)
        self.main_col1.addLayout(self.col1_btn_group)
        
        # Col 2 Layout - Instructions
        self.main_col2 = QVBoxLayout()
        
        self.main_col2.addWidget(self.rec_instructions_label)
        self.main_col2.addWidget(self.rec_instructions)
        
        # Master Layout
        self.master_layout.addLayout(self.main_col1, 30) # The stretch number is the amount of space of the app is using,                                                       
        self.master_layout.addLayout(self.main_col2, 70) # so we can give more room to the image
        
        self.setLayout(self.master_layout)
        
    def load_data(self, recipe):
        """ This function loads the data from the selected recipe in the main window
            and displays it in the appropriate fields in this window."""
        self.rec_ingredients_list.clear()
        self.rec_category_list.clear()

        self.current_recipe = recipe # Store the current recipe for PDF generation
        
        self.setWindowTitle(recipe["title"])
        
        self.rec_title.setText(recipe["title"])
        self.rec_description.setText(recipe["description"])
        self.rec_instructions.setPlainText(recipe["instructions"])
        self.rec_prep.setText(str(recipe["prep_time"]))
        self.rec_cook.setText(str(recipe["cook_time"]))
        self.rec_servings.setText(str(recipe["servings"]))
        self.rec_difficulty.setText(recipe["difficulty"])
        
        # Iterating over the list of ingredients
        ing_list = []
        i = 0
        temp_list = recipe['ingredient_list']
        for i in range(len(temp_list)):
            ing_list.append(f"{temp_list[i]['i_quantity']} {temp_list[i]['i_unit']} of {temp_list[i]['i_name']}")
        
        self.rec_ingredients_list.addItems(ing_list)
        
        # Iterating over the list of categories
        cat_list = []
        c = 0
        temp_list = recipe['category_list']
        for c in range(len(temp_list)):
            cat_list.append(f"{temp_list[c]['c_name']} : {temp_list[c]['c_description']}")
        
        self.rec_category_list.addItems(cat_list)
        
        self.load_image(recipe["Image"])
        
    def close_window(self):
        self.clear_recipe_fields()
        self.hide()
        
    def load_image(self, image_path):
        self.rec_image.hide() # Clears the current image or label
        image = QPixmap(image_path) # loads the image from the directory
        w, h = self.rec_image.width(), self.rec_image.height() # stores the height and width values of the image container
        image = image.scaled(w, h, Qt.KeepAspectRatio) # Scale the image to the same as container and retains its quality
        self.rec_image.setPixmap(image) # Place the image inside the container
        self.rec_image.show() # Show the image
        
    def download_recipe(self):
        """
        This calls the class to generate the PDF file fo the recipe
        Theres the options for opening the file:
        
        pdf_generator.generate_recipe_pdf(self.current_recipe, open_mode="folder")
        pdf_generator.generate_recipe_pdf(self.current_recipe, open_mode="file")
        pdf_generator.generate_recipe_pdf(self.current_recipe, open_mode=None)
        """
        pdf_generator = PDFGenerator()
        pdf_generator.generate_recipe_pdf(self.current_recipe, open_mode="file")

    def clear_recipe_fields(self):
        print("clear")
