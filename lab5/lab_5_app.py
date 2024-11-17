import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import threading
from lab5.key_manager import KeyManager
from lab5.signer import Signer
from lab5.verifier import Verifier


class CryptoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Digital Signature Tool")
        self.root.geometry("700x700")
        self.loading_label = None

        self.setup_menu()

    def setup_menu(self):
        self.clear_window()
        tk.Label(self.root, text="Digital Signature Tool", font=("Helvetica", 16)).pack(pady=10)
        tk.Button(self.root, text="Manage Keys", command=self.open_key_management_window).pack(pady=10)
        tk.Button(self.root, text="Sign Text or File", command=self.open_sign_window).pack(pady=10)
        tk.Button(self.root, text="Verify Signature", command=self.open_verify_window).pack(pady=10)
        tk.Button(self.root, text="Exit", command=self.root.quit).pack(pady=10)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def open_key_management_window(self):
        key_window = tk.Toplevel(self.root)
        key_window.title("Key Management")
        key_window.geometry("600x400")

        tk.Label(key_window, text="Manage Keys", font=("Helvetica", 14)).pack(pady=10)
        tk.Button(key_window, text="Generate Keys", command=self.generate_keys).pack(pady=10)
        tk.Button(key_window, text="Back to Main Menu", command=key_window.destroy).pack(pady=10)

    def generate_keys(self):
        save_dir = filedialog.askdirectory(title="Select Save Directory for Keys")
        if save_dir:
            private_key_path = f"{save_dir}/private_key.pem"
            public_key_path = f"{save_dir}/public_key.pem"
            KeyManager.generate_keys(private_key_path, public_key_path)
            messagebox.showinfo("Success", f"Keys saved to {save_dir}")

    def open_sign_window(self):
        sign_window = tk.Toplevel(self.root)
        sign_window.title("Sign Text or File")
        sign_window.geometry("600x400")

        tk.Label(sign_window, text="Sign Text or File", font=("Helvetica", 14)).pack(pady=10)
        tk.Button(sign_window, text="Sign Text", command=lambda: self.sign_text(sign_window)).pack(pady=10)
        tk.Button(sign_window, text="Sign File", command=self.sign_file).pack(pady=10)
        tk.Button(sign_window, text="Back to Main Menu", command=sign_window.destroy).pack(pady=10)

    def sign_text(self, parent_window):
        text = simpledialog.askstring("Input", "Enter text to sign:", parent=parent_window)
        private_key_file = filedialog.askopenfilename(title="Select Private Key File")
        if text and private_key_file:
            try:
                signature = Signer.sign_message(text, private_key_file)
                messagebox.showinfo("Signed", f"Signature (Hex): {signature}")
                self.save_to_file(signature, "Save Signature As")
            except Exception as e:
                messagebox.showerror("Error", f"Signing failed: {str(e)}")
        else:
            messagebox.showwarning("Warning", "Please provide both text and private key.")

    def sign_file(self):
        input_file = filedialog.askopenfilename(title="Select File to Sign")
        private_key_file = filedialog.askopenfilename(title="Select Private Key File")
        output_file = filedialog.asksaveasfilename(defaultextension=".sig", title="Save Signature File As")
        if input_file and private_key_file and output_file:
            try:
                signature = Signer.sign_message_file(input_file, private_key_file)
                with open(output_file, 'w') as f:
                    f.write(signature)
                messagebox.showinfo("Success", f"Signature saved to {output_file}")
            except Exception as e:
                messagebox.showerror("Error", f"File signing failed: {str(e)}")
        else:
            messagebox.showwarning("Warning", "Please provide all required inputs.")

    def _sign_file_thread(self, input_file, output_file):
        try:
            self.show_loading("Signing file...")
            signature = Signer.sign_message_file(input_file)
            with open(output_file, 'w') as f:
                f.write(signature)
            self.hide_loading()
            messagebox.showinfo("Success", f"Signature saved to {output_file}")
        except Exception as e:
            self.hide_loading()
            messagebox.showerror("Error", "File signing failed.")

    def open_verify_window(self):
        verify_window = tk.Toplevel(self.root)
        verify_window.title("Verify Signature")
        verify_window.geometry("600x400")

        tk.Label(verify_window, text="Verify Signature", font=("Helvetica", 14)).pack(pady=10)
        tk.Button(verify_window, text="Verify Text Signature", command=lambda: self.verify_text(verify_window)).pack(pady=10)
        tk.Button(verify_window, text="Verify File Signature", command=self.verify_file).pack(pady=10)
        tk.Button(verify_window, text="Back to Main Menu", command=verify_window.destroy).pack(pady=10)

    def verify_text(self, parent_window):
        text = simpledialog.askstring("Input", "Enter text to verify:", parent=parent_window)
        signature_hex = simpledialog.askstring("Input", "Enter signature (Hex):", parent=parent_window)
        public_key_file = filedialog.askopenfilename(title="Select Public Key File")
        if text and signature_hex and public_key_file:
            try:
                verified = Verifier.verify_signature(text, signature_hex, public_key_file)
                messagebox.showinfo("Verification", "Signature valid!" if verified else "Signature invalid!")
            except Exception as e:
                messagebox.showerror("Error", f"Verification failed: {str(e)}")
        else:
            messagebox.showwarning("Warning", "Please provide all required inputs.")

    def verify_file(self):
        input_file = filedialog.askopenfilename(title="Select File to Verify")
        signature_file = filedialog.askopenfilename(title="Select Signature File")
        public_key_file = filedialog.askopenfilename(title="Select Public Key File")
        if input_file and signature_file and public_key_file:
            try:
                with open(signature_file, 'r') as f:
                    signature_hex = f.read()
                verified = Verifier.verify_signature_file(input_file, signature_hex, public_key_file)
                messagebox.showinfo("Verification", "Signature valid!" if verified else "Signature invalid!")
            except Exception as e:
                messagebox.showerror("Error", f"Verification failed: {str(e)}")
        else:
            messagebox.showwarning("Warning", "Please provide all required inputs.")

    def _verify_file_thread(self, input_file, signature_file):
        try:
            self.show_loading("Verifying file...")
            with open(signature_file, 'r') as f:
                signature_hex = f.read()
            verified = Verifier.verify_signature_file(input_file, signature_hex)
            self.hide_loading()
            messagebox.showinfo("Verification", "Signature valid!" if verified else "Signature invalid!")
        except Exception as e:
            self.hide_loading()
            messagebox.showerror("Error", "File verification failed.")

    def save_to_file(self, content, title):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", title=title)
        if file_path:
            with open(file_path, "w") as file:
                file.write(content)
            messagebox.showinfo("Success", f"Content saved to {file_path}")

    def show_loading(self, text="Loading, please wait..."):
        self.loading_label = tk.Label(self.root, text=text, font=("Helvetica", 12))
        self.loading_label.pack(pady=10)
        self.root.update()

    def hide_loading(self):
        if self.loading_label:
            self.loading_label.destroy()
            self.loading_label = None
