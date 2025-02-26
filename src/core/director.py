import time
import threading
from core import common, events, commentary, camera
from core import telemetry_filters, config_manager, database_manager

class Director:
    def __init__(self):
        # Initialize running flag
        self.running = False

        # Initialize configuration manager
        self.config_manager = config_manager.ConfigManager()
        
        # Initialize database manager
        self.db_manager = database_manager.DatabaseManager()
        
        # Initialize event detection (existing logic from events.py)
        self.event_detector = events.Events()
        
        # Initialize commentary generator (AI functionality)
        self.commentary_generator = commentary.CommentaryGenerator()
        
        # Initialize camera manager for dynamic view switching
        self.camera_manager = camera.Camera()
        
        # Set update frequency from configuration; default fallback is 0.1 seconds
        self.update_freq = float(self.config_manager.get("general", "director_update_freq", fallback="0.1"))

    def run(self):
        """Main loop that orchestrates telemetry data processing, event detection,
        commentary generation, and camera management."""
        self.running = True
        while self.running:
            # Fetch telemetry data (here, simulated; in practice, this comes from common.ir)
            telemetry_data = self.fetch_telemetry_data()
            
            # Apply smoothing to telemetry data using our telemetry_filters module
            smoothed_data = {}
            for key, value in telemetry_data.items():
                if isinstance(value, list):
                    smoothed_data[key] = telemetry_filters.moving_average_filter(value)
                else:
                    smoothed_data[key] = value

            # Log raw telemetry data to the database
            current_timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            self.db_manager.insert_telemetry(current_timestamp, telemetry_data)
            
            # Update global driver data (simulate integration with iRacing SDK data)
            common.drivers = telemetry_data.get("drivers", [])
            
            # Detect events using our event detector (which compares current and previous driver states)
            detected_events = self.event_detector.get_events()
            for event in detected_events:
                self.db_manager.insert_event(
                    event_type=event.get("type", "unknown"),
                    description=event.get("description", ""),
                    driver=event.get("driver", ""),
                    timestamp=event.get("timestamp", current_timestamp)
                )
            
            # If events are detected, generate commentary text using our AI module
            if detected_events:
                commentary_text = self.commentary_generator.generate(detected_events, {"league": common.context.get("league", {})})
                # (Optional) Here we could pass commentary_text to the TTS pipeline for voice synthesis
            
            # Update camera view based on race conditions (example: switching to a random camera for demonstration)
            # In a real scenario, the logic would consider which driver is in the lead or where key events occur.
            if common.drivers:
                # For simplicity, use the first driver's index (this should be refined)
                self.camera_manager.choose_random_camera(car_idx=common.drivers[0].get("position", 1))
            
            time.sleep(self.update_freq)

    def stop(self):
        """Stop the director's main loop."""
        self.running = False

    def fetch_telemetry_data(self):
        """
        Simulate fetching telemetry data.
        In the actual implementation, this data would be fetched from the iRacing SDK (common.ir).
        """
        # Dummy telemetry data example; replace with real sensor/SDK data as available.
        return {
            "drivers": [
                {"name": "Driver A", "lap_percent": 0.75, "position": 1},
                {"name": "Driver B", "lap_percent": 0.73, "position": 2},
                {"name": "Driver C", "lap_percent": 0.60, "position": 3}
            ],
            "speed": [100, 102, 98, 101, 99],
            "lap_times": [90.5, 89.8, 90.1, 90.3, 90.0]
        }

if __name__ == "__main__":
    director = Director()
    director_thread = threading.Thread(target=director.run, daemon=True)
    director_thread.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        director.stop()
        print("Director stopped.")
