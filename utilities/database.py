import sys
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtWidgets import QMessageBox

class RecipeDatabase:
    def createDatabase(self):
        # Create our database
        database = QSqlDatabase.addDatabase("QSQLITE")
        database.setDatabaseName("recipe_book.db")
        if not database.open():
            QMessageBox.critical(None, "Error", "Could not open your database")
            sys.exit(1)
            
        query = QSqlQuery()
        print("Init Test")
        
        # Create Recipes Table
        query.exec_("""
                    CREATE TABLE IF NOT EXISTS Recipes(
                        recipe_id VARCHAR(32) PRIMARY KEY,
                        title VARCHAR(200) NOT NULL,
                        description TEXT,
                        Image LONGBLOB,
                        instructions LONGTEXT NOT NULL,
                        prep_time INT,   -- minutes
                        cook_time INT,   -- minutes
                        servings INT,
                        difficulty VARCHAR(20),  -- e.g. 'easy', 'medium', 'hard'
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                    """)
        
        # Create Ingredients table
        query.exec_("""
                    CREATE TABLE IF NOT EXISTS Ingredients(
                        ingredient_id VARCHAR(12) PRIMARY KEY,
                        name VARCHAR(150) NOT NULL,
                        category VARCHAR(100),
                        unit VARCHAR(50)   -- default measurement, e.g., grams, ml, pcs
                    )
                    """)
        
        # Create RecipeIngredients (join table)
        query.exec_("""
                    CREATE TABLE IF NOT EXISTS RecipeIngredients(
                        recipe_id VARCHAR(16) NOT NULL,
                        ingredient_id VARCHAR(12) NOT NULL,
                        quantity DECIMAL(10,2),
                        unit VARCHAR(50),   -- overrides default unit if needed
                        PRIMARY KEY (recipe_id, ingredient_id),
                        FOREIGN KEY (recipe_id) REFERENCES Recipes(recipe_id) ON DELETE CASCADE,
                        FOREIGN KEY (ingredient_id) REFERENCES Ingredients(ingredient_id) ON DELETE CASCADE
                    )
                    """)
        
        # Create Categories table
        query.exec_("""
                    CREATE TABLE IF NOT EXISTS Categories(
                        category_id SERIAL PRIMARY KEY,
                        name VARCHAR(100) UNIQUE NOT NULL,
                        description TEXT
                    )
                    """)
        
        # Create RecipeCategories (join table)
        query.exec_("""
                    CREATE TABLE IF NOT EXISTS RecipeCategories(
                        recipe_id VARCHAR(16) NOT NULL,
                        category_id INT NOT NULL,
                        PRIMARY KEY (recipe_id, category_id),
                        FOREIGN KEY (recipe_id) REFERENCES Recipes(recipe_id) ON DELETE CASCADE,
                        FOREIGN KEY (category_id) REFERENCES Categories(category_id) ON DELETE CASCADE
                    )
                    """)
        
        # Create Tags table
        query.exec_("""
                    CREATE TABLE IF NOT EXISTS Tags(
                        tag_id SERIAL PRIMARY KEY,
                        name VARCHAR(50) UNIQUE NOT NULL
                    )
                    """)
        
        # Create RecipeTags (join table)
        query.exec_("""
                    CREATE TABLE IF NOT EXISTS RecipeTags(
                        recipe_id VARCHAR(16) NOT NULL,
                        tag_id INT NOT NULL,
                        PRIMARY KEY (recipe_id, tag_id),
                        FOREIGN KEY (recipe_id) REFERENCES Recipes(recipe_id) ON DELETE CASCADE,
                        FOREIGN KEY (tag_id) REFERENCES Tags(tag_id) ON DELETE CASCADE
                    )
                    """)
        
    def insertCategoryValues(self):
        query = QSqlQuery()
        
        # Insert standard values into Category
        query.exec_("""
                    INSERT into Categories(category_id, name, description)
                    VALUES (1,'Breakfast', 'Morning meals'),
                           (2,'Lunch', 'Meal in the middle of the day'),
                           (3,'Dinner or MainCourse', 'The Main meal of the day'),
                           (4,'Appetizer', 'The dish before the Main Course'),
                           (5,'Snack', 'Simple meals to satiate your hunger over the day'),
                           (6,'Soup', 'Dishes in liquid form'),
                           (7,'Stew', 'Soups with chunks of meat in them'),
                           (8,'Salad', 'Dishes without meat'),
                           (9,'Side Dish', 'Dishes that usually come alongside the main dish'),
                           (10,'Dessert', 'Sweet dishes served after meals'),
                           (11,'Baked Goods', 'Food derivated of Bakery'),
                           (12,'Beverages', 'Drinks and Juices')
                    """)
    
    def insertIngredientValues(self):
        query = QSqlQuery()
        
        query.exec_("""
                    INSERT INTO Ingredients (ingredient_id, name, category, unit)
                    VALUES ('ING_TYU76A','Flour', 'Baking', 'grams'),
                           ('ING_TYU75A','Sugar', 'Baking', 'grams'),
                           ('ING_TYU74A','Butter', 'Dairy', 'grams'),
                           ('ING_TYU73A','Egg', 'Dairy', 'pcs'),
                           ('ING_TYU72A','Milk', 'Dairy', 'ml'),
                           ('ING_TYU71A','Salt', 'Spice', 'grams')
                    """)
        
    def insertRecipeValues(self):
        query = QSqlQuery()
        
        query.exec_("""
                    INSERT INTO Recipes (recipe_id, title, description, instructions, prep_time, cook_time, servings, difficulty)
                    VALUES ('REC_HT67TYUH',
                            'Pancakes', 
                           'Fluffy homemade pancakes', 
                           '1. Mix dry ingredients.\n2. Add wet ingredients.\n3. Cook on skillet until golden brown.', 
                           10, 
                           15, 
                           4, 
                           '1 - easy')
                    """)
        
    def insertTest(self):

        query = QSqlQuery()
        
        query.exec_("""
                    INSERT INTO RecipeIngredients (recipe_id, ingredient_id, quantity, unit)
                    VALUES ('REC_HT67TYUH', 'ING_TYU76A', 200, 'grams'),   -- Flour
                          ('REC_HT67TYUH', 'ING_TYU75A', 50, 'grams'),    -- Sugar
                          ('REC_HT67TYUH', 'ING_TYU74A', 30, 'grams'),    -- Butter
                          ('REC_HT67TYUH', 'ING_TYU73A', 2, 'pcs'),       -- Eggs
                          ('REC_HT67TYUH', 'ING_TYU72A', 250, 'ml'),      -- Milk
                          ('REC_HT67TYUH', 'ING_TYU71A', 2, 'grams')     -- Salt
                    """)
        
        query.exec_("""
                    INSERT INTO RecipeCategories (recipe_id, category_id)
                    VALUES ('REC_HT67TYUH', 1),   -- Breakfast
                          ('REC_HT67TYUH', 10)    -- Dessert
                    """)
        print("Inserted test")