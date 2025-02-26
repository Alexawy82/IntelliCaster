"""
Module: database_manager.py

This module handles persistent storage for IntelliCaster using SQLite.
It provides functions to initialize the database, and to insert and update telemetry logs,
detected events, and user settings.
"""

import sqlite3
import os
import json

class DatabaseManager:
    def __init__(self, db_filename="intellicaster.db"):
        self.db_filename = db_filename
        self.connection = None
        self.connect()
        self.initialize_database()
    
    def connect(self):
        self.connection = sqlite3.connect(self.db_filename)
        self.connection.row_factory = sqlite3.Row
    
    def initialize_database(self):
        cursor = self.connection.cursor()
        # Table for telemetry logs
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS telemetry (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                data TEXT
            )
        """)
        # Table for events
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT,
                description TEXT,
                driver TEXT,
                timestamp TEXT
            )
        """)
        # Table for settings
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT UNIQUE,
                value TEXT
            )
        """)
        self.connection.commit()
    
    def insert_telemetry(self, timestamp, data):
        """
        Insert a telemetry record into the database.
        :param timestamp: String representing the timestamp.
        :param data: Telemetry data (will be stored as JSON string).
        """
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO telemetry (timestamp, data) VALUES (?, ?)", 
                       (timestamp, json.dumps(data)))
        self.connection.commit()
    
    def insert_event(self, event_type, description, driver, timestamp):
        """
        Insert an event record into the database.
        :param event_type: Type of the event (e.g., 'overtake', 'stopped').
        :param description: A descriptive message.
        :param driver: Identifier for the driver involved.
        :param timestamp: Event timestamp.
        """
        cursor = self.connection.cursor()
        cursor.execute("""
            INSERT INTO events (event_type, description, driver, timestamp) 
            VALUES (?, ?, ?, ?)
        """, (event_type, description, driver, timestamp))
        self.connection.commit()
    
    def update_setting(self, key, value):
        """
        Insert or update a setting.
        :param key: Setting name.
        :param value: Setting value.
        """
        cursor = self.connection.cursor()
        cursor.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, value))
        self.connection.commit()
    
    def get_setting(self, key, default=None):
        """
        Retrieve a setting value.
        :param key: Setting name.
        :param default: Default value if setting is not found.
        :return: The setting value or default.
        """
        cursor = self.connection.cursor()
        cursor.execute("SELECT value FROM settings WHERE key=?", (key,))
        row = cursor.fetchone()
        return row["value"] if row else default
    
    def close(self):
        if self.connection:
            self.connection.close()

# Example usage:
# db = DatabaseManager()
# db.insert_event("overtake", "Driver A overtook Driver B", "Driver A", "2025-02-26 12:00:00")
# db.update_setting("telemetry_threshold", "0.7") 