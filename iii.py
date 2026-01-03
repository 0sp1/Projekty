import os
import shutil
import json

LOG_FILE = ".organization_log.json"

def preview_organization(folder_path, custom_mapping):
    file_structure = {}

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            ext = filename.split(".")[-1].lower() if "." in filename else "others"
            folder_name = get_folder_name_for_extension(ext, custom_mapping)
            file_structure.setdefault(folder_name, []).append(filename)
    
    if not file_structure:
        print("No files to organize.")
        return
    
    print("\n--- Preview of Organization ---")
    for folder, files in file_structure.items():
        print(f"\nFolder: {folder}")
        for f in files:
            print(f"  - {f}")
    print("-------------------------------")

def get_folder_name_for_extension(ext, custom_mapping):
    for folder, extensions in custom_mapping.items():
        if ext in extensions:
            return folder
    return ext  # Default: folder named after the extension

def organize_files(folder_path, custom_mapping):
    if not os.path.exists(folder_path):
        print("Folder does not exist.")
        return

    moved_files = []

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        if os.path.isfile(file_path):
            ext = filename.split(".")[-1].lower() if "." in filename else "others"
            folder_name = get_folder_name_for_extension(ext, custom_mapping)
            dest_folder = os.path.join(folder_path, folder_name)

            if not os.path.exists(dest_folder):
                os.makedirs(dest_folder)

            dest_path = os.path.join(dest_folder, filename)
            shutil.move(file_path, dest_path)
            moved_files.append({"src": file_path, "dest": dest_path})

    if moved_files:
        with open(LOG_FILE, "w") as f:
            json.dump(moved_files, f, indent=2)
        print("Files organized successfully.")
    else:
        print("No files moved.")

def undo_last_organization():
    if not os.path.exists(LOG_FILE):
        print("No previous organization found to undo.")
        return

    with open(LOG_FILE, "r") as f:
        moved_files = json.load(f)

    for entry in moved_files:
        src = entry["src"]
        dest = entry["dest"]
        if os.path.exists(dest):
            os.makedirs(os.path.dirname(src), exist_ok=True)
            shutil.move(dest, src)

    os.remove(LOG_FILE)
    print("Undo completed. Files restored to original locations.")

def get_custom_mapping():
    print("\nWould you like to define custom folder mappings? (e.g., images: jpg, png)")
    choice = input("Enter 'y' for yes or press Enter to skip: ").lower()
    mapping = {}

    if choice == "y":
        print("Enter mappings one per line (folder_name: ext1, ext2, ...)")
        print("Type 'done' when finished.\n")
        while True:
            line = input("> ").strip()
            if line.lower() == "done":
                break
            if ":" in line:
                folder, exts = line.split(":", 1)
                folder = folder.strip().lower()
                extensions = [e.strip().lower() for e in exts.split(",")]
                mapping[folder] = extensions
    return mapping

def main():
    print("📁 File Organizer with Undo & Custom Folders")
    
    while True:
        print("\nOptions:")
        print("1. Organize a folder")
        print("2. Undo last organization")
        print("3. Exit")
        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            folder = input("\nEnter folder path to organize: ").strip()
            if not os.path.exists(folder):
                print("Folder does not exist.")
                continue

            custom_mapping = get_custom_mapping()
            preview_organization(folder, custom_mapping)
            confirm = input("\nProceed with organizing? (y/n): ").lower()
            if confirm == "y":
                organize_files(folder, custom_mapping)
            else:
                print("Organization cancelled.")

        elif choice == "2":
            undo_last_organization()

        elif choice == "3":
            print("Exiting File Organizer.")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
