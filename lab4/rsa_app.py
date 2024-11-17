import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import threading
import subprocess
from lab4.rsa_handler import RSAHandler


class RSAApp:
    def __init__(self, root):
        self.root = root
        self.root.title("RSA Encryption/Decryption")
        self.root.geometry("700x700")
        self.loading_label = None
        self.rsa_handler = RSAHandler()
        self.setup_menu()

    def setup_menu(self):
        self.clear_window()
        tk.Label(self.root, text="RSA Encryption/Decryption", font=("Helvetica", 14)).pack(pady=10)
        tk.Button(self.root, text="Encrypt/Decrypt Text", command=self.open_text_window).pack(pady=10)
        tk.Button(self.root, text="Encrypt/Decrypt File", command=self.open_file_window).pack(pady=10)
        tk.Button(self.root, text="Run Tests", command=self.run_tests).pack(pady=10)
        tk.Button(self.root, text="Exit", command=self.root.quit).pack(pady=10)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_loading(self, text="Loading, please wait..."):
        self.loading_label = tk.Label(self.root, text=text, font=("Helvetica", 12))
        self.loading_label.pack(pady=10)
        self.root.update()

    def hide_loading(self):
        if self.loading_label:
            self.loading_label.destroy()
            self.loading_label = None

    def open_text_window(self):
        text_window = tk.Toplevel(self.root)
        text_window.title("Text Encryption/Decryption")
        text_window.geometry("600x400")
        tk.Label(text_window, text="Text Encryption/Decryption", font=("Helvetica", 14)).pack(pady=10)

        tk.Button(text_window, text="Encrypt Text", command=lambda: self.encrypt_text(text_window)).pack(pady=10)
        tk.Button(text_window, text="Decrypt Text", command=lambda: self.decrypt_text(text_window)).pack(pady=10)
        tk.Button(text_window, text="Back to Main Menu", command=text_window.destroy).pack(pady=10)

    def open_file_window(self):
        file_window = tk.Toplevel(self.root)
        file_window.title("File Encryption/Decryption")
        file_window.geometry("600x400")
        tk.Label(file_window, text="File Encryption/Decryption", font=("Helvetica", 14)).pack(pady=10)

        tk.Button(file_window, text="Encrypt File", command=self.encrypt_file).pack(pady=10)
        tk.Button(file_window, text="Decrypt File", command=self.decrypt_file).pack(pady=10)
        tk.Button(file_window, text="Back to Main Menu", command=file_window.destroy).pack(pady=10)

    def encrypt_text(self, parent_window):
        plaintext = simpledialog.askstring("Input", "Enter text to encrypt:", parent=parent_window)
        if plaintext:
            ciphertext = self.rsa_handler.encrypt(plaintext.encode())
            messagebox.showinfo("Encrypted", f"Encrypted text (hex): {ciphertext.hex()}")
            self.save_to_file(ciphertext.hex(), "Save Encrypted Text As")

    def decrypt_text(self, parent_window):
        ciphertext_hex = simpledialog.askstring("Input", "Enter encrypted text (hex):", parent=parent_window)
        if ciphertext_hex:
            try:
                ciphertext = bytes.fromhex(ciphertext_hex)
                plaintext = self.rsa_handler.decrypt(ciphertext)
                messagebox.showinfo("Decrypted", f"Decrypted text: {plaintext.decode()}")
                self.save_to_file(plaintext.decode(), "Save Decrypted Text As")
            except Exception as e:
                messagebox.showerror("Error", "Decryption failed.")

    def encrypt_file(self):
        input_file = filedialog.askopenfilename(title="Select File to Encrypt")
        output_file = filedialog.asksaveasfilename(defaultextension=".enc", title="Save Encrypted File As")
        if input_file and output_file:
            threading.Thread(target=self._encrypt_file_thread, args=(input_file, output_file)).start()

    def _encrypt_file_thread(self, input_file, output_file):
        try:
            self.show_loading()
            with open(input_file, 'rb') as f:
                plaintext = f.read()
            encrypted = self.rsa_handler.encrypt(plaintext)
            with open(output_file, 'wb') as f:
                f.write(encrypted)
            self.hide_loading()
            messagebox.showinfo("Success", f"File encrypted as {output_file}")
        except Exception as e:
            self.hide_loading()
            messagebox.showerror("Error", "File encryption failed.")

    def decrypt_file(self):
        input_file = filedialog.askopenfilename(title="Select File to Decrypt")
        output_file = filedialog.asksaveasfilename(defaultextension=".dec", title="Save Decrypted File As")
        if input_file and output_file:
            threading.Thread(target=self._decrypt_file_thread, args=(input_file, output_file)).start()

    def _decrypt_file_thread(self, input_file, output_file):
        try:
            self.show_loading()
            with open(input_file, 'rb') as f:
                encrypted = f.read()
            decrypted = self.rsa_handler.decrypt(encrypted)
            with open(output_file, 'wb') as f:
                f.write(decrypted)
            self.hide_loading()
            messagebox.showinfo("Success", f"File decrypted as {output_file}")
        except Exception as e:
            self.hide_loading()
            messagebox.showerror("Error", "File decryption failed.")

    def save_to_file(self, content, title):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", title=title)
        if file_path:
            with open(file_path, "w") as file:
                file.write(content)
            messagebox.showinfo("Success", f"Content saved to {file_path}")

    def run_tests(self):
        threading.Thread(target=self._run_tests_thread).start()

    def _run_tests_thread(self):
        self.show_loading("Running tests, please wait...")
        try:
            result = subprocess.run(
                ["python", "-m", "unittest", "discover", "-s", "tests"],
                capture_output=True,
                text=True,
            )
            self.hide_loading()
            if result.returncode == 0:
                messagebox.showinfo("Test Results", "All tests passed successfully!")
            else:
                messagebox.showerror("Test Results", "Some tests failed. Check logs for details.")
        except Exception as e:
            self.hide_loading()
            messagebox.showerror("Error", f"Failed to run tests: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = RSAApp(root)
    root.mainloop()
