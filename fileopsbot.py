import os
import time
import shutil
import logging
from datetime import datetime
#from backend import root_directory

class FileOrganizer:
    def __init__(self, root_directory):
        self.root_directory = root_directory
        self.backup_folder = 'Backup_folder'
        self.extension_folder = "Extension Files"
        self.log_file = "ExtensionData.log"
        
        os.makedirs(os.path.join(self.extension_folder,root_directory), exist_ok=True)
        os.makedirs(os.path.join(self.backup_folder,root_directory), exist_ok=True)
        
        self.logging_setup()
        self.extension_map = self.get_extension_map()

    def logging_setup(self):
        logging.basicConfig(filename=self.log_file, level=logging.DEBUG,
                            format='%(asctime)s--%(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    def get_extension_map(self):
        return {
            "Text Files": {
                ".txt": "Plain Text",
                ".rtf": "Rich Text Format",
                ".log": "Log Files",
            },
            "Image Files": {
                ".jpg": "JPEG Images",
                ".jpeg": "JPEG Images",
                ".png": "Portable Network Graphics",
                ".gif": "Graphics Interchange Format",
                ".bmp": "Bitmap Images",
                ".svg": "Scalable Vector Graphics",
            },
            "Document Files": {
                ".pdf": "Portable Document Format",
                ".doc": "Microsoft Word Documents",
                ".docx": "Microsoft Word Documents",
                ".odt": "OpenDocument Text",
                ".ppt": "Microsoft PowerPoint Files",
                ".pptx": "Microsoft PowerPoint Files",
            },
            "Audio Files": {
                ".mp3": "MP3 Audio",
                ".wav": "Waveform Audio File Format",
                ".aac": "Advanced Audio Coding",
                ".flac": "Free Lossless Audio Codec",
            },
            "Video Files": {
                ".mp4": "MPEG-4 Video",
                ".mkv": "Matroska Video",
                ".avi": "Audio Video Interleave",
                ".mov": "Apple QuickTime Movie",
            },
            "Compressed Files": {
                ".zip": "ZIP Archive",
                ".rar": "RAR Archive",
                ".tar": "Tape Archive",
                ".gz": "Gzip Compressed Archive",
            },
            "Application & Code Files": {
                ".exe": "Windows Executable File",
                ".dll": "Dynamic Link Library",
                ".java": "Java Source Code",
                ".py": "Python Script",
                ".html": "HyperText Markup Language",
                ".css": "Cascading Style Sheets",
                ".js": "JavaScript",
            }
        }

    def organize_files(self):
        files_and_dirs = os.listdir(self.root_directory)

        for folder, extensions in self.extension_map.items():
            if isinstance(extensions, dict):
                os.makedirs(os.path.join(self.root_directory, folder), exist_ok=True)
                for ext in extensions.keys():
                    os.makedirs(os.path.join(folder, ext), exist_ok=True)

        # Moving and Backuping the file
        for filename in os.listdir(self.root_directory):
            file_path = os.path.join(self.root_directory, filename)    
            
            if not os.path.isfile(file_path):
                continue
            
            ext = os.path.splitext(filename)[1]
            target_folder = 'Others'
            
            for folder, extensions in self.extension_map.items():
                if isinstance(extensions, dict) and ext in extensions:
                    target_folder = folder
                    break

            dest_path = os.path.join(self.root_directory, target_folder, filename)
            self.move_file(file_path, dest_path)
            self.create_backup(dest_path)

    def move_file(self, file_path, dest_path):
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        shutil.move(file_path, dest_path)
        logging.debug(f"Moved {os.path.basename(file_path)} to {dest_path}")
    
    def create_backup(self, dest_path):
        backup_path = os.path.join(self.backup_folder, os.path.relpath(dest_path, self.root_directory)) #relative path of the file ->dest_path w.r.t to the self.root_directory (Intersection of the both path as address)
        os.makedirs(os.path.dirname(backup_path), exist_ok=True)
        shutil.copy(dest_path, backup_path)

    def cleanup_old_backups(self):
        today = datetime.now()
        now = time.time()

        for root, dirs, files in os.walk(self.backup_folder):
            for filename in files:
                file_path = os.path.join(root, filename)
                file_creation_time = os.path.getctime(file_path)
                if (now - file_creation_time) > (7 * 86400):  # Older than 7 days
                    os.remove(file_path)
                    print(f"Deleted old backup file: {filename}")
                    logging.debug(f"{filename} has been deleted from backup")



if __name__ == "__main__":
    root_directory=r"C:\.......\.......\......."
    file_organizer = FileOrganizer(root_directory)
    
    file_organizer.organize_files() 
    file_organizer.cleanup_old_backups()  
