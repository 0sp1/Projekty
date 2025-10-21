import os
import shutil

def preview_organization(folder_path):
    file_structure = {}
    
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        if os.path.isfile(file_path):
            ext = filename.split(".")[-1].lower() if "." in filename else "others"
            file_structure.setdefault(ext, []).append(filename)
    
    if not file_structure:
        print("No files to organize.")
        return
    
    print("\n--- Preview of Organization ---")
    for ext, files in file_structure.items():
        print(f"\nFolder: {ext}")
        for f in files:
            print(f"  - {f}")
    print("-------------------------------")

def organize_files(folder_path):
    if not os.path.exists(folder_path):
        print("Folder does not exist.")
        return

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        if os.path.isfile(file_path):
            ext = filename.split(".")[-1].lower() if "." in filename else "others"
            ext_folder = os.path.join(folder_path, ext)

            if not os.path.exists(ext_folder):
                os.makedirs(ext_folder)

            shutil.move(file_path, os.path.join(ext_folder, filename))

    print("Files organized successfully.")

def main():
    print("File Organizer")
    while True:
        folder = input("\nEnter folder path to organize: ").strip()
        if not folder:
            print("Please enter a valid path.")
            continue

        if not os.path.exists(folder):
            print("Folder does not exist.")
            continue

        preview_organization(folder)
        confirm = input("\nProceed with organizing? (y/n): ").lower()
        if confirm == 'y':
            organize_files(folder)
        else:
            print("Organization cancelled.")

        again = input("\nDo you want to organize another folder? (y/n): ").lower()
        if again != "y":
            print("Exiting File Organizer.")
            break

if __name__ == "__main__":
    main()
