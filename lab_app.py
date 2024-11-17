import tkinter as tk
from PIL import Image, ImageTk
from lab1.lab1_app import Lab1App
from lab2.lab2_app import Lab2App
from lab3.lab3_app import Lab3App
from lab4.rsa_app import RSAApp
from lab5.lab_5_app import CryptoApp


class LabNavigator:
    def __init__(self, root):
        self.root = root
        self.root.title("Lab Navigator")
        self.root.geometry("500x500")
        self.set_background()
        self.setup_menu()

    def set_background(self):
        image = Image.open("img.png")
        image = image.resize((500, 500), Image.Resampling.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(image)
        bg_label = tk.Label(self.root, image=self.bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    def setup_menu(self):
        label = tk.Label(self.root, text="Select a Lab", font=("Helvetica", 14), bg="lightblue")
        label.pack(pady=10)

        lab1_btn = tk.Button(self.root, text="Lab 1: PRNG (Custom vs System)", command=self.open_lab1)
        lab1_btn.pack(pady=10)
        lab2_btn = tk.Button(self.root, text="Lab 2 - MD5 Hashing", command=self.open_lab2)
        lab2_btn.pack(pady=10)
        lab3_btn = tk.Button(self.root, text="Lab 3 ", command=self.open_lab3)
        lab3_btn.pack(pady=10)
        lab4_btn = tk.Button(self.root, text="Lab 4 ", command=self.open_lab4)
        lab4_btn.pack(pady=10)
        lab5_btn = tk.Button(self.root, text="Lab 5 ", command=self.open_lab5)
        lab5_btn.pack(pady=10)

    def open_lab1(self):
        Lab1App(self.root)

    def open_lab2(self):
        Lab2App(self.root)

    def open_lab3(self):
        Lab3App(self.root)

    def open_lab4(self):
        RSAApp(self.root)

    def open_lab5(self):
        CryptoApp(self.root)

