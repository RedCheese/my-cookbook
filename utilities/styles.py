import os
from PyQt5.QtWidgets import QApplication

# Default stylesheet as a fallback
cookbook_qss = """QWidget {
    background-color: #fdf6e3; /* light parchment color */
    font-family: "Georgia", "Times New Roman", serif;
    font-size: 14px;
    color: #4e342e; /* dark brown text */
}

/* Headings (e.g. Labels you use as titles) */
QLabel#title {
    font-size: 20px;
    font-weight: bold;
    color: #6d4c41; /* warm brown */
    border-bottom: 2px solid #d7ccc8;
    padding: 6px;
}

/* Buttons */
QPushButton {
    background-color: #fff3e0; /* light warm orange */
    border: 2px solid #d7ccc8;
    border-radius: 8px;
    padding: 6px 12px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #ffe0b2;
}

QPushButton:pressed {
    background-color: #ffcc80;
}

/* Line edits (for input fields) */
QLineEdit, QTextEdit {
    background-color: #fff8e1;
    border: 1px solid #d7ccc8;
    border-radius: 6px;
    padding: 4px;
}

/* Tables (if you list recipes) */
QTableWidget {
    background-color: #fffde7;
    border: 1px solid #d7ccc8;
    gridline-color: #d7ccc8;
}

QHeaderView::section {
    background-color: #ffe0b2;
    border: 1px solid #d7ccc8;
    padding: 4px;
    font-weight: bold;
}

/* Scrollbars (make them subtle like a notebook margin) */
QScrollBar:vertical {
    background: #f5f5dc;
    width: 12px;
}
QScrollBar::handle:vertical {
    background: #d7ccc8;
    border-radius: 6px;
    min-height: 20px;
}
"""

def load_cookbook_style(app: QApplication, filename="cookbook.qss", force_overwrite=False):
    """
    Ensure stylesheet file exists (optionally overwrite), 
    load it into the QApplication,
    and fall back to default style if file is missing/corrupted.
    """
    try:
        if force_overwrite or not os.path.exists(filename):
            with open(filename, "w", encoding="utf-8") as f:
                f.write(cookbook_qss)
            print(f"Created/overwritten {filename}")

        # Try loading from file
        with open(filename, "r", encoding="utf-8") as f:
            style = f.read().strip()

        if not style:
            raise ValueError("Stylesheet file is empty, falling back to default.")

        app.setStyleSheet(style)
        print(f"Applied stylesheet from {filename}")

    except Exception as e:
        # Fallback: apply built-in default style
        print(f"⚠️ Failed to load {filename}: {e}")
        print("Applying fallback style...")
        app.setStyleSheet(cookbook_qss)