# Qur'an TikTok Generator
TikTok account showcasing videos created using this generator: [@quran_2_listen](https://www.tiktok.com/@quran_2_listen)

---

## Description

Qur'an TikTok Generator is a Python automation tool that creates TikTok-ready videos featuring Quranic recitations with synchronized Arabic text, translations, and verse numbers overlaid on customizable background footage. The tool handles timing synchronization, text rendering, video composition, and multi-language support to produce professional-quality Islamic content for social media.

While technically open-source, this repository primarily serves to **showcase the capabilities of the tool** and the videos it can produce. The codebase is functional but may require technical expertise to set up and customize for your own use.

---

## Features

* **Automated Video Generation** - Converts Quranic audio recitations into complete TikTok videos with synchronized text overlays
* **Multi-Language Support** - Display Arabic text alongside translations in various languages
* **Verse-Level Synchronization** - Uses timestamp markers to sync text with audio at the verse level
* **Customizable Visual Settings** - Configure dimensions, clip speeds, text positioning, fonts, and fade durations
* **Background Video Integration** - Overlay recitations on background clips with options for mirroring and speed adjustment
* **Preset System** - Save and reuse configurations for different reciters, chapters, and styles
* **Flexible Verse Selection** - Create videos for single verses, verse ranges, or entire chapters
* **Text Fade Effects** - Smooth fade-in/fade-out transitions for verse text and translations
* **Account Management** - Support for multiple account configurations with different settings

---

## Installation

### Prerequisites

* **Python 3.7 or higher**
* **ImageMagick** - Required for text rendering and image manipulation
* **ffmpeg** - Required for video processing and composition

### Setup Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/9iiota/quranic-tiktoks-generator.git
   cd quranic-tiktoks-generator
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install ImageMagick:
   - Download from [imagemagick.org](https://imagemagick.org/)
   - Follow the installation instructions for your operating system
   - Ensure ImageMagick is added to your system PATH

4. Install ffmpeg:
   - Download from [ffmpeg.org](https://ffmpeg.org/)
   - Follow the installation instructions for your operating system
   - Ensure ffmpeg is added to your system PATH

---

## Usage

### Quick Start

The tool uses a preset-based workflow. Here's the basic process:

```python
from tiktok import TikTok
from presets import Presets
from models import Account

# Initialize with an account configuration
tiktok = TikTok(account=Account.YOUR_ACCOUNT)

# Create a video using a preset
tiktok.create(preset=Presets.YOUR_PRESET)
```

### Setting Up a New Preset

1. **Configure Account Settings** in `enums.py`:
   - Define account names in the `Accounts` enum
   - Set background video directories
   - Configure language preferences

2. **Prepare Audio Files**:
   - Create a folder structure: `Surahs/ReciterName/ChapterName (CHAPTER.START_END)/`
   - Example: `Surahs/Mishary Rashid/Al-Fatiha (1.1_7)/`
   - Place your audio file (`.wav` or `.mp3`) in this folder

3. **Generate Chapter Text** (first-time setup):
   - Run `main.py` to generate `chapter.csv` containing verse text
   - The CSV file will be created automatically based on the chapter number

4. **Create Timestamp Markers** using Adobe Audition (or similar):
   - **Normal Marker** - Place at the start of each new verse
   - **CD Track Marker** - Place between verse starts for sub-timing
   - **Subclip Marker** - Use when you want text to fade while video continues
   - Export markers as `Markers.csv` to the same folder

5. **Verify CSV Data**:
   - Open `chapter.csv` and ensure verse text is correct
   - Verify `Markers.csv` contains accurate timestamps

6. **Create Preset** in `presets.py`:
   ```python
   YOUR_PRESET = Preset(
       audio_directory_path="Surahs/ReciterName/ChapterName (1.1_7)/",
       video_verse_range=(1, 7),
       time_modifiers=TimeModifiers(...),
       additional_video_settings=AdditionalVideoSettings(...)
   )
   ```

7. **Run the Generator**:
   ```bash
   python main.py
   ```

---

## Project Structure

```
├── Fonts/                    # Font files for text rendering
├── Pages/                    # Generated output videos
├── Surahs/                   # Audio files and CSVs organized by reciter/chapter
├── enums.py                  # Account configurations and enums
├── file_manager.py           # File handling utilities
├── functions.py              # Core video generation functions
├── main.py                   # Main execution script
├── models.py                 # Data models (Account, VideoSettings, etc.)
├── presets.py                # Preset configurations for different videos
├── tiktok.py                 # TikTok class and video creation logic
├── queue.txt                 # Video generation queue
└── requirements.txt          # Python dependencies
```

---

## Configuration

### Video Settings

Customize video output in `VideoSettings`:

```python
VideoSettings(
    allowDuplicateClips=False,
    allowMirroredClips=True,
    clipSpeed=1.0,
    minimumClipDuration=1.25,
    videoDimensions=(576, 1024),  # TikTok portrait format
    videoMode=VideoModes.VIDEO
)
```

### Text Clip Configuration

Adjust text appearance with `TextClipInfo`:

```python
TextClipInfo(
    text_background_color="transparent",
    text_fade_duration=0.5,
    text_font_size=44,
    text_method="caption",
    text_position=("center", 0.41),
    text_size=(520, None)
)
```

### Time Modifiers

Fine-tune timing synchronization:

```python
TimeModifiers(
    start_offset=0.0,
    end_offset=0.0,
    verse_delay=0.0
)
```

---

## CSV File Format

### chapter.csv
Contains verse text data:
```csv
verse,ar,translation
1,بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ,In the name of Allah, the Entirely Merciful...
2,ٱلْحَمْدُ لِلَّهِ رَبِّ ٱلْعَٰلَمِينَ,All praise is due to Allah, Lord of the worlds
```

### Markers.csv
Contains timestamp data exported from audio editing software:
```csv
Name,Start,Duration,Time Format,Type
1,00:00:00.000,00:00:03.500,decimal,Cue
2,00:00:03.500,00:00:04.200,decimal,Cue
```

---

## Requirements

See `requirements.txt` for a complete list of Python dependencies. Key libraries include:

* `moviepy` - Video editing and composition
* Additional libraries for text rendering and audio processing

---

## Examples

See the example output on TikTok: [@quran_2_listen](https://www.tiktok.com/@quran_2_listen)

---

## Notes

* **This tool is primarily for showcase purposes** - While functional, it may require technical expertise to adapt for your specific use case
* **Adobe Audition recommended** - For precise timestamp marker creation, though other audio editors with marker support can work
* **Background clips not included** - You must provide your own background video footage
* **Arabic font required** - Ensure you have appropriate Arabic fonts installed in the `Fonts/` directory
* The tool generates videos with metadata suitable for TikTok's platform requirements

---

## Troubleshooting

* **ImageMagick errors**: Ensure ImageMagick is properly installed and the path is configured in your environment
* **Missing CSV files**: Run `main.py` first to generate `chapter.csv` before creating videos
* **Timestamp sync issues**: Verify your `Markers.csv` file has accurate timestamps and marker types
* **Text rendering problems**: Check that the required fonts are present in the `Fonts/` directory

---

## Contributing

Contributions are welcome! While the codebase may not be straightforward to work with, feel free to fork the repository and submit pull requests for improvements, bug fixes, or additional features.

---

## License

This project is open-source and licensed under the **MIT License**. See [LICENSE](LICENSE) for details.

---

## Links

* [GitHub Repository](https://github.com/9iiota/quranic-tiktoks-generator)
* [Example TikTok Account](https://www.tiktok.com/@quran_2_listen)
