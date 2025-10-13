# Class to handle lists of ingredients
from fractions import Fraction
import re

class ListfIngredientsHandler:
    def main_function(self, ing_list: str):
        """
        Main function that will handle the conversion of the string into a list of lists with the correct format.

        e.g. Input:
        2 cups warm milk
        1 tbsp sugar
        1/2 tsp salt

        It will return a list of lists in this format:
        [[quantity: float, unit: str, name: str],
         [quantity: float, unit: str, name: str],
         etc...]
        e.g.:
        [[2.0, "cups", "warm milk"],    
         [1.0, "tbsp", "sugar"],
         [0.5, "tsp", "salt"]]

        """
        
        ingredients_list = self.ingredients_to_list(ing_list)
        
        formatted_ingredients_list = []
        
        try:
            for ing in ingredients_list:
                new_ing = ing.split(" ", 2)
                is_number = self.check_fraction(new_ing[1]) # Calls the method to check if the element is a fraction or number

                if is_number: # If True
                    new_ing = self.combine_elements(ing) # Will take this ingredient to combine first two elements as one

                new_ing[0] = self.convert_to_number(new_ing[0])#convert the first element into a float number
                formatted_ingredients_list.append(new_ing)

            return formatted_ingredients_list
        except IndexError:
            print("Error converting the list. Please add it correctly")
            return
    
    def ingredients_to_list(self, text: str) -> list:
        """
        Function that turns the string into a list with each individual element containing an ingredient
        """
        items = []
        for line in text.splitlines():
            # Remove leading/trailing spaces and common bullet symbols
            cleaned = re.sub(r'^\s*[-*•]\s*', '', line.strip())
            if cleaned:  # ignore empty lines
                items.append(cleaned)
        return items
    
    def check_fraction(self, string: str) -> bool:
        """
        Function that will check if is a a fraction string e.g. 1/2 . Will first split into indivisdual chaarcters, 
        then will check if the first and third element are numbers, confirming that is a fraction so will return True for
        another oepration to fix it since the second element of the ignredient lsit needs to be a unit, not a number/fraction.
        """
        y = list(string) # string = "1/2" y = ["1", "/", "2"]
        a = y[0].isnumeric()
        b = y[2].isnumeric()
        
        if a and b and y[1] == "/":
            return True
        else:
            return False
        
    def check_decimal(self, string: str) -> bool:
        """
        Function that checks if the number is a decimal or float
        """
        try:
            val = float(string)
            return True
        except ValueError:
            return False
        
    def check_trace(self, string: str) -> bool:
        """
        Checks if the string has " - " divding the numbers
        """
        y = list(string)
        a = y[0].isnumeric()
        b = y[2].isnumeric()
        
        if a and b and y[1] == "-":
            return True
        else:
            return False
        
    def check_doubles(self, string: str) -> bool:
        """
        Check if the element contains two numbers. It splits into a new lsit and checks if it has two elements
        """
        y = string.split()
        if len(y) == 2:
            return True
        else:
            return False
        
    def combine_elements(self, ingredient: list) -> list:
        """
        Combine the first two elements of the list into one
        """
        #print(ingredient)
        temp_ing = ingredient.split(" ", 3)
        other_temp_ing = [' '.join(temp_ing[0:2])]
        #print(other_temp_ing)
        temp_ing = other_temp_ing + temp_ing[2:]
        #print(temp_ing)
        return temp_ing
        
    def convert_to_number(self, element: str) -> float:
        
        try:
            if element.isnumeric():
                return float(element)
            elif self.check_decimal(element):
                return float(element)
            elif self.check_fraction(element):
                a = Fraction(element)
                b = "{:.1f}".format(float(a))
                return float(b)
            elif self.check_trace(element):
                ele = (int(element[0]) + int(element[2])) / 2
                float_ele = "{:.1f}".format(ele)
                return float(float_ele)
            elif self.check_doubles(element):
                new_list = element.split()
                a = float(new_list[0])
                b = Fraction(new_list[1])
                return  a + float(b)
            else:
                return 0.0
        except ValueError:
            #QMessageBox.warning(self, "Error converting the list", "Please add it correctly")
            print("Error converting the list. Please add it correctly")
            return