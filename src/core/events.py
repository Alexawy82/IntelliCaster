from copy import deepcopy
import time

from core import common


class Events:
    """A class to detect and report events.
    
    This class is used to detect and report events such as overtakes and
    incidents. It is run in a separate thread from the main thread and is
    responsible for updating the drivers list and the previous drivers list.
    """
    def __init__(self):
        """Initialize the Events object.

        This method initializes the Events object by creating an empty events
        list and setting the id counter to 0.

        Attributes:
            events (list): A list of events
            id_counter (int): The id of the next event to be added
        """
        # Initialize the events list and id counter
        self.events = []
        self.id_counter = 0

    def _add(self, type, description, focus=None):
        """Add a new event to the list.
        
        Args:
            type (str): The type of event
            description (str): A description of the event
            focus (int): The number of the driver to focus on
        """
        # Create a new event
        new_event = {
            "id": self.id_counter,
            "type": type,
            "description": description,
            "focus": focus,
            "timestamp": time.time()
        }

        # Add the event to the list
        self.events.append(new_event)

        # Increment the id counter
        self.id_counter += 1

    def _detect_overtakes(self):
        """Detect overtakes and add them to the events list.
        
        This method detects overtakes by comparing the current drivers list to
        the previous drivers list. If a driver's position has decreased, they
        have overtaken someone. If this is the case, the driver who was
        overtaken is found and an overtake event is added to the events list.
        This method also checks a few other conditions to make sure the overtake
        is legitimate.
        """
        # Go through all the drivers
        for driver in common.drivers:
            # Get this driver's previous information
            prev_driver = None
            for item in common.prev_drivers:
                if item["name"] == driver["name"]:
                    prev_driver = item
                    break

            # If a driver's position has decreased, they have overtaken someone
            if prev_driver and driver["position"] < prev_driver["position"]:
                # Find the driver whose position is 1 higher than this driver's
                overtaken = None
                for item in common.drivers:
                    if item["position"] == driver["position"] + 1:
                        overtaken = item
                        break
                
                # If no driver was found, don't report overtake
                if not overtaken:
                    continue

                # If either driver is in the pits, don't report overtake
                if driver["in_pits"] or overtaken["in_pits"]:
                    continue

                # If laps completed is negative (DNF), don't report overtake
                if driver["laps_completed"] < 0:
                    continue
                if overtaken["laps_completed"] < 0:
                    continue

                # If an legitimate overtake was found, add it to the events list
                driver_name = common.remove_numbers(driver["name"])
                overtaken_name = common.remove_numbers(overtaken["name"])
                description = (
                    f"{driver_name} overtook "
                    f"{overtaken_name} for "
                    f"P{driver['position']}"
                )
                self._add("overtake", description, driver["number"])

                # End this iteration of the loop
                break

    def _remove(self, id):
        """Remove an event from the list.
        
        Args:
            id (int): The id of the event to remove
        """
        # Remove the event from the list
        for event in self.events:
            if event["id"] == id:
                self.events.remove(event)

    def _update_drivers(self):
        """Update the drivers list.

        This method updates the drivers list by getting the latest data from the
        iRacing SDK and updating the drivers list accordingly.
        """
        # Get driver data from iRacing SDK
        driver_data = common.ir["DriverInfo"]["Drivers"]

        # Update the drivers list
        if common.ir["CarIdxPosition"] != []:
            for i, pos in enumerate(common.ir["CarIdxPosition"]):
                # Exclude the pace car and cars that don't exist
                if pos == 0: 
                    continue
                # Exclude disconnected drivers
                try:
                    if not driver_data[i]["UserName"]:
                        continue
                # If i is out of range, continue
                except:
                    continue

                # Find the driver in the drivers list at this index
                for j, driver in enumerate(common.drivers):
                    if driver["idx"] == i:
                        # Get the driver's last lap time
                        last_lap = common.ir["CarIdxLastLapTime"][i]
                        common.drivers[j]["last_lap"] = last_lap

                        # If there's no fastest lap, set it to the last lap
                        if driver["fastest_lap"] == None:
                            common.drivers[j]["fastest_lap"] = last_lap
                        
                        # If the last lap is faster than the fastest lap, update
                        elif last_lap < driver["fastest_lap"]:
                            common.drivers[j]["fastest_lap"] = last_lap

                        # Update percentage of lap completed
                        lap_percent = common.ir["CarIdxLapDistPct"][i]
                        common.drivers[j]["lap_percent"] = lap_percent

                        # Update laps started and completed
                        started = common.ir["CarIdxLap"][i]
                        completed = common.ir["CarIdxLapCompleted"][i]
                        common.drivers[j]["laps_started"] = started
                        common.drivers[j]["laps_completed"] = completed

                        # Update gap to leader
                        gap_to_leader = common.ir["CarIdxF2Time"][i]
                        common.drivers[j]["gap_to_leader"] = gap_to_leader

                        # Update pits status
                        in_pits = common.ir["CarIdxOnPitRoad"][i]
                        common.drivers[j]["in_pits"] = in_pits

                        # Update on track status
                        if common.ir["CarIdxLapDistPct"][i] > 0:
                            common.drivers[j]["on_track"] = True
                        else:
                            common.drivers[j]["on_track"] = False

                        # Update incidents
                        incidents = driver_data[i]["CurDriverIncidentCount"]
                        common.drivers[j]["incidents"] = incidents

        # Sort the list by current position if race has started
        if common.race_started:
            common.drivers.sort(
                key=lambda x: x["laps_completed"] + x["lap_percent"],
                reverse=True
            )

            # Update the positions
            for i, driver in enumerate(common.drivers):
                common.drivers[i]["position"] = i + 1
                
        # Otherwise, sort by grid position
        else:
            common.drivers.sort(key=lambda x: x["grid_position"])

    def get_next_event(self):
        """Pick the next event to report.
        
        Returns:
            dict: The next event to report
        """
        # If there are no events, return None
        if not self.events:
            return None
        
        # Sort the events list by timestamp, with the most recent first
        self.events.sort(key=lambda x: x["timestamp"], reverse=True)

        # Return the first event in the list and remove it
        event = self.events[0]
        self._remove(event["id"])
        return event
    
    def run(self):
        """Run the events thread.

        This method runs the events thread, which detects events and adds them
        to the events list. It also updates the drivers list and the previous
        drivers list.
        """
        # Keep running until told to stop
        while common.running:
            # Update the drivers list
            self._update_drivers()

            # Detect events
            self._detect_overtakes()

            # Update the previous drivers list
            common.prev_drivers = deepcopy(common.drivers)

            # Remove old events
            max_hist_len = float(common.settings["system"]["event_hist_len"])
            for event in self.events:
                if time.time() - event["timestamp"] > max_hist_len:
                    self._remove(event["id"])

            # Wait the amount of time specified in the settings
            time.sleep(float(common.settings["system"]["events_update_freq"]))