import sys
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QLineEdit, QTableWidget, QTableWidgetItem, QMessageBox, 
                             QSizePolicy, QHeaderView, QRadioButton, QAction)
from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlQuery
from utilities.database import RecipeDatabase
from windows.recipe_window import RecipeWindow
from windows.create_window import CreateWindow
from windows.settings_window import SettingsWindow
from utilities.settings import SettingsManager
from utilities.styles import load_cookbook_style


class Cookbook(QMainWindow):
    def __init__(self):
        """
        Main Window of the App containing Buttons with different function, a search abr and a table displaying all the recipes
        in the database.
        
        First it has a Title for the Cookbook which you can edit and change it
        
        The lists and dictioanries are use to store information to be used throught the app.
        
        Theres a Search Bar where you can type anything and will search the database for recipes that ahs the serached word 
        in its title or description. Example, if you type mushroom and clcik search, the table will load only recipes with 
        mushrooms.
        
        Next is the row of buttons with each one having a functionality:
        
        Open: If you select a row and then click this button, it will open a window showing all the information from that recipe
        New: It opens a new window where you can create a brand new recipe
        Edit: Need to select a recipe and then this opens a new window containing all the current information of that recipe. 
        You then can change that information to update it in the database.
        Delete: SImply deletes the chosen recipe from the database
        
        Then theres a table showing, by default, all the recipes in your database. You can filter it via the search bar 
        or the Tags( Future Update ). This table only shows the name, description and date of creation so it doesnt clutter the 
        window. You can open the recipe for more information of that recipe.
        """
        super().__init__()
        
        self.setWindowTitle("Cookbook")
        self.resize(1400, 900)
        
        main_window = QWidget()
        
        # Load the settings
        self.settings = SettingsManager()
        
        ###----- Styles -------- ###
        # Load stylesheet (create if missing)
        load_cookbook_style(self)

        ###------ Windows ------###
        self.recipe_window = RecipeWindow(self) # Initializing the Recipe Window
        self.create_window = CreateWindow(self) # Initializing the Create Window
        self.settings_window = SettingsWindow(self) # Initializing the Settings Window
        
        # Lists and Dictonaries
        self.recipe_data_dic = {'ingredient_list': [], 'category_list': []}# Dictionary that stores the information of 
                                                                           # the selected recipe
        table_headers = ['Title', 'Description', 'Date of Creation'] # Table headers
        self.cookbook_settings = {'cookbook_name': self.settings.name} # Dictionary with the app settings
        
        self.show_or_update = "Show"
        
        ###-------Menu---------###
        self.menu = self.menuBar()
        
        self.file_menu = self.menu.addMenu("&File")
        self.edit_menu = self.menu.addMenu("Edit")
        
        #File Menu
        self.settings_action = QAction("Settings", self)
        self.settings_action.setStatusTip("This opens the Cookbook settings window")
        self.settings_action.triggered.connect(self.open_settings)
        
        self.file_menu.addAction(self.settings_action)
        
        # Edit Menu
        self.edit_table_submenu = self.edit_menu.addMenu("Table")
        
        self.table_alphabetic_action = QAction("Alphabetic Order", self)
        self.table_alphabetic_action.setStatusTip("This orders the table in alphabetic order by title name")
        self.table_alphabetic_action.triggered.connect(self.table_alphabetic)
        
        self.edit_table_submenu.addAction(self.table_alphabetic_action)
        
        ###------- Objects --------###
        # Objects - Title
        self.title = QLabel(self.settings.name)
        self.title.setStyleSheet("font-size: 18pt; font-weight: bold; margin: 5px;")
        
        # Objects - LineEdit
        self.search_line = QLineEdit()
        self.search_line.setText("")
        
        # Objects - Buttons
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_recipe)
        self.search_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.search_button.setMinimumWidth(100)
        self.search_button.setMinimumHeight(40)
        self.search_button.setStyleSheet("font-size: 14pt; margin: 5px;")
        
        self.open_button = QPushButton("Open")
        self.open_button.clicked.connect(self.show_mode_recipe)
        self.open_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.open_button.setMinimumWidth(100)
        self.open_button.setMinimumHeight(50)
        self.open_button.setStyleSheet("font-size: 14pt; margin: 5px;")
        
        self.new_button = QPushButton("New")
        self.new_button.clicked.connect(self.new_recipe)
        self.new_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.new_button.setMinimumWidth(100)
        self.new_button.setMinimumHeight(50)
        self.new_button.setStyleSheet("font-size: 14pt; margin: 5px;")
        
        self.edit_button = QPushButton("Edit")
        self.edit_button.clicked.connect(self.update_mode_recipe)
        self.edit_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.edit_button.setMinimumWidth(100)
        self.edit_button.setMinimumHeight(50)
        self.edit_button.setStyleSheet("font-size: 14pt; margin: 5px;")
        
        self.delete_button = QPushButton("Delete")
        self.delete_button.clicked.connect(self.delete_recipe)
        self.delete_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.delete_button.setMinimumWidth(100)
        self.delete_button.setMinimumHeight(50)
        self.delete_button.setStyleSheet("font-size: 14pt; margin: 5px;")
        
        self.reload_table = QPushButton("Reload")
        self.reload_table.clicked.connect(self.load_table)
        self.reload_table.setStyleSheet("font-size: 12pt; margin: 5px;")
        self.reload_table.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.reload_table.setMinimumWidth(80)
        self.reload_table.setMinimumHeight(50)
        
        # Objects - Ascending/Descending Table Radio Buttons
        self.asc_radio_button = QRadioButton("Ascending")
        self.asc_radio_button.setChecked(True)
        self.asc_radio_button.order = "Ascending"
        self.asc_radio_button.toggled.connect(self.table_order_toggle)
        
        self.desc_radio_button = QRadioButton("Descending")
        self.desc_radio_button.order = "Descending"
        self.desc_radio_button.toggled.connect(self.table_order_toggle)
        
        # Objects - Table
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(table_headers)
        self.table.horizontalHeader().sectionClicked.connect(self.header_clicked)
        
        #table design
        #Dynamically change the size of the app accordinglly to the table to remove the scrolling bar
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        #Sort the table in descending order to show at top the newest entries
        self.table.sortByColumn(2, Qt.DescendingOrder)
        
        ###------- Layout --------###
        self.master_layout = QVBoxLayout()
        
        self.row1 = QHBoxLayout() # Title
        self.row2 = QHBoxLayout() # Buttons
        self.row3 = QHBoxLayout() # Option Buttons
        self.row4 = QHBoxLayout() # Order Radio Buttons
        
        # Row 1 - Title
        self.row1 = QHBoxLayout()
        self.row1.addWidget(self.title)
        
        # Row 2 - Buttons
        self.row2.addWidget(self.open_button)
        self.row2.addWidget(self.new_button)
        self.row2.addWidget(self.edit_button)
        self.row2.addWidget(self.delete_button)
        
        # Row 3 - Optin Buttons
        self.row3.addWidget(self.search_button)
        self.row3.addWidget(self.search_line)
        self.row3.addWidget(self.reload_table)
        
        # Row 4 - Table Order Radio Buttons
        self.row4.addStretch(1)
        self.row4.addWidget(self.asc_radio_button)
        self.row4.addWidget(self.desc_radio_button)
        
        # Master Layout
        self.master_layout.addLayout(self.row1)
        self.master_layout.addLayout(self.row2)
        self.master_layout.addLayout(self.row3)
        self.master_layout.addLayout(self.row4)
        self.master_layout.addWidget(self.table)

        #self.setLayout(self.master_layout)
        main_window.setLayout(self.master_layout)
        self.setCentralWidget(main_window)
        
        # Load table
        self.load_table()
        
    def load_table(self):
        """
        Resets the table and then perform a query based on the string in the search abr. If its empty, will search for all
        recipes. Otherwise, will search the title and description that matches the text in the search bar
        """
        self.table.setRowCount(0)
        query = QSqlQuery()
        
        if self.search_line.text() == "":
            query.exec_("SELECT title, description, created_at FROM Recipes")
        else:
            query.exec_("""
                    SELECT title, description, created_at
                    FROM Recipes
                    WHERE LOWER(title) LIKE LOWER(?)
                    OR
                    LOWER(description) LIKE LOWER(?)
                    """)
            query.addBindValue('%'+self.search_line.text()+'%')
            query.addBindValue('%'+self.search_line.text()+'%')
            query.exec_()
        
        row = 0
        
        while query.next():
            title_col = query.value(0)
            description_col = query.value(1)
            created_at_col = query.value(2)
            
            #add values to Table
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(title_col))
            self.table.setItem(row, 1, QTableWidgetItem(description_col))
            self.table.setItem(row, 2, QTableWidgetItem(str(created_at_col)))
            
            row += 1
        
    def search_recipe(self):
        """
        Function called by the Search button. By default it simply calls the laod_table() function
        """
        print("Search Recipe")
        self.load_table()
        
    def show_mode_recipe(self):
        """
        Function called by the Open Button. It has a string to indicate which type of mode the window should open on.
        In this case when query the recipe it will open The Recipe Window.
        """
        self.show_or_update = "Show"
        self.open_recipe()
        
    def update_mode_recipe(self):
        """
        Function called by the Edit button and will tell the app which mode is. After search query for the recipe, 
        it will open th Create Window
        """
        self.show_or_update = "Update"
        self.open_recipe()
        
    def open_recipe(self):
        """
        This function is called to query information from the selected recipe and store its information inside a list.
        Then it will check which mode is so it passes the recipe to the correct window
        """
        if self.recipe_window.isVisible():
            self.recipe_window.hide()

        else:
            self.recipe_data_dic.clear()
            
            # Resets the recipe data dictionary
            selected_row = self.table.currentRow()
            self.recipe_data_dic = {'ingredient_list': [], 'category_list': []}
            
            if selected_row == -1:
                QMessageBox.warning(self, "No Data was chosen", "Please select a recipe to open")
                return
            
            query = QSqlQuery()
            
            recipe_title = self.table.item(selected_row,0).text()
            recipe_description = self.table.item(selected_row,1).text()
            
            # Getting all the basic information from the Recipe table
            query.exec_("SELECT * FROM Recipes WHERE title = ? AND description = ?")
            query.addBindValue(recipe_title)
            query.addBindValue(recipe_description)
            query.exec_()
            
            while query.next():
                self.recipe_data_dic["recipe_id"] = query.value(0)
                self.recipe_data_dic["title"] = query.value(1)
                self.recipe_data_dic["description"] = query.value(2)
                self.recipe_data_dic["Image"] = query.value(3)
                self.recipe_data_dic["instructions"] = query.value(4)
                self.recipe_data_dic["prep_time"] = query.value(5)
                self.recipe_data_dic["cook_time"] = query.value(6)
                self.recipe_data_dic["servings"] = query.value(7)
                self.recipe_data_dic["difficulty"] = query.value(8)
                self.recipe_data_dic["created_at"] = query.value(9)
            
            # Getting all the ingredients of the selected recipe from the database
            query.exec_("""
                    SELECT ri.quantity, ri.unit, i.name, i.category
                    FROM Recipes r
                    JOIN RecipeIngredients ri ON r.recipe_id = ri.recipe_id
                    JOIN Ingredients i ON ri.ingredient_id = i.ingredient_id
                    WHERE r.recipe_id = ?;
                    """)
            query.addBindValue(self.recipe_data_dic["recipe_id"])
            query.exec_()
            while query.next():
                ing_quantity = query.value(0)
                ing_unit = query.value(1)
                ing_name = query.value(2)
                ing_category = query.value(3)
                
                self.recipe_data_dic['ingredient_list'].append({'i_quantity': ing_quantity,  'i_unit': ing_unit, 'i_name' : ing_name, 'i_category': ing_category})
            
            
            # Getting all the categories of the selected recipe from the database
            query.exec_("""
                    SELECT c.name, c.description
                    FROM Recipes r
                    JOIN RecipeCategories rc ON r.recipe_id = rc.recipe_id
                    JOIN Categories c ON rc.category_id = c.category_id
                    WHERE r.recipe_id = ?;
                    """)
            query.addBindValue(self.recipe_data_dic["recipe_id"])
            query.exec_()
            while query.next():
                cat_name = query.value(0)
                cat_description = query.value(1)
                
                self.recipe_data_dic['category_list'].append({'c_name': cat_name,  'c_description': cat_description})
            
            
            # Checks if its Show mode or Edit mode
            if self.show_or_update == "Update":
                self.create_window.show()
                self.create_window.update_mode(self.recipe_data_dic)
                
            else:
                self.recipe_window.show()
                self.recipe_window.load_data(self.recipe_data_dic)
        
    def new_recipe(self):
        """
        Function called by the New Button to open the Create Window in Creation mode by default
        """
        if self.create_window.isVisible():
            self.create_window.hide()

        else:
            self.create_window.show()
            self.create_window.create_mode()
        
    def delete_recipe(self):
        """
        Function called by the delete button to delete from the table the selected recipe
        """
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "No Data was chosen", "Please select an Row to delete")
            return
        
        recipe_title = self.table.item(selected_row,0).text()
        recipe_description = self.table.item(selected_row,1).text()
        
        confirm = QMessageBox.question(self, "Are you sure?", "Delete Row?", QMessageBox.Yes | QMessageBox.No)
        
        if confirm == QMessageBox.No:
            return
        
        query = QSqlQuery()
        query.prepare("DELETE FROM Recipes WHERE title = ? AND description = ?")
        query.addBindValue(recipe_title)
        query.addBindValue(recipe_description)
        query.exec_()
        
        self.load_table()
        
    def table_order_toggle(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            if radioButton.order == "Ascending":
                self.table.sortByColumn(0, Qt.AscendingOrder)
            else:
                self.table.sortByColumn(0, Qt.DescendingOrder)
            
    def header_clicked(self, index: int):
        """
        Function called when clicking a table header that will display the table in ascending order alphabetically
        """
        self.table.sortByColumn(index, Qt.AscendingOrder)
        if index == 0 and self.asc_radio_button.isChecked() == False:
            self.asc_radio_button.setChecked(True)
        
    ###------ Menu Functions -----###
    def open_settings(self):
        if self.settings_window.isVisible():
            self.settings_window.hide()

        else:
            self.settings_window.load_settings(self.cookbook_settings) # Pass on a dictionary with the current settings
            self.settings_window.show()
            
    def table_alphabetic(self):
        self.header_clicked(0)