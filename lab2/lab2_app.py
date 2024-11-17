import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from threading import Thread
import time

from common.utils import clear_window
from lab2.constants import MD5_HASHES
from lab2.file_handler import FileHandler
from lab2.hash_validator import HashValidator

class Lab2App:
    def __init__(self, root):
        self.root = root
        self.root.title("Lab 2 - Custom MD5 Hashing")
        self.root.geometry("1000x900")
        self.loading_label = None
        self.setup_menu()

    def setup_menu(self):
        clear_window(self.root)

        label = tk.Label(self.root, text="MD5 Hashing Lab", font=("Helvetica", 14))
        label.pack(pady=10)

        text_entry_label = tk.Label(self.root, text="Enter text to hash:")
        text_entry_label.pack()

        self.text_entry = tk.Entry(self.root)
        self.text_entry.pack(pady=5)

        generate_hash_btn = tk.Button(self.root, text="Generate MD5 Hash", command=self.generate_hash)
        generate_hash_btn.pack(pady=5)

        load_file_btn = tk.Button(self.root, text="Load File and Hash", command=self.start_load_file_hashing)
        load_file_btn.pack(pady=5)

        text_check_label = tk.Label(self.root, text="Enter the expected hash:")
        text_check_label.pack()

        self.text_check = tk.Entry(self.root)
        self.text_check.pack(pady=5)
        check_integrity_btn = tk.Button(self.root, text="Check File Integrity", command=self.check_file_integrity)
        check_integrity_btn.pack(pady=5)

        generate_file_label = tk.Label(self.root, text="Enter size of file to generate (in MB):")
        generate_file_label.pack(pady=5)

        self.file_size_entry = tk.Entry(self.root)
        self.file_size_entry.pack(pady=5)

        generate_large_file_btn = tk.Button(self.root, text="Generate Large File", command=self.start_file_generation)
        generate_large_file_btn.pack(pady=5)

        test_btn = tk.Button(self.root, text="Run Tests", command=self.run_tests)
        test_btn.pack(pady=10)

        # Scrollable text area for displaying results
        self.result_text = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=80, height=10)
        self.result_text.pack(pady=10)

        # Clear Results Button
        clear_btn = tk.Button(self.root, text="Clear Results", command=self.clear_results)
        clear_btn.pack(pady=5)


    def show_loading(self):
        """Shows a loading message on the screen."""
        if not self.loading_label:
            self.loading_label = tk.Label(self.root, text="Loading...", font=("Helvetica", 12), fg="red")
            self.loading_label.pack(pady=10)
        else:
            self.loading_label.config(text="Loading...")
        self.root.update()  # Force the GUI to update and show the loading message immediately

    def hide_loading(self):
        """Hides the loading message from the screen."""
        if self.loading_label:
            self.loading_label.config(text="")
        self.root.update()  # Force the GUI to update to remove the loading message

    def generate_hash(self):
        text = self.text_entry.get().strip()
        if not text:
            messagebox.showerror("Error", "Text cannot be empty!")
            return

        md5_hash = HashValidator.md5(text.encode())
        result = f"The MD5 hash of '{text}' is:\n{md5_hash}\n\n"
        self.result_text.insert(tk.END, result)
        self.prompt_save(result)

    def load_file(self):
        """Handles the file loading and hashing process."""
        file_path = filedialog.askopenfilename()
        if file_path:
            try:
                md5_hash = FileHandler.md5_file(file_path)
                result = f"MD5 hash of the file is:\n{md5_hash}\n\n"
                self.result_text.insert(tk.END, result)
                self.prompt_save(result)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load and hash the file: {str(e)}")
        self.hide_loading()  # Hide loading after the process is done

    def start_load_file_hashing(self):
        """Starts the file hashing process in a separate thread to keep the GUI responsive."""
        self.show_loading()  # Show the loading message before starting
        thread = Thread(target=self.load_file)  # Run the load_file method in a separate thread
        thread.start()

    def check_file_integrity(self):
        file_path = filedialog.askopenfilename(title="Select File to Check Integrity")
        if file_path:
            expected_hash = self.text_check.get().strip()
            if not expected_hash:
                messagebox.showerror("Error", "Please enter the expected MD5 hash in the text field!")
                return

            try:
                is_valid = FileHandler.md5_file(file_path).upper() == expected_hash.upper()
                result = f"File integrity is {'valid' if is_valid else 'invalid'}. MD5 hashes {'match' if is_valid else 'do not match'}.\n\n"
                self.result_text.insert(tk.END, result)
                self.prompt_save(result)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to check file integrity: {str(e)}")

    def generate_large_file_thread(self, size_in_mb, file_path):
        """Thread that generates the file."""
        if size_in_mb > 100:
            messagebox.showerror("Error", "File size is too large! Maximum allowed size is 100MB.")
            self.hide_loading()
            return

        try:
            FileHandler.generate_large_file(file_path, size_in_mb)
            self.hide_loading()
            messagebox.showinfo("Success", f"Large file of {size_in_mb}MB generated at: {file_path}")
        except Exception as e:
            self.hide_loading()
            messagebox.showerror("Error", f"Failed to generate large file: {str(e)}")

    def start_file_generation(self):
        """Starts the file generation process, showing a loading message."""
        size_str = self.file_size_entry.get().strip()
        if not size_str.isdigit() or int(size_str) <= 0:
            messagebox.showerror("Error", "Please enter a valid positive integer for file size (in MB).")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".bin", title="Save Large File As")
        if not file_path:
            messagebox.showwarning("Warning", "No file path selected. File generation canceled.")
            return

        size_in_mb = int(size_str)
        self.show_loading()  # Show loading message
        thread = Thread(target=self.generate_large_file_thread, args=(size_in_mb, file_path))
        thread.start()  # Run the file generation in a separate thread

    def run_tests(self):
        results = []
        for text, expected_hash in MD5_HASHES.items():
            generated_hash = HashValidator.md5(text.encode())
            result = f"Input: '{text}', Expected: {expected_hash}, Generated: {generated_hash}, Test: {'Passed' if generated_hash == expected_hash else 'Failed'}"
            results.append(result)
            self.result_text.insert(tk.END, result + "\n")

        final_results = "\n".join(results)
        self.prompt_save(final_results)

    def prompt_save(self, result):
        """Asks the user if they want to save the result to a file."""
        save_response = messagebox.askyesno("Save Results", "Do you want to save the result to a file?")
        if save_response:
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", title="Save Result As")
            if file_path:
                try:
                    with open(file_path, 'w') as f:
                        f.write(result)
                    messagebox.showinfo("Success", f"Result saved to: {file_path}")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to save result: {str(e)}")

    def clear_results(self):
        """Clears the result text area."""
        self.result_text.delete('1.0', tk.END)

