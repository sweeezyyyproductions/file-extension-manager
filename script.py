import os
import shutil
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tqdm import tqdm

def should_copy_file(file_path, selected_extensions):
    # Check if the file extension is in the selected extensions list
    file_extension = os.path.splitext(file_path)[-1].lower()
    return any(file_extension == ext.lower() for ext in selected_extensions)

def process_files(action):
    source_directory = source_dir_entry.get()
    destination_directory = dest_dir_entry.get()
    
    if not source_directory or not destination_directory:
        result_label.config(text="Please select source and destination directories.")
        return
    
    selected_extensions = [".aegraphic", ".aep", ".mp3", ".png", ".PNG", ".jpg", ".JPEG", ".HEIC", ".wav", ".WAV", ".m4a"]
    
    if action == "Copy":
        perform_action(copy_files_with_selected_extensions, source_directory, destination_directory, selected_extensions, "Copying Files")
    elif action == "Move":
        perform_action(move_files_with_selected_extensions, source_directory, destination_directory, selected_extensions, "Moving Files")
    elif action == "Delete":
        perform_action(delete_files_with_selected_extensions, source_directory, destination_directory, selected_extensions, "Deleting Files")

def perform_action(action_function, source_directory, destination_directory, selected_extensions, action_description):
    try:
        with tqdm(desc=action_description, ascii=True, ncols=100) as pbar:
            action_function(source_directory, destination_directory, selected_extensions, pbar)
    
        result_label.config(text=f"Files {action_description[:-1].lower()}ed successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def copy_files_with_selected_extensions(source_directory, destination_directory, selected_extensions, pbar):
    for root, _, files in os.walk(source_directory):
        for file in files:
            if should_copy_file(file, selected_extensions):
                source_file = os.path.join(root, file)
                destination_file = os.path.join(destination_directory, file)
                
                # Check if the file already exists in the destination
                if not os.path.exists(destination_file):
                    # Copy the file to the destination directory
                    shutil.copy(source_file, destination_file)
                pbar.update(1)  # Update the progress bar

def move_files_with_selected_extensions(source_directory, destination_directory, selected_extensions, pbar):
    for root, _, files in os.walk(source_directory):
        for file in files:
            if should_copy_file(file, selected_extensions):
                source_file = os.path.join(root, file)
                destination_file = os.path.join(destination_directory, file)
                
                # Check if the file already exists in the destination
                if not os.path.exists(destination_file):
                    # Move the file to the destination directory
                    shutil.move(source_file, destination_file)
                pbar.update(1)  # Update the progress bar

def delete_files_with_selected_extensions(source_directory, destination_directory, selected_extensions, pbar):
    for root, _, files in os.walk(source_directory):
        for file in files:
            if should_copy_file(file, selected_extensions):
                source_file = os.path.join(root, file)
                
                # Check if the file exists in the destination
                if os.path.exists(source_file):
                    # Delete the file
                    os.remove(source_file)
                pbar.update(1)  # Update the progress bar

# Create the main window
root = tk.Tk()
root.title("File Processor")

# Source directory entry
source_label = tk.Label(root, text="Source Directory:")
source_label.pack()
source_dir_entry = tk.Entry(root, width=50)
source_dir_entry.pack()

def select_source_directory():
    source_directory = filedialog.askdirectory()
    source_dir_entry.delete(0, tk.END)
    source_dir_entry.insert(0, source_directory)

source_button = tk.Button(root, text="Select Source Directory", command=select_source_directory)
source_button.pack()

# Destination directory entry
dest_label = tk.Label(root, text="Destination Directory:")
dest_label.pack()
dest_dir_entry = tk.Entry(root, width=50)
dest_dir_entry.pack()

def select_destination_directory():
    destination_directory = filedialog.askdirectory()
    dest_dir_entry.delete(0, tk.END)
    dest_dir_entry.insert(0, destination_directory)

dest_button = tk.Button(root, text="Select Destination Directory", command=select_destination_directory)
dest_button.pack()

# Action buttons
copy_button = tk.Button(root, text="Copy Files", command=lambda: process_files("Copy"))
copy_button.pack()

move_button = tk.Button(root, text="Move Files", command=lambda: process_files("Move"))
move_button.pack()

delete_button = tk.Button(root, text="Delete Files", command=lambda: process_files("Delete"))
delete_button.pack()

# Progress bar
# The progress bar is defined within the perform_action function

# Result label
result_label = tk.Label(root, text="")
result_label.pack()

# Start the GUI main loop
root.mainloop()
