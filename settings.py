import os
import json

class SettingsManager:
    def __init__(self, filename="settings.json", defaults=None):
        self.filename = filename
        self.defaults = defaults or {
            "name": "My Cookbook"
        }
        self._settings = self._load()

    def _load(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as f:
                    return json.load(f)
            except (json.JSONDecodeError, OSError):
                print("Settings file corrupted or unreadable. Using defaults.")
        return self.defaults.copy()

    def save(self):
        try:
            with open(self.filename, "w") as f:
                json.dump(self._settings, f, indent=4)
        except OSError as e:
            print(f"Error saving settings: {e}")

    def reset(self):
        """Reset settings to defaults and save."""
        self._settings = self.defaults.copy()
        self.save()

    def __getattr__(self, name):
        if name in self._settings:
            return self._settings[name]
        raise AttributeError(f"No setting named '{name}'")

    def __setattr__(self, name, value):
        # Allow normal attributes
        if name in {"filename", "defaults", "_settings"}:
            super().__setattr__(name, value)
        elif name in self._settings:
            self._settings[name] = value
            self.save()  # Auto-save when changed
        else:
            raise AttributeError(f"No setting named '{name}'")

    def __repr__(self):
        return f"SettingsManager({self._settings})"