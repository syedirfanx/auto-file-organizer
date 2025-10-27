# Auto File Organizer

## Overview
AutoFileOrganizer is a Python-based automated file management system that continuously monitors a folder, organizes files by type and date, logs activities.

## Features
- Real-time folder monitoring
- Moves files into structured directories:
```
MyFiles/
└── YYYY-MM-DD/
  ├── JPG/
  ├── PNG/
  ├── MP4/
  └── PDF/
```
- Automatic CSV logging Records:
  - Timestamp  
  - File Name  
  - Old Path  
  - New Path
- Visualization script to analyze file activity trends.

## Folder Structure
```
AutoFileProject/
  ├── logs/
  │ └── file_log.csv 
  └── MyFiles/ # Folder being monitored
    └── YYYY-MM-DD/
      ├── JPG/
      ├── PNG/
      ├── MP4/
      └── PDF/
```


## Installation

1. **Clone or copy** this project to your local machine.
2. Create a **virtual environment**:
```bash
python -m venv env
env\Scripts\activate
```
3. Install dependencies
```
pip install watchdog pandas matplotlib
```

## Usage

1. Set your folder paths inside main.py:
  ```
  FOLDER_TO_WATCH = r"C:\Users\HP\AutoFileProject\MyFiles"
  CSV_LOG = r"C:\Users\HP\AutoFileProject\logs\file_log.csv"
  ```

2. Run the script:
```
python folder_organizer.py
```

3. Drop any file into your MyFiles folder, and the system will:
  - Move it into YYYY-MM-DD/FORMAT/
  - Log the movement in file_log.csv
  - Show a success message in the console

## Project Demonstration

Watch the project walkthrough video here:
[Watch on Google Drive](https://drive.google.com/file/d/1DDbbZl5P5bmjB77gfMKXRhIVN0r6WRjN/view?usp=sharing)

_Note: The audio in the video is slightly low due to microphone limitations. Please use headphones for better clarity._
