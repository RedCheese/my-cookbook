import string
import secrets
import os
from PyQt5.QtWidgets import QFileDialog

# Utiltiy Functions
def generate_id(prefix: str = "", length: int = 8) -> str:
        """Generate a random alphanumeric ID with an optional prefix.
        
            # For a recipe
            recipe_id = generate_id(prefix="REC_", length=8)
            print(recipe_id)   # e.g. "REC_J9X2P7QK"
            
            # For an ingredient
            ingredient_id = generate_id(prefix="ING_", length=6)
            print(ingredient_id)  # e.g. "ING_7KF9QZ"
        """
        
        alphabet = string.ascii_uppercase + string.digits
        random_part = ''.join(secrets.choice(alphabet) for _ in range(length))
        return f"{prefix}{random_part}"
    
def working_directory() -> str:
        """
            Function to get the path directory of an image type
        """
        #current_dir = os.path.dirname(os.path.abspath(__file__))
        #current_dir = Path(__file__).absolute()
        #current_dir = Path().absolute() #---- C:\Users\User
        current_dir = os.path.abspath(os.getcwd()) 
        working_directory = QFileDialog.getOpenFileName(None, "Open File",
                                                current_dir,
                                                "Images (*.png *.jpg *.jpeg *.svg)")

        if working_directory:
            return working_directory[0]
        else:
            return