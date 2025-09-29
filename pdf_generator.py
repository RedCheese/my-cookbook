import os
import platform
import subprocess
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, ListFlowable, ListItem


class PDFGenerator:
        
    def generate_recipe_pdf(self, recipe: dict, open_mode="folder"):
        """
        Generate a PDF file for a recipe using reportlab.
    
        Parameters:
            recipe (dict): {
                "title": str,
                "Image": str (path to image file, optional)
                "description": str,
                "prep_time": str,
                "cook_time": str,
                "servings": str,
                "difficulty": str,
                "categories": list of str, #{"c_name": str, "c_description": str}
                "ingredient_list": list of dicts, # {"i_name": str, "i_quantity": int, "i_unit": str, "i_category": str}
                "instructions": str
            }
            filename (str): Output PDF filename
        """
        
        # Setup document
        filename = recipe["title"]+".pdf"
        doc = SimpleDocTemplate(filename, pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []
        
        # Title
        elements.append(Paragraph(recipe.get("title", "Untitled Recipe"), styles['Title']))
        elements.append(Spacer(1, 12))
        
        # Image
        image_path = recipe.get("Image")
        if image_path:
            try:
                img = Image(image_path)
                img._restrictSize(400, 300)  # resize if too large
                elements.append(img)
                elements.append(Spacer(1, 12))
            except Exception as e:
                elements.append(Paragraph(f"[Image could not be loaded: {e}]", styles['Normal']))
                elements.append(Spacer(1, 12))
        
        # Description
        desc = recipe.get("description")
        if desc:
            elements.append(Paragraph(desc, styles['Italic']))
            elements.append(Spacer(1, 12))
        
        # Recipe metadata (prep time, cook time, servings, difficulty)
        meta_data = [
            ["Prep Time:", recipe.get("prep_time", "N/A")],
            ["Cook Time:", recipe.get("cook_time", "N/A")],
            ["Servings:", recipe.get("servings", "N/A")],
            ["Difficulty:", recipe.get("difficulty", "N/A")]
        ]
        table = Table(meta_data, hAlign="LEFT", colWidths=[100, 300])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LINEBELOW', (0, 0), (-1, -1), 0.25, colors.grey),
        ]))
        elements.append(table)
        elements.append(Spacer(1, 12))
        
        # Categories
        categories = recipe.get("category_list", [])
        if categories:
            formatted_categories = []
            for cat in categories:
                formatted_categories.append(cat["c_name"])
            elements.append(Paragraph("Categories: " + ", ".join(formatted_categories), styles['Normal']))
            elements.append(Spacer(1, 12))
        
        # Ingredients
        elements.append(Paragraph("Ingredients:", styles['Heading2']))
        ingredients = recipe.get("ingredient_list", [])
        if ingredients:
            formatted_ingredients = []
            for ing in ingredients:
                qty = ing.get("i_quantity", "")
                unit = ing.get("i_unit", "")
                name = ing.get("i_name", "")
                category = ing.get("i_category", "")
            
                # Format: "200 g spaghetti (Pasta)"
                line = f"{qty} {unit} of {name}".strip()
                if category:
                    line += f" ({category})"
            
                formatted_ingredients.append(ListItem(Paragraph(line, styles['Normal'])))
        
            ingredient_list = ListFlowable(formatted_ingredients, bulletType='bullet')
            elements.append(ingredient_list)
        else:
            elements.append(Paragraph("No ingredients listed.", styles['Normal']))
        elements.append(Spacer(1, 15))
        
        # Instructions
        elements.append(Paragraph("Instructions:", styles['Heading2']))
        instructions = recipe.get("instructions", "")
        if instructions:
            elements.append(Paragraph(instructions, styles['Normal']))
        else:
            elements.append(Paragraph("No instructions provided.", styles['Normal']))
        
        # Build PDF
        doc.build(elements)
        abs_path = os.path.abspath(filename)
        print(f"PDF generated: {abs_path}")
    
        # Handle opening after generation
        system = platform.system()
        if open_mode == "folder":
            try:
                if system == "Windows":
                    subprocess.run(["explorer", "/select,", abs_path])
                elif system == "Darwin":  # macOS
                    subprocess.run(["open", "-R", abs_path])
                else:  # Linux
                    subprocess.run(["xdg-open", os.path.dirname(abs_path)])
            except Exception as e:
                print(f"Could not open folder: {e}")
        
        elif open_mode == "file":
            try:
                if system == "Windows":
                    os.startfile(abs_path)  # Windows-only
                elif system == "Darwin":  # macOS
                    subprocess.run(["open", abs_path])
                else:  # Linux
                    subprocess.run(["xdg-open", abs_path])
            except Exception as e:
                print(f"Could not open file: {e}")
