"""
Module: config_manager.py

This module manages the configuration settings for IntelliCaster.
It loads and saves settings using a configuration file (e.g., settings.ini).
"""

import configparser
import os

class ConfigManager:
    def __init__(self, filename="settings.ini"):
        self.filename = filename
        self.config = configparser.ConfigParser()
        self.load_config()
    
    def load_config(self):
        """
        Loads configuration from the file. If the file does not exist,
        create a default configuration.
        """
        if os.path.exists(self.filename):
            self.config.read(self.filename)
        else:
            self.config["keys"] = {"openai_api_key": "", "elevenlabs_api_key": ""}
            self.config["general"] = {
                "telemetry_threshold": "0.5",
                "director_update_freq": "0.1",
                "event_hist_len": "30",
                "events_update_freq": "0.5"
            }
            self.save_config()
    
    def get(self, section, key, fallback=None):
        return self.config.get(section, key, fallback=fallback)
    
    def set(self, section, key, value):
        if section not in self.config:
            self.config[section] = {}
        self.config[section][key] = value
    
    def save_config(self):
        with open(self.filename, "w") as configfile:
            self.config.write(configfile)
    
    def get_config(self):
        return self.config

# Example usage:
# cm = ConfigManager()
# threshold = cm.get("general", "telemetry_threshold")
# cm.set("general", "telemetry_threshold", "0.7")
# cm.save_config()