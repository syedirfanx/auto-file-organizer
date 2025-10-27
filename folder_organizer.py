import os
import time
import shutil
import csv
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime

FOLDER_TO_WATCH = r"C:\Users\HP\AutoFileProject\MyFiles"
LOG_FOLDER = r"C:\Users\HP\AutoFileProject\logs"
os.makedirs(LOG_FOLDER, exist_ok=True)

FILE_TYPES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".svg"],
    "Videos": [".mp4", ".mkv", ".flv", ".avi", ".mov"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".pptx", ".xls", ".xlsx"],
    "Music": [".mp3", ".wav", ".aac"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
}

CSV_LOG = os.path.join(LOG_FOLDER, "file_log.csv")

os.makedirs(FOLDER_TO_WATCH, exist_ok=True)

def is_file_ready(file_path, wait_time=2, retries=15):
    for _ in range(retries):
        try:
            with open(file_path, 'rb'):
                return True
        except (PermissionError, OSError):
            time.sleep(wait_time)
    return False

def classify_file(file_path):
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()
    for folder_name, extensions in FILE_TYPES.items():
        if ext in extensions:
            return folder_name
    return "Others"

def log_to_csv(file_name, old_path, new_path):
    try:
        with open(CSV_LOG, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            if os.path.getsize(CSV_LOG) == 0:
                writer.writerow(["Timestamp", "File Name", "Old Path", "New Path"])
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            writer.writerow([timestamp, file_name, old_path, new_path])
    except Exception as e:
        print(f"ERROR logging CSV: {e}")

def move_file(file_path):
    if not os.path.exists(file_path):
        print(f"FILE does not exist: {file_path}")
        return

    if not is_file_ready(file_path):
        print(f"FILE not ready yet: {file_path}")
        return

    try:
        _, ext = os.path.splitext(file_path)
        ext_folder = ext[1:].upper() if ext else "Misc"
        date_folder = datetime.now().strftime("%Y-%m-%d")

        destination_folder = os.path.join(FOLDER_TO_WATCH, date_folder, ext_folder)
        os.makedirs(destination_folder, exist_ok=True)

        new_path = os.path.join(destination_folder, os.path.basename(file_path))
        if os.path.exists(new_path):
            base, ext2 = os.path.splitext(new_path)
            new_path = base + "_moved_copy" + ext2

        shutil.move(file_path, new_path)
        print(f"MOVED: {file_path} → {destination_folder}")
        log_to_csv(os.path.basename(file_path), file_path, new_path)

    except Exception as e:
        print(f"ERROR moving file {file_path}: {e}")
        if not os.path.exists(file_path) and os.path.exists(new_path):
            try:
                shutil.move(new_path, file_path)
                print(f"ROLLBACK successful: {new_path} → {file_path}")
            except Exception as rollback_error:
                print(f"ROLLBACK failed: {rollback_error}")

class WatcherHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            if os.path.dirname(event.src_path) == FOLDER_TO_WATCH:
                print(f"NEW FILE detected: {event.src_path}")
                move_file(event.src_path)
            else:
                print(f"Skipping file in subfolder: {event.src_path}")

if __name__ == "__main__":
    event_handler = WatcherHandler()
    observer = Observer()
    observer.schedule(event_handler, FOLDER_TO_WATCH, recursive=False)
    observer.start()
    print(f"MONITORING and ORGANIZING folder: {FOLDER_TO_WATCH}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("STOPPED monitoring.")
    observer.join()
