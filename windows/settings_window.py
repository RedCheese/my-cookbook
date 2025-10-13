from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QLineEdit, QMessageBox) 

class SettingsWindow(QWidget):   
    def __init__(self, main_window):
        """
        Window with basic settings of the Cook book

        """
        super().__init__()
        
        self.main_window = main_window  # keep reference to the previous window
        
        self.setWindowTitle("Settings")
        
        ###------Obejcts-------###
        
        # Cookbook Name Objects
        self.settings_title_label = QLabel("Cookbook Name")
        self.settings_title_line = QLineEdit()
        
        # Buttons
        self.update_settings_btn = QPushButton("Update")
        self.update_settings_btn.clicked.connect(self.update_settings)
        
        ###------Layouts-------###
        self.master_layout = QVBoxLayout()
        
        self.row1 = QHBoxLayout()
        self.row2 = QHBoxLayout()
        
        # Row 1
        self.row1.addWidget(self.settings_title_label)
        self.row1.addWidget(self.settings_title_line)
        
        # Row 2
        self.row2.addWidget(self.update_settings_btn)
        
        # Master Layouts
        self.master_layout.addLayout(self.row1)
        self.master_layout.addLayout(self.row2)

        self.setLayout(self.master_layout)
        
    def update_settings(self):
        """
        First is gettings the Cookbook name from the main window and then settings its name with the new one from this window
        Then storing the new name in the main window's settings dictionary
        
        (self.main_window.settings.name) references the settings value initialized in the main window
        """
        self.main_window.title.setText(self.settings_title_line.text())
        self.main_window.settings.name = self.main_window.title.text()
        self.hide()
        
    def load_settings(self, settings_data: dict):
        print(settings_data)
        self.settings_title_line.setText(settings_data["cookbook_name"])