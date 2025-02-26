"""
Module: events.py

Enhanced event detection for IntelliCaster.
This module processes race telemetry data (stored in common.drivers and common.prev_drivers),
detecting key events such as overtakes and stops using adaptive thresholds and smoothing.
Detected events are stored with a timestamp and description.
"""

import time
from copy import deepcopy
from core import common
from core import telemetry_filters  # Smoothing functions (e.g., moving_average_filter)

class Events:
    def __init__(self):
        self.events = []
        self.id_counter = 0

    def _add_event(self, event_type, description, driver, lap_percent=None):
        """
        Create and store an event.
        """
        event = {
            "id": self.id_counter,
            "type": event_type,
            "description": description,
            "driver": driver,
            "lap_percent": lap_percent,
            "timestamp": time.time()
        }
        self.events.append(event)
        self.id_counter += 1

    def _detect_overtakes(self):
        """
        Compare current and previous driver positions to detect overtakes.
        Uses adaptive logic based on changes in positions and lap percentages.
        """
        detected_events = []
        if not common.prev_drivers:
            return detected_events

        for curr in common.drivers:
            # Locate previous data for the same driver.
            prev = next((d for d in common.prev_drivers if d.get("name") == curr.get("name")), None)
            if not prev:
                continue

            # Check if current position is better (lower number) than before.
            if curr.get("position", 999) < prev.get("position", 999):
                # Calculate the difference in position.
                pos_diff = prev.get("position", 999) - curr.get("position", 999)
                # Use a simple adaptive threshold: trigger an event if a driver gains at least one position.
                if pos_diff >= 1:
                    description = (f"{curr.get('name')} moved from position {prev.get('position')} "
                                   f"to {curr.get('position')} at lap progress {curr.get('lap_percent', 0):.2f}.")
                    self._add_event("overtake", description, curr.get("name"), curr.get("lap_percent"))
                    detected_events.append({
                        "type": "overtake",
                        "description": description,
                        "driver": curr.get("name"),
                        "lap_percent": curr.get("lap_percent", 0),
                        "timestamp": time.time()
                    })
        return detected_events

    def _detect_stopped(self):
        """
        Detect if a driver appears to have stopped by comparing progress in total distance.
        Uses a threshold that can be adjusted based on track length or average speeds.
        """
        detected_events = []
        if not common.prev_drivers:
            return detected_events

        for curr in common.drivers:
            prev = next((d for d in common.prev_drivers if d.get("name") == curr.get("name")), None)
            if not prev:
                continue

            # Calculate the difference in total distance covered.
            distance_diff = curr.get("total_dist", 0) - prev.get("total_dist", 0)
            # Adaptive threshold: here we use 1.0 as a placeholder; in practice, this might depend on track length.
            if distance_diff < 1.0:
                description = f"{curr.get('name')} shows minimal progress in distance, possibly stopped."
                self._add_event("stopped", description, curr.get("name"), curr.get("lap_percent", 0))
                detected_events.append({
                    "type": "stopped",
                    "description": description,
                    "driver": curr.get("name"),
                    "lap_percent": curr.get("lap_percent", 0),
                    "timestamp": time.time()
                })
        return detected_events

    def get_events(self):
        """
        Retrieve and return the combined list of detected events, sorted by timestamp.
        After retrieval, the internal event list is refreshed.
        """
        events_overtake = self._detect_overtakes()
        events_stopped = self._detect_stopped()
        all_events = events_overtake + events_stopped
        all_events.sort(key=lambda e: e["timestamp"], reverse=True)
        # Optionally remove duplicates.
        unique_events = self._remove_duplicates(all_events)
        self.events = unique_events
        return unique_events

    def _remove_duplicates(self, events):
        """
        Remove events with duplicate descriptions.
        """
        seen = set()
        unique = []
        for event in events:
            desc = event.get("description", "")
            if desc not in seen:
                unique.append(event)
                seen.add(desc)
        return unique

    def update_previous_drivers(self):
        """
        Update the previous driver snapshot with the current driver state.
        """
        common.prev_drivers = deepcopy(common.drivers)


# For testing purposes:
if __name__ == "__main__":
    import time

    # Simulate previous telemetry data.
    common.prev_drivers = [
        {"name": "Driver A", "position": 2, "lap_percent": 0.70, "total_dist": 500},
        {"name": "Driver B", "position": 1, "lap_percent": 0.72, "total_dist": 510},
        {"name": "Driver C", "position": 3, "lap_percent": 0.65, "total_dist": 490}
    ]
    # Simulate updated telemetry data.
    common.drivers = [
        {"name": "Driver A", "position": 1, "lap_percent": 0.75, "total_dist": 505},
        {"name": "Driver B", "position": 2, "lap_percent": 0.73, "total_dist": 512},
        {"name": "Driver C", "position": 3, "lap_percent": 0.66, "total_dist": 492}
    ]
    
    events_detector = Events()
    detected = events_detector.get_events()
    for event in detected:
        print(event)
