import os
import shutil

# Set this to the folder you want to organize
FOLDER_PATH = "downloads"

# File type mappings
FILE_TYPES = {
    "Images": [".png", ".jpg", ".jpeg", ".gif", ".bmp"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".pptx"],
    "Videos": [".mp4", ".mov", ".avi", ".mkv"],
    "Audio": [".mp3", ".wav", ".flac"],
    "Archives": [".zip", ".rar", ".tar", ".gz"],
    "Scripts": [".py", ".js", ".sh", ".bat"],
    "Others": []
}

def get_category(extension):
    for category, extensions in FILE_TYPES.items():
        if extension.lower() in extensions:
            return category
    return "Others"

def organize_folder(path):
    if not os.path.exists(path):
        print("❌ Folder not found.")
        return

    files = os.listdir(path)
    for file in files:
        file_path = os.path.join(path, file)
        if os.path.isfile(file_path):
            _, ext = os.path.splitext(file)
            category = get_category(ext)
            target_dir = os.path.join(path, category)
            os.makedirs(target_dir, exist_ok=True)
            shutil.move(file_path, os.path.join(target_dir, file))
            print(f"📂 Moved '{file}' to '{category}/'")

def main():
    print(f"📁 Organizing folder: {FOLDER_PATH}")
    organize_folder(FOLDER_PATH)
    print("✅ Done.")

if __name__ == "__main__":
    main()
