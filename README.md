# IntelliCaster

**IntelliCaster** is an open-source AI-powered tool that adds dynamic, immersive voice commentary to iRacing race replays. It integrates advanced text generation (using OpenAI models) and high-quality text-to-speech (via ElevenLabs) with real-time race telemetry and event detection to create engaging, broadcast-style commentary. Our modular design makes IntelliCaster efficient, cost-effective, and open for community collaboration and enhancements.

## Overview

IntelliCaster is built using a layered architecture:

- **Front End:**  
  - Developed with CustomTkinter, it provides a user-friendly interface with navigation, settings, real-time event logging, and video preview.
  - Key files: `app.py`, `splash.py`.

- **Backend:**  
  - Handles telemetry data processing, event detection, race orchestration, and video editing/export.
  - Integrates configuration management and persistent storage via SQLite.
  - Key files/modules:  
    - `common.py`, `director.py`, `events.py`  
    - **New Modules:**  
      - `telemetry_filters.py` – for smoothing noisy telemetry data.  
      - `config_manager.py` – for dynamic settings and thresholds.  
      - `database_manager.py` – for persistent storage of telemetry, events, and settings.

- **AI Functionality:**  
  - Generates race commentary by combining real-time event data with refined prompt templates.
  - Converts commentary text into natural-sounding speech using a TTS integration with ElevenLabs.
  - Manages camera selection based on race data.
  - Key files/modules:  
    - `commentary.py`, `prompt_templates.py`, `tts_integration.py`, `camera.py`.

- **Video Editing & Export:**  
  - Combines the race video with the generated commentary audio, ensuring proper synchronization and quality.
  - Key files: `editor.py`, `export.py`.

## Features

- **Real-Time Event Detection:**  
  - Continuously processes race telemetry to detect key events (overtakes, stops, etc.) with adaptive thresholds and noise reduction.
  
- **Dynamic Commentary Generation:**  
  - Uses refined, structured prompts to generate energetic, context-aware commentary.
  
- **High-Quality Voice Synthesis:**  
  - Converts text commentary into natural, expressive speech using ElevenLabs' TTS engine.
  
- **Camera Management:**  
  - Dynamically selects optimal camera angles based on race events and driver performance.
  
- **Video Export:**  
  - Merges race footage with commentary audio into a final, exportable video file.
  
- **Persistent Data Storage:**  
  - Stores telemetry logs, events, and user configurations in a lightweight SQLite database.
  
- **Modular and Open Source:**  
  - Designed for community contributions, with clear separation of concerns and thorough documentation.

## Installation

1. **Requirements:**
   - Python 3.12+
   - A stable internet connection for API calls
   - Valid API keys for OpenAI and ElevenLabs
   - iRacing configured for video capture

2. **Clone the Repository:**

   ```bash
   git clone https://github.com/joshjaysalazar/IntelliCaster.git
   cd IntelliCaster
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run IntelliCaster:**

   Navigate to the `src` directory and run:

   ```bash
   python main.py
   ```

## Usage

1. **API Configuration:**
   - Open the **Settings** tab in the IntelliCaster UI.
   - Enter your OpenAI and ElevenLabs API keys.
   - Adjust other settings (e.g., telemetry thresholds) as needed.
   - Save the settings (a restart might be required).

2. **Generating Commentary:**
   - Open an iRacing replay.
   - Click the **Start Commentary** button to begin processing the race data.
   - The system will use telemetry data to detect events and generate commentary accordingly.
   - When finished, click **Stop Commentary** to render the final video with the integrated voice commentary.

## Project Structure

- **Front End:**
  - `app.py` – Main application interface and navigation.
  - `splash.py` – Splash screen displayed at startup.

- **Backend:**
  - `common.py` – Global variables and shared configurations.
  - `director.py` – Orchestrates the race, linking telemetry, event detection, camera switching, and commentary generation.
  - `events.py` – Processes telemetry data to detect race events.
  - **New Modules:**
    - `telemetry_filters.py` – Implements smoothing algorithms for telemetry data.
    - `config_manager.py` – Manages dynamic configuration and settings.
    - `database_manager.py` – Handles SQLite database interactions for persistent storage.

- **AI Functionality:**
  - `commentary.py` – Generates commentary text using OpenAI.
  - `prompt_templates.py` – Centralizes structured prompt templates for commentary generation.
  - `tts_integration.py` – Integrates with ElevenLabs to convert text to speech.
  - `camera.py` – Manages camera view selection based on race events.

- **Video Processing:**
  - `editor.py` – Combines video footage and commentary audio.
  - `export.py` – Provides UI for tracking video export progress.

- **Documentation & Tests:**
  - `README.md` – Project documentation.
  - `requirements.txt` – Required libraries.
  - Additional documentation and tests will be organized in dedicated folders (`docs/`, `tests/`).

## Contributing

We welcome contributions! Whether it's bug fixes, new features, or improvements to our documentation, your help is invaluable. Please follow these steps:

1. Fork the repository.
2. Create a dedicated branch for your changes.
3. Submit a pull request with a clear description of your changes.
4. Open an issue for bugs or feature requests.

## API Usage & Costs

IntelliCaster integrates OpenAI for text generation and ElevenLabs for voice synthesis. Both services use a usage-based pricing model. Please review their respective websites for details on costs and usage limits.

## License

IntelliCaster is released under the GPL-3.0 license. See the [LICENSE](LICENSE) file for more details.

## Issues

If you encounter any bugs or have feature requests, please open an issue in the GitHub repository. Your feedback helps us improve IntelliCaster for everyone.

---

This updated README.md reflects our current progress and architecture, covering front-end, backend (with database integration and configuration management), AI commentary generation, and video processing. Let me know if you'd like any further adjustments or additional details!
