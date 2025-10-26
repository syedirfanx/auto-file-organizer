import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os

FOLDER_TO_WATCH = r"C:\Users\HP\AutoFileProject\WATCH_FOLDER"

class WatcherHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            print(f"NEW FILE detected: {event.src_path}")

    def on_modified(self, event):
        if not event.is_directory:
            print(f"FILE modified: {event.src_path}")

if __name__ == "__main__":
    event_handler = WatcherHandler()
    observer = Observer()
    observer.schedule(event_handler, FOLDER_TO_WATCH, recursive=True)
    observer.start()
    print(f"MONITORING folder: {FOLDER_TO_WATCH}...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("STOPPED monitoring.")

    observer.join()
