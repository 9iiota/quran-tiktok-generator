# Quranic TikToks Generator

This repository hosts the Quranic TikToks Generator, a Python tool designed to facilitate the creation of TikTok videos featuring Quranic recitations and Arabic text on screen. While the project may require some exploration and adaptation, I've made it open-source to showcase my projects and provide a starting point for others interested in similar endeavors.

You can see an example of what this repository does on the following TikTok account: [@quran_2_listen](https://www.tiktok.com/@quran_2_listen).

## Getting Started

### Prerequisites
- Python 3.x
- Required Python packages listed in `requirements.txt`
- ImageMagick
- ffmpeg

### Installation
1. Clone the repository to your local machine.
2. Install the required Python packages by running:
```
pip install -r requirements.txt
```
3. Install ImageMagick:
   - Visit the [ImageMagick website](https://imagemagick.org/) to download and install the appropriate version for your operating system.
   - Follow the installation instructions provided on the website.
4. Install ffmpeg:
   - Visit the [ffmpeg website](https://ffmpeg.org/) to download and install ffmpeg for your operating system.
   - Follow the installation instructions provided on the website.

### Note
Please note that while efforts have been made to provide comprehensive instructions, there could be some missing parts in this README. Feel free to reach out or explore the code for further clarification.

### Usage
**Configuration**
- Before using the code, you need to make some modifications to enums.py:
  - Change the variable names of the Accounts enum according to your requirements.
  - Update the background clips directories as needed.

**Adding Background Clips**
- You'll need to add background clips of your choice. Place them in the appropriate directories.

**Adding New Presets**
- All presets are stored in presets.py. Follow these steps to add a new one:
  1. In the "Surahs" folder, add a new folder with the name of the reciter.
  2. Inside the new folder, create another folder with the format: "SURAHNAME (CHAPTERNUMBER.STARTVERSENUMBER_ENDVERSENUMBER)". Here, the start verse number and end verse number refer to the specific verses of the clip you want to make. For example, if the entire audio covers verses 1-10 but you want to make a clip from only verses 1-3, then the start verse number would be 1 and the end verse number would be 3.
  3. Place the audio file in that folder.
  4. Add a new preset in presets.py following the existing format.
  5. Run main.py, which will generate a chapter.csv file containing the text of the verses. If you ever need to regenerate this file, just rename the existing chapter.csv file and run main.py again.
  6. Open the audio file using Adobe Audition and add markers:
     - Use a normal marker at the start of each new verse.
     - Use a CD track marker for any markers in between the starts.
     - Use a subclip marker if you want the video clip to continue but want the text to fade away at the time of the subclip marker.
  7. Export all markers to the same folder.
  8. Edit the chapter.csv file to ensure the text for each marker is correct.
  9. Finally, run the code, and it should create the TikTok video correctly.
 
### Contributing
Contributions are welcome! Feel free to submit pull requests or open issues.

### License
This project is licensed under the [MIT License](https://opensource.org/license/MIT).
