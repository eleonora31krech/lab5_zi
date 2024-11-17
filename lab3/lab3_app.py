import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import threading

from lab2.utils import clear_window
from lab3.rc5_cbc import RC5CBCPad
from lab3.file_handler import FileHandler
from lab3.iv_generator import LemerRandom
from lab2.hash_validator import HashValidator

class Lab3App:
    def __init__(self, root):
        self.root = root
        self.root.title("RC5 CBC Pad Encryption/Decryption")
        self.root.geometry("700x700")
        self.loading_label = None
        self.setup_menu()

    def setup_menu(self):
        clear_window(self.root)
        tk.Label(self.root, text="RC5 CBC Pad Encryption/Decryption", font=("Helvetica", 14)).pack(pady=10)
        tk.Button(self.root, text="Encrypt a File", command=self.encrypt_file).pack(pady=10)
        tk.Button(self.root, text="Decrypt a File", command=self.decrypt_file).pack(pady=10)
        tk.Button(self.root, text="Encrypt Text", command=self.encrypt_text).pack(pady=10)
        tk.Button(self.root, text="Decrypt Text", command=self.decrypt_text).pack(pady=10)
        tk.Button(self.root, text="Exit", command=self.root.quit).pack(pady=10)

    def show_loading(self):
        """Display a loading message."""
        self.loading_label = tk.Label(self.root, text="Loading, please wait...", font=("Helvetica", 12))
        self.loading_label.pack(pady=10)
        self.root.update()

    def hide_loading(self):
        """Remove the loading message."""
        if self.loading_label:
            self.loading_label.destroy()
            self.loading_label = None

    def get_passcode_and_rc5(self):
        passcode = simpledialog.askstring("Password", "Enter the password:")
        if passcode:
            try:
                key = self.derive_key(passcode)
                rc5 = RC5CBCPad(key, word_size=16, num_rounds=20)
                return rc5
            except Exception as e:
                messagebox.showerror("Error", "Could not generate key. Please try again.")
        else:
            messagebox.showwarning("Input Error", "Password cannot be empty.")
        return None

    def derive_key(self, passphrase):
        passphrase_bytes = passphrase.encode('utf-8')
        md5_hash = HashValidator.md5(passphrase_bytes)
        key = bytes.fromhex(md5_hash)
        return key

    def encrypt_file(self):
        rc5 = self.get_passcode_and_rc5()
        if rc5:
            input_filename = filedialog.askopenfilename(title="Select File to Encrypt")
            output_filename = filedialog.asksaveasfilename(defaultextension=".enc", title="Save Encrypted File As")
            if input_filename and output_filename:
                threading.Thread(target=self._encrypt_file_thread, args=(rc5, input_filename, output_filename)).start()

    def _encrypt_file_thread(self, rc5, input_filename, output_filename):
        try:
            self.show_loading()
            file_handler = FileHandler(rc5)
            seed = rc5.generate_seed()
            lemer_generator = LemerRandom(seed)
            iv = lemer_generator.get_bytes(rc5.block_size)
            file_handler.encrypt_file(input_filename, output_filename, iv)
            self.hide_loading()
            messagebox.showinfo("Success", f"File '{input_filename}' encrypted to '{output_filename}'")
        except Exception as e:
            self.hide_loading()
            messagebox.showerror("Error", "Encryption failed. Please try again.")

    def decrypt_file(self):
        rc5 = self.get_passcode_and_rc5()
        if rc5:
            input_filename = filedialog.askopenfilename(title="Select File to Decrypt")
            output_filename = filedialog.asksaveasfilename(defaultextension=".dec", title="Save Decrypted File As")
            if input_filename and output_filename:
                threading.Thread(target=self._decrypt_file_thread, args=(rc5, input_filename, output_filename)).start()

    def _decrypt_file_thread(self, rc5, input_filename, output_filename):
        try:
            self.show_loading()
            file_handler = FileHandler(rc5)
            file_handler.decrypt_file(input_filename, output_filename)
            self.hide_loading()
            messagebox.showinfo("Success", f"File '{input_filename}' decrypted to '{output_filename}'")
        except ValueError as e:
            self.hide_loading()
            messagebox.showerror("Error", "Decryption failed. Invalid input or wrong file. Please try again.")
        except Exception as e:
            self.hide_loading()
            messagebox.showerror("Error", "Decryption failed. Please try again.")

    def encrypt_text(self):
        rc5 = self.get_passcode_and_rc5()
        if rc5:
            plaintext = simpledialog.askstring("Input", "Enter text to encrypt:")
            if plaintext:
                threading.Thread(target=self._encrypt_text_thread, args=(rc5, plaintext)).start()

    def _encrypt_text_thread(self, rc5, plaintext):
        try:
            self.show_loading()
            seed = rc5.generate_seed()
            lemer_generator = LemerRandom(seed)
            iv = lemer_generator.get_bytes(rc5.block_size)
            plaintext_bytes = plaintext.encode('utf-8')
            ciphertext = rc5.encrypt(plaintext_bytes, iv)
            ciphertext_hex = ciphertext.hex()
            self.hide_loading()
            messagebox.showinfo("Encrypted", f"Encrypted text (hex): {ciphertext_hex}")
        except Exception as e:
            self.hide_loading()
            messagebox.showerror("Error", "Encryption failed. Please try again.")

    def decrypt_text(self):
        rc5 = self.get_passcode_and_rc5()
        if rc5:
            ciphertext_input = simpledialog.askstring("Input", "Enter ciphertext (hex) to decrypt:")
            if ciphertext_input:
                threading.Thread(target=self._decrypt_text_thread, args=(rc5, ciphertext_input)).start()

    def _decrypt_text_thread(self, rc5, ciphertext_input):
        try:
            self.show_loading()
            ciphertext = bytes.fromhex(ciphertext_input.strip())
            if len(ciphertext) < rc5.block_size:
                raise ValueError("Ciphertext is too short to contain valid IV and data.")
            iv = ciphertext[:rc5.block_size]
            ciphertext = ciphertext[rc5.block_size:]
            decrypted = rc5.decrypt(ciphertext, iv)
            decrypted_text = decrypted.decode("utf-8")
            self.hide_loading()
            messagebox.showinfo("Decrypted", f"Decrypted text: {decrypted_text}")
        except UnicodeDecodeError:
            self.hide_loading()
            messagebox.showinfo("Decrypted", "Decryption succeeded, but the result appears to be binary.")
        except ValueError:
            self.hide_loading()
            messagebox.showerror("Error", "Invalid ciphertext format or data. Please try again.")
        except Exception as e:
            self.hide_loading()
            messagebox.showerror("Error", "Decryption failed. Please try again.")

if __name__ == "__main__":
    root = tk.Tk()
    app = Lab3App(root)
    root.mainloop()
