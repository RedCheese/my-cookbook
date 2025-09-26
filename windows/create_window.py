from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QTextEdit, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QComboBox, QTableWidget, QTableWidgetItem, QMessageBox, QSizePolicy, QHeaderView, QGroupBox, QCheckBox
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtCore import Qt
from windows.ingredient_window import IngredientWindow
from utils import generate_id, working_directory
from PyQt5.QtGui import QPixmap
from PIL import Image

class CreateWindow(QWidget):   
    def __init__(self, main_window):
        """
        This is the window where you Edit a Recipe either by Creating a brand new or updating an existing one. The fields 
        in this window are as followed:
        
        Tile: Name of the Recipe you want to give
        Image: Image of the recipe. You need to have the image in a fodler in your PC because its pathway that is saved in the
        Database
        Description: A resume or short description of the Recipe
        Ingredients: This is a table containing all the ingredients of your recipe. You can add or remove as you want.
        Instructions: The msot important of a recipe, the instructions to make it.
        Prep Time: Number in minutes of the time required to prepare the ignredients and equipment for the recipe
        Cook time: Number in minuteds of the time in average is required to cook the recipe.
        Servings: Number of people this recipe is made for
        Difficulty: Rating in how difficult is to make this recipe. This is more subjective in general.
        Category: Theres a check list of pre defined categories which you can choose any nubmer of where the Recipe falls under.
        
        Theres two hidden attributes of the Recipe that are automatically created when the Recipe is confirmed created:
        
        The ID, which is automatically created by a function that geenrates a random string with numbers to easilly identify
        the recipe for our queries. And the created_at that display the time and date at the exact momment this recipe is 
        created. These two attribtues are stored in the table alongside the rest during the query process.
        
        Update is different since we aren't creating, simply udpating a selected recipe.
        
        Example of a Recipe:
        
        ID: REC_78336640 (This is generated automatically so the user won't see this in the window)
        Title : Pancackes
        Image: c:/User/Images/pancacke.jpeg (The image path is generated when you select the image from a file)
        Description: "Delicious Breakfast for the whole familly"
        Ingredients: [(1, 'cup', 'Milk', 'Dairy'),
                      (2, 'units', 'chicken Egg', 'Bakery')]
        Instructions: " Mix in a bow the eggs and milk and then cook in a pan with 100 degrees"
        Prep Time in Minutes: 5
        Cook Time in Minutes: 2
        Servings: 4
        Difficulty: 1 - Easy
        Category: Breakfast, Snack
        created_at: 17/09/2025 (This is only created in the database)
        
        Update is basically the same as is the same window, but with the fields filled with the information we fetched
        from the database of the recipe we selected. The ID is already determiend so that doesn't change then the user
        can change all the information above(minus ID and created_at)

        """
        super().__init__()
        
        self.main_window = main_window  # keep reference to the previous window
        
        self.setWindowTitle("Update Window")
        
        self.ingredient_window = IngredientWindow(self) # Initializing the Recipe Window
        
        # Lists
        difficulty_rating = ["1 - Easy", "2 - Medium", "3 - Hard"]
        ingredients_table_headers = ["Quantity", "Unit", "Name", "Category"]
        self.ingredients_list = []
        self.current_recipe = {}
        self.category_check_list = {"Breakfast": 0, "Lunch": 0, "Dinner or Main Course": 0, "Appetizer":0, "Snack":0, "Soup":0,
                                   "Stew":0, "Salad":0, "Side Dish":0, "Dessert":0, "Baked Goods":0, "Beverages": 0}
        
        ###------- Objects --------###
        
        # title
        self.title_label = QLabel("Title")
        self.title_line = QLineEdit()
        
        # Image
        self.image_btn = QPushButton("Load Image")
        self.image_btn.setMaximumWidth(120)
        self.image_btn.setMaximumHeight(50)
        self.image_btn.clicked.connect(self.load_image)
        
        self.image_label = QLabel("Image")
        self.image_label.setMaximumWidth(360)
        self.image_label.setMaximumHeight(220)
        self.image_label.setMinimumWidth(340)
        self.image_label.setMinimumHeight(200)
        self.image = None
        self.image_path = ""
        
        # description
        self.description_label = QLabel("Description")
        self.description_line = QTextEdit()
        self.description_line.setMinimumHeight(30)
        self.description_line.setMaximumHeight(50)
        
        # ingredients
        self.ingredients_label = QLabel("Ingredients")
        self.ingredients_table = QTableWidget()
        self.ingredients_table.setColumnCount(4)
        self.ingredients_table.setHorizontalHeaderLabels(ingredients_table_headers)
        #Dynamically change the size of the app accordinglly to the table to remove the scrolling bar
        self.ingredients_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ingredients_table.setMinimumHeight(200)
        self.ingredients_table.setMaximumHeight(300)
        
        self.ingredients_add_button = QPushButton("Add")
        self.ingredients_add_button.setMaximumWidth(300)
        self.ingredients_add_button.setMinimumWidth(200)
        self.ingredients_add_button.clicked.connect(self.add_ingredient)
        
        self.ingredients_remove_button = QPushButton("Remove")
        self.ingredients_remove_button.setMaximumWidth(300)
        self.ingredients_remove_button.setMinimumWidth(200)
        self.ingredients_remove_button.clicked.connect(self.remove_ingredient)
        
        # instructions
        self.instructions_label = QLabel("Instructions")
        self.instructions_line = QTextEdit()
        
        # prep_time
        self.prep_label = QLabel("Prep Time in Minutes")
        self.prep_line = QLineEdit()
        
        # cook_time
        self.cook_label = QLabel("Cook Time in Minutes")
        self.cook_line = QLineEdit()
        
        # servings
        self.servings_label = QLabel("Servings")
        self.servings_line = QLineEdit()
        
        # difficulty
        self.difficulty_label = QLabel("Difficulty")
        self.difficulty_box = QComboBox()
        self.difficulty_box.addItems(difficulty_rating)
        
        # Category
        self.category_checkbox_list = []
        self.category_group = QGroupBox("Category")
        
        self.cat_breakfast = QCheckBox("Breakfast")
        self.cat_breakfast.stateChanged.connect(lambda state, checkbox="Breakfast", cat_id=1: self.category_check(state, checkbox, cat_id))
        self.category_checkbox_list.append(self.cat_breakfast)
                
        self.cat_lunch = QCheckBox("Lunch")
        self.cat_lunch.toggled.connect(lambda state, checkbox="Lunch", cat_id=2: self.category_check(state, checkbox, cat_id))
        self.category_checkbox_list.append(self.cat_lunch)
                
        self.cat_main = QCheckBox("Dinner or Main Course")
        self.cat_main.toggled.connect(lambda state, checkbox="Dinner or Main Course", cat_id=3: self.category_check(state, checkbox, cat_id))
        self.category_checkbox_list.append(self.cat_main)
        
        self.cat_appetizer = QCheckBox("Appetizer")
        self.cat_appetizer.toggled.connect(lambda state, checkbox="Appetizer", cat_id=4: self.category_check(state, checkbox, cat_id))
        self.category_checkbox_list.append(self.cat_appetizer)
        
        self.cat_snack = QCheckBox("Snack")
        self.cat_snack.toggled.connect(lambda state, checkbox="Snack", cat_id=5: self.category_check(state, checkbox, cat_id))
        self.category_checkbox_list.append(self.cat_snack)
        
        self.cat_soup = QCheckBox("Soup")
        self.cat_soup.toggled.connect(lambda state, checkbox="Soup", cat_id=6: self.category_check(state, checkbox, cat_id))
        self.category_checkbox_list.append(self.cat_soup)
        
        self.cat_stew = QCheckBox("Stew")
        self.cat_stew.toggled.connect(lambda state, checkbox="Stew", cat_id=7: self.category_check(state, checkbox, cat_id))
        self.category_checkbox_list.append(self.cat_stew)
        
        self.cat_salad = QCheckBox("Salad")
        self.cat_salad.toggled.connect(lambda state, checkbox="Salad", cat_id=8: self.category_check(state, checkbox, cat_id))
        self.category_checkbox_list.append(self.cat_salad)
        
        self.cat_side = QCheckBox("Side Dish")
        self.cat_side.toggled.connect(lambda state, checkbox="Side Dish", cat_id=9: self.category_check(state, checkbox, cat_id))
        self.category_checkbox_list.append(self.cat_side)
        
        self.cat_dessert = QCheckBox("Dessert")
        self.cat_dessert.toggled.connect(lambda state, checkbox="Dessert", cat_id=10: self.category_check(state, checkbox, cat_id))
        self.category_checkbox_list.append(self.cat_dessert)
        
        self.cat_baked = QCheckBox("Baked Goods")
        self.cat_baked.toggled.connect(lambda state, checkbox="Baked Goods", cat_id=11: self.category_check(state, checkbox, cat_id))
        self.category_checkbox_list.append(self.cat_baked)
        
        self.cat_beverage = QCheckBox("Beverages")
        self.cat_beverage.toggled.connect(lambda state, checkbox="Beverages", cat_id=12: self.category_check(state, checkbox, cat_id))
        self.category_checkbox_list.append(self.cat_beverage)
        
        # Category Layout Grouping
        self.category_group_layout = QVBoxLayout()
        self.category_group_layout_row1 = QHBoxLayout()
        self.category_group_layout_row2 = QHBoxLayout()
        self.category_group_layout_row3 = QHBoxLayout()
        
        self.category_group_layout_row1.addWidget(self.cat_breakfast)
        self.category_group_layout_row1.addWidget(self.cat_lunch)
        self.category_group_layout_row1.addWidget(self.cat_main)
        self.category_group_layout_row1.addWidget(self.cat_appetizer)
        
        self.category_group_layout_row2.addWidget(self.cat_snack)
        self.category_group_layout_row2.addWidget(self.cat_soup)
        self.category_group_layout_row2.addWidget(self.cat_stew)
        self.category_group_layout_row2.addWidget(self.cat_salad)
        
        self.category_group_layout_row3.addWidget(self.cat_side)
        self.category_group_layout_row3.addWidget(self.cat_dessert)
        self.category_group_layout_row3.addWidget(self.cat_baked)
        self.category_group_layout_row3.addWidget(self.cat_beverage)
        
        self.category_group_layout.addLayout(self.category_group_layout_row1)
        self.category_group_layout.addLayout(self.category_group_layout_row2)
        self.category_group_layout.addLayout(self.category_group_layout_row3)
        
        self.category_group.setLayout(self.category_group_layout)
        
        ##  ---- Buttons ---- ##
        
        # Confirm Button
        self.confirm_button = QPushButton("Confirm")
        self.confirm_button.clicked.connect(self.confirm_creation)
        #self.confirm_btn_layout = QHBoxLayout()
        #self.confirm_btn_layout.addWidget(self.confirm_button)
        
        # Update Button
        self.update_button = QPushButton("Update")
        self.update_button.clicked.connect(self.confirm_update)
        #self.update_btn_layout = QHBoxLayout()
        #self.update_btn_layout.addWidget(self.update_button)
        #self.update_btn_layout.hide()
        self.update_button.hide()
        
        # Cancel Button
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.cancel_creation)
        
        ###------- Layout --------###
        
        self.master_layout = QVBoxLayout()
        
        self.row1 = QHBoxLayout()
        self.row2 = QHBoxLayout()
        self.row3 = QHBoxLayout()
        self.row4 = QHBoxLayout()
        self.row5 = QHBoxLayout()
        self.row6 = QHBoxLayout()
        self.row7 = QHBoxLayout()
        self.row8 = QHBoxLayout()
        
        # Row 1
        self.title_group = QVBoxLayout()
        
        self.title_group.addWidget(self.title_label)
        self.title_group.addWidget(self.title_line)
        
        self.row1.addLayout(self.title_group)
        
        # Row 2 - Description Row
        self.desc_group = QVBoxLayout()
        
        self.desc_group.addWidget(self.description_label)
        self.desc_group.addWidget(self.description_line)
        
        self.row2.addLayout(self.desc_group)
        
        # Row 3 - Ingredients Row
        self.ing_group = QVBoxLayout()
        self.ing_btn_group = QVBoxLayout()
        self.ing_btn_table_group = QHBoxLayout()
        
        self.ing_btn_group.addWidget(self.ingredients_add_button)
        self.ing_btn_group.addWidget(self.ingredients_remove_button)
        
        self.ing_btn_table_group.addLayout(self.ing_btn_group)
        self.ing_btn_table_group.addWidget(self.ingredients_table)
        
        self.ing_group.addWidget(self.ingredients_label)
        self.ing_group.addLayout(self.ing_btn_table_group)
        
        self.row3.addLayout(self.ing_group)
        
        # Row 4 - Instructions Row
        self.inst_group = QVBoxLayout()
        
        self.inst_group.addWidget(self.instructions_label)
        self.inst_group.addWidget(self.instructions_line)
        
        self.row4.addLayout(self.inst_group)
        
        # Row 5
        self.row5.addWidget(self.prep_label)
        self.row5.addWidget(self.prep_line)
        self.row5.addWidget(self.cook_label)
        self.row5.addWidget(self.cook_line)
        self.row5.addWidget(self.servings_label)
        self.row5.addWidget(self.servings_line)
        self.row5.addWidget(self.difficulty_label)
        self.row5.addWidget(self.difficulty_box)
        
        # Row 6 - Category Row
        self.row6.addWidget(self.category_group)
        
        # Row 7 - Image Row
        # Stack the image and the button
        self.image_layout = QGridLayout()
        self.image_layout.addWidget(self.image_label, 0 ,0)
        self.image_layout.addWidget(self.image_btn, 0, 0, Qt.AlignBottom | Qt.AlignHCenter)

        self.row7.addLayout(self.image_layout)
        
        # row 8 - Button Row
        #self.row8.addLayout(self.confirm_btn_layout)
        #self.row8.addLayout(self.update_btn_layout)
        self.row8.addWidget(self.confirm_button)
        self.row8.addWidget(self.update_button)
        self.row8.addWidget(self.cancel_button)
        
        
        # Master Layouts
        self.master_layout.addLayout(self.row1)
        self.master_layout.addLayout(self.row2)
        self.master_layout.addLayout(self.row3)
        self.master_layout.addLayout(self.row4)
        self.master_layout.addLayout(self.row5)
        self.master_layout.addLayout(self.row6)
        self.master_layout.addLayout(self.row7)
        self.master_layout.addLayout(self.row8)

        self.setLayout(self.master_layout)
        
    
        
    def category_check(self, state, category: str, cat_id: int):
        """
        This method receives the state(checked or unchecked) the category type and its ID.
        By Checking its state it changes the ID inside the category list. 0 always will be for the unchecked categories
        This ID will be then used for when inserting inside the RecipeCategory table
        """
        
        if state == 0:
            self.category_check_list[category]= 0
            
        else:
            self.category_check_list[category] = cat_id
            
    def create_mode(self):
        """
        The default mode Create Recipe Mode where the user can create the new recipe
        """
        #self.confirm_button.clicked.connect(self.confirm_creation)
        if self.update_button.isVisible():
            self.confirm_button.show()
            self.update_button.hide()
        self.clear_field()
        self.setWindowTitle("New Recipe")
        
    def update_mode(self, recipe: list):
        """
        This changes the CreateWindow into an Update Window, putting all the information from the recipe clicked into
        their respective fields in the window.
        """
        # Will hide the Create Button and show the Update Button
        #self.confirm_button.clicked.connect(self.confirm_update)
        if self.confirm_button.isVisible():
            self.confirm_button.hide()
            self.update_button.show()
        
        self.current_recipe = recipe
        
        self.setWindowTitle("Update Window")
        
        self.ingredients_table.clear()
        
        for box in self.category_checkbox_list:
            box.setChecked(False)
        
        self.title_line.setText(recipe["title"])
        self.description_line.setText(recipe["description"])
        self.instructions_line.setPlainText(recipe["instructions"])
        self.prep_line.setText(str(recipe["prep_time"]))
        self.cook_line.setText(str(recipe["cook_time"]))
        self.servings_line.setText(str(recipe["servings"]))
        self.difficulty_box.setCurrentText(recipe["difficulty"])
        
        # Iterating over the list of ingredients
        self.ingredients_list = recipe["ingredient_list"]
        self.load_ing_table()
        
        # Iterating over the list of categories
        for box in self.category_checkbox_list:
            for cat in recipe["category_list"]:
                if box.text() == cat["c_name"]:
                    box.setChecked(True)
                     
        
    def confirm_creation(self):
        """
        Method that will query the information inside the fields into the tables in the Da5tabase. It goes in order:
        
        First query is to insert in the Recipe Table all its information
        
        Second query will iterate over the recipe's ingredients and insert them into the Ingredients table and then in the same
        loop create the thrid type of query that connects Recipe and Ingredient in the RecipeIngredients Union Table
        
        Forth Query will connect the Recipe to its Categories.
        
        As finisher it cleans up the fields, clsoe the current Create WIndow and loads the Main Window table showing it updated 
        with the new entry
        """
        query = QSqlQuery()
        
        recipe_title = self.title_line.text()
        recipe_instructions = self.instructions_line.toPlainText()
        
        # Make sure important fields arent empty
        if recipe_title == "" or recipe_instructions == "" or len(self.ingredients_list) <= 0:
            QMessageBox.warning(self, "Got an empty field", "Please add a value to all fields")
            return
        
        # Recipe
        recipe_id = generate_id(prefix="REC_", length=8)
        recipe_description = self.description_line.toPlainText()
        recipe_prep_time = self.prep_line.text()
        recipe_cook_time = self.cook_line.text()
        recipe_servings = self.servings_line.text()
        recipe_difficulty = self.difficulty_box.currentText()
        recipe_image = self.image_path
        
        query.exec_("""
                    INSERT INTO Recipes (recipe_id, title, description, instructions, prep_time, cook_time, servings, difficulty, Image)
                    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """)
        query.addBindValue(recipe_id)
        query.addBindValue(recipe_title)
        query.addBindValue(recipe_description)
        query.addBindValue(recipe_instructions)
        query.addBindValue(recipe_prep_time)
        query.addBindValue(recipe_cook_time)
        query.addBindValue(recipe_servings)
        query.addBindValue(recipe_difficulty)
        query.addBindValue(recipe_image)
        query.exec_()

        
        # Ingredient
        for ing in self.ingredients_list:
            ing_id = generate_id(prefix="ING_", length=8)
            query.exec_("""
                    INSERT INTO Ingredients (ingredient_id, name, category, unit)
                    VALUES(?, ?, ?, ?)
                    """)
            query.addBindValue(ing_id)
            query.addBindValue(ing["i_name"])
            query.addBindValue(ing["i_category"])
            query.addBindValue(ing["i_unit"])
            query.exec_()
            
            
            # RecipeIngredient
            query.exec_("""
                    INSERT INTO RecipeIngredients (recipe_id, ingredient_id, quantity, unit)
                    VALUES(?, ?, ?, ?)
                    """)
            query.addBindValue(recipe_id)
            query.addBindValue(ing_id)
            query.addBindValue(ing["i_quantity"])
            query.addBindValue(ing["i_unit"])
            query.exec_()
        
        # RecipeCategories
        for value in self.category_check_list.values():
            if value != 0:
                query.exec_("""
                    INSERT INTO RecipeCategories (recipe_id, category_id)
                    VALUES(?, ?)
                    """)
                query.addBindValue(recipe_id)
                query.addBindValue(value)
                query.exec_()
                
            else:
                continue
        
        self.main_window.load_table() # Call the laod table fucntion from main window
        self.clear_field()
        self.hide()
        
    def confirm_update(self):
        """
        In update mode, this fucntion is called by the Update Button that will call multiple queries to update the changes 
        to the recipe.
        
        The Error Handling was to identify issues like the table locking from solving a query the afct that multiple queries
        are been called at the same time. So each Query has a tarnsation and commit to make ssure the database doesnt lock.
        
        The first query is to delete all connections between Recipe and Ingredients, due the fact Ingredients could have
        been removed or added during the update, so i clean reset was required and even if an ingredient hasnt been changed,
        its conenction will be cut off, but will be reconnected later on.
        
        The second query is to delete all Ingredients that no longer have a connection to a recipe. Only wasting space in
        the Database by having an ingredient not been used in any recipe.
        
        The Third query is to delete the connection between Recipe and Category tables to a more simplified state
        
        All Delete queries are done, now for the forth query is to update the Recipe table by taking the current information
        from the Update Window. These are seperate from Ingredients and Categories as they require different queries.
        
        5th and 6th queries will iterated over the ingredients list with the 5th gonig each ingredient and 6th query to 
        create the connection to the Recipe table.
        
        And finally the 7th query to handle the Categories by creating the connection. Categories table is a static table 
        with defined values so the query will compare the IDs only to create the conenction.
        
        It concludes by calling the Load Table Function from the Main Window with the updated information, clears the 
        fields and closes the window
        """
        
        # Getting the fields
        recipe_title = self.title_line.text()
        recipe_instructions = self.instructions_line.toPlainText()
        
        if recipe_title == "" or recipe_instructions == "" or len(self.current_recipe["ingredient_list"]) <= 0:
            QMessageBox.warning(self, "Got an empty field", "Please add a value to all fields")
            return
        
        
        recipe_id = self.current_recipe["recipe_id"]
        recipe_description = self.description_line.toPlainText()
        recipe_prep_time = self.prep_line.text()
        recipe_cook_time = self.cook_line.text()
        recipe_servings = self.servings_line.text()
        recipe_difficulty = self.difficulty_box.currentText()
        recipe_image = self.image_path
        
        print(self.current_recipe)
        
        # Error Handling
        db = QSqlDatabase.database()
        
        if not db.isOpen():
            print("Database is not open")
            return
        
        # Delete fields
        if not db.transaction():
            print("Failed to start transaction:", db.lastError().text())
            return
        
        try:
            query1 = QSqlQuery(db)
            
            # -- Remove ingredient links for this recipe
            query1.prepare("""
                   -- Remove ingredient links for this recipe
                    DELETE FROM RecipeIngredients
                    WHERE recipe_id = ?;
                    """)
            query1.addBindValue(recipe_id)

            if not query1.exec_():
                raise Exception(query1.lastError().text())
            
            query1.finish()
            
            # -- Delete ingredients that are no longer used anywhere
            query2 = QSqlQuery(db)
            
            if not query2.exec_("""
                   -- Delete ingredients that are no longer used anywhere
                    DELETE FROM Ingredients
                    WHERE NOT EXISTS (
                        SELECT 1
                        FROM RecipeIngredients ri
                        WHERE ri.ingredient_id = Ingredients.ingredient_id
                    );
                    """):
                raise Exception(query2.lastError().text())
            query2.finish()
            
            # -- Remove category links for this recipe
            query3 = QSqlQuery(db)
            
            query3.prepare("""
                   -- Remove category links for this recipe
                    DELETE FROM RecipeCategories
                    WHERE recipe_id = ?;
                    """)
            query3.addBindValue(recipe_id)
            if not query3.exec_():
                raise Exception(query3.lastError().text())
        
            query3.finish()
            print("Recipe deleted successfully")
            
            # COmmit the transaction
            if not db.commit():
                raise Exception(db.lastError().text())
     
        except Exception as e:
            db.rollback()
            print("Error:", e)
      
        # Adding The Recipe base details
        if not db.transaction():
            print("Failed to start transaction:", db.lastError().text())
            return
        
        try:
            # Recipe
            query4 = QSqlQuery(db)
            
            query4.prepare("""
                    UPDATE Recipes
                    SET  title = ?, description = ?, instructions = ?, prep_time = ?, cook_time = ?, 
                    servings = ?, difficulty = ?, Image = ?
                    WHERE recipe_id = ?
                    """)
            query4.addBindValue(recipe_title)
            query4.addBindValue(recipe_description)
            query4.addBindValue(recipe_instructions)
            query4.addBindValue(recipe_prep_time)
            query4.addBindValue(recipe_cook_time)
            query4.addBindValue(recipe_servings)
            query4.addBindValue(recipe_difficulty)
            query4.addBindValue(recipe_image)
            query4.addBindValue(recipe_id)
            if not query4.exec_():
                raise Exception(query4.lastError().text())
        
            query4.finish()
            print("Recipe updated successfully")
            
            # COmmit the transaction
            if not db.commit():
                raise Exception(db.lastError().text())
            
        except Exception as e:
            db.rollback()
            print("Error:", e)
            
        # Adding The Ingredients
        if not db.transaction():
            print("Failed to start transaction:", db.lastError().text())
            return
        
        try:
            # Now to insert the ingredients
            query5 = QSqlQuery(db)
            
            for ing in self.current_recipe["ingredient_list"]:
                ing_id = generate_id(prefix="ING_", length=8)
                query5.prepare("""
                    INSERT INTO Ingredients (ingredient_id, name, category, unit)
                    VALUES(?, ?, ?, ?)
                    """)
                query5.addBindValue(ing_id)
                query5.addBindValue(ing["i_name"])
                query5.addBindValue(ing["i_category"])
                query5.addBindValue(ing["i_unit"])
                if not query5.exec_():
                    raise Exception(query5.lastError().text())
                    
                query5.finish()
                
                
                # RecipeIngredient
                query5.prepare("""
                        INSERT INTO RecipeIngredients (recipe_id, ingredient_id, quantity, unit)
                        VALUES(?, ?, ?, ?)
                        """)
                query5.addBindValue(recipe_id)
                query5.addBindValue(ing_id)
                query5.addBindValue(ing["i_quantity"])
                query5.addBindValue(ing["i_unit"])
                if not query5.exec_():
                    raise Exception(query5.lastError().text())
                
                query5.finish()
                    
            # COmmit the transaction
            if not db.commit():
                raise Exception(db.lastError().text())
                
            print("Ingredients added successfully")
            
        except Exception as e:
            db.rollback()
            print("Error:", e)
        
        
        # Adding The Categories
        if not db.transaction():
            print("Failed to start transaction:", db.lastError().text())
            return
        
        try:
            query6 = QSqlQuery(db)
            print(self.category_check_list)
            for value in self.category_check_list.values():
                if value != 0:
                    query6.finish()
                    query6.prepare("""
                            INSERT INTO RecipeCategories (recipe_id, category_id)
                            VALUES(?, ?)
                            """)
                    query6.addBindValue(recipe_id)
                    query6.addBindValue(value)
                
                    if not query6.exec_():
                        raise Exception(query6.lastError().text())
                else:
                    continue
            
            print("Category Updated successfully")
            
            # COmmit the transaction
            if not db.commit():
                raise Exception(db.lastError().text())
            
        except Exception as e:
            db.rollback()
            print("Error:", e)
        
        # Conclusion
        self.main_window.load_table() # Call the load table function from main window
        self.clear_field()
        self.hide()
 
    def cancel_creation(self):
        """
        Function called by the Cancel Button that will call the function to clear the fields and then close/hide the
        Create Recipe window.
        """
        self.clear_field()
        self.hide()
        
    def clear_field(self):
        """
        Function that will clean up the fields returning them into the default empty state
        """
        for box in self.category_checkbox_list:
            box.setChecked(False)
        
        self.ingredients_list.clear()
        self.category_check_list.clear()
        
        self.load_ing_table()
        
        self.title_line.clear()
        self.description_line.clear()
        self.instructions_line.clear()
        self.prep_line.clear()
        self.cook_line.clear()
        self.servings_line.clear()
        self.difficulty_box.setCurrentIndex(0)
        
        
    def add_ingredient(self):
        """
        Function called by the Add Ingredient button to show/hide the Ingredients Window
        """
        if self.ingredient_window.isVisible():
            self.ingredient_window.hide()

        else:
            self.ingredient_window.show()
        
    def remove_ingredient(self):
        """
        Function that will remove the current chsoen ingredient in the table
        
        Will be required to select the ingredient that you want to remove. Then the function to load the ingredients table
        to show the changes.
        """
        selected_row = self.ingredients_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "No Ingredient was chosen", "Please select an Row to delete")
            return
        
        confirm = QMessageBox.question(self, "Are you sure?", "Delete Row?", QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.No:
            return
        
        self.ingredients_list.pop(selected_row)
        self.load_ing_table()
        
    def load_ing_data(self, ing):
        """
        This function is called by the Ingredients Window so we can the new ingredient to the list of ingredients. Also
        calling to load the ingredients table to show the new changes
        """
        self.ingredients_list.append(ing)
        self.load_ing_table()
        
        
    def load_ing_table(self):
        """
        We have an ingredients list (self.ingredients_list) to keep track of all ingredients of the recipe and this function
        will iterate over this lsit and display them in a table.
        """
        self.ingredients_table.setRowCount(0) # Resets the table to empty
        row = 0 # Indicates the first row
        for row in range(len(self.ingredients_list)): #Will iterate over the ingredients list
            quantity = self.ingredients_list[row]["i_quantity"]
            unit = self.ingredients_list[row]["i_unit"]
            name = self.ingredients_list[row]["i_name"]
            category = self.ingredients_list[row]["i_category"]
            
            self.ingredients_table.insertRow(row)
            self.ingredients_table.setItem(row, 0, QTableWidgetItem(str(quantity)))
            self.ingredients_table.setItem(row, 1, QTableWidgetItem(unit))
            self.ingredients_table.setItem(row, 2, QTableWidgetItem(name))
            self.ingredients_table.setItem(row, 3, QTableWidgetItem(category))
            
            row += 1
    
    def load_image(self):
        """
        Function to load an image file from a folder. The Image will be display in the window and its path will be stored in
        a variable that will be later stored in the database
        """
        self.image_path = working_directory() # Calls the working_directory function to get image path
        
        if self.image_path:
            self.image = Image.open(self.image_path) # Stores the image
        else:
            return
        
        self.image_label.hide() # Clears the current image or label
        image = QPixmap(self.image_path) # loads the image from the directory
        w, h = self.image_label.width(), self.image_label.height() # stores the height and width values of the image container
        image = image.scaled(w, h, Qt.KeepAspectRatio) # Scale the image to the same as container and retains its quality
        self.image_label.setPixmap(image) # Place the image inside the container
        self.image_label.show() # Show the image