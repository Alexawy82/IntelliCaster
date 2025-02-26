"""
Module: camera.py

This module manages camera views for IntelliCaster.
It provides functions to get available cameras and switch between them.
"""

import random
from core import common

class Camera:
    def __init__(self):
        """Initialize the Camera class.
        
        Sets the current camera and all available cameras. If iRacing is not
        connected yet, it will defer loading cameras until needed.
        """
        self.current_camera = None
        self.cameras = []
        # Don't try to load cameras immediately, only when requested
    
    def _get_cameras(self):
        """Get all cameras from iRacing.
        
        Returns:
            A list of all available cameras.
        """
        cameras = []
        
        # Check if iRacing is connected
        if not common.ir or not common.ir.is_connected:
            common.app.add_message("iRacing not connected. Camera information unavailable.")
            return []
            
        try:
            # Get cameras from iRacing
            if common.ir.is_initialized and common.ir.is_connected:
                for camera in common.ir["CameraInfo"]["Groups"]:
                    cameras.append(camera)
            
            common.app.add_message(f"Found {len(cameras)} cameras.")
        except (KeyError, AttributeError) as e:
            common.app.add_message(f"Error getting cameras: {str(e)}")
            return []
            
        return cameras
    
    def choose_random_camera(self, car_idx=0):
        """Choose a random camera and switch to it.
        
        Args:
            car_idx: The car to focus on.
        """
        # Lazy loading of cameras if we don't have them yet
        if not self.cameras:
            self.cameras = self._get_cameras()
            
        # If we still don't have cameras, we can't do anything
        if not self.cameras:
            return
            
        # Choose a random camera
        camera_idx = random.randint(0, len(self.cameras) - 1)
        self.current_camera = self.cameras[camera_idx]
        
        # Switch to the camera
        self.switch_camera(camera_idx, car_idx)
    
    def switch_camera(self, camera_idx, car_idx=0):
        """Switch to a specific camera.
        
        Args:
            camera_idx: The index of the camera to switch to.
            car_idx: The car to focus on.
        """
        # Check if iRacing is connected
        if not common.ir or not common.ir.is_connected:
            common.app.add_message("iRacing not connected. Cannot switch camera.")
            return
            
        try:
            # Switch to the camera
            common.ir.cam_switch_pos(camera_idx, car_idx, 0)
        except Exception as e:
            common.app.add_message(f"Error switching camera: {str(e)}")