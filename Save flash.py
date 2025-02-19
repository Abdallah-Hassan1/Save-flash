import os
import shutil
import time
import win32file
from tqdm import tqdm

def get_removable_drives():
    """Returns a list of removable drives."""
    drives = []
    drive_bits = win32file.GetLogicalDrives()
    for letter in range(26):  # A-Z
        if drive_bits & (1 << letter):
            drive = f"{chr(65 + letter)}:\\"
            if win32file.GetDriveType(drive) == win32file.DRIVE_REMOVABLE:
                drives.append(drive)
    return drives

def copy_files_with_progress(source, target):
    """Copies files from the source to the target directory with a progress bar."""
    try:
        # Get the list of all files to be copied
        all_files = []
        for root, dirs, files in os.walk(source):
            for file in files:
                all_files.append(os.path.join(root, file))

        # Progress bar
        with tqdm(total=len(all_files), desc="Copying Files", unit="file") as progress_bar:
            for src_file in all_files:
                relative_path = os.path.relpath(src_file, source)
                dest_file = os.path.join(target, relative_path)
                os.makedirs(os.path.dirname(dest_file), exist_ok=True)
                shutil.copy2(src_file, dest_file)
                progress_bar.update(1)  # Update progress bar
        print(f"Files copied successfully from {source} to {target}!")
    except Exception as e:
        print(f"Error during copying: {e}")

def monitor_usb(target_directory):
    """Monitors for USB drive insertion and backs up files."""
    print("Monitoring USB drives...")
    previous_drives = set(get_removable_drives())

    while True:
        time.sleep(2)  # Check every 2 seconds
        current_drives = set(get_removable_drives())
        new_drives = current_drives - previous_drives

        if new_drives:
            for drive in new_drives:
                print(f"New USB drive detected: {drive}")
                backup_path = os.path.join(target_directory, os.path.basename(drive.strip('\\')))
                os.makedirs(backup_path, exist_ok=True)
                copy_files_with_progress(drive, backup_path)
            print("-------------------------------------------------------------------------------")
            print("Monitoring USB drives...")

        previous_drives = current_drives

if __name__ == "__main__":
    target_directory = "A:\\Backup"
    os.makedirs(target_directory, exist_ok=True)
    monitor_usb(target_directory)
