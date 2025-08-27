import os
import shutil

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

        organize_files(folder)

        again = input("Do you want to organize another folder? (y/n): ").lower()
        if again != "y":
            print("Exiting File Organizer.")
            break

if __name__ == "__main__":
    main()
