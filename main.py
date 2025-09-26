from cookbook_app import Cookbook
from database import RecipeDatabase
from PyQt5.QtWidgets import QApplication


if __name__ == "__main__":
    RecipeDatabase().createDatabase()
    RecipeDatabase().insertCategoryValues()
    app = QApplication([])
    main = Cookbook()
    main.show()
    app.exec_()