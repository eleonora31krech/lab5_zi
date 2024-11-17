import tkinter as tk
from tkinter import messagebox, filedialog
import time
import threading
from lab1.lcg import LCGGenerator
from lab1.chebyshev import ChebyshevTest
from common.utils import clear_window
from lab1.constants import LCG_MODULUS, LCG_MULTIPLIER, LCG_INCREMENT, LCG_SEED

class Lab1App:
    def __init__(self, root):
        self.root = root
        self.root.title("Lab 1 (Custom vs System)")
        self.root.geometry("700x700")
        self.lcg_generator = LCGGenerator(LCG_MODULUS, LCG_MULTIPLIER, LCG_INCREMENT, LCG_SEED )
        self.setup_menu()

    def setup_menu(self):
        clear_window(self.root)
        label = tk.Label(self.root, text="Lab 1 (Custom vs System)", font=("Helvetica", 14))
        label.pack(pady=10)

        num_label = tk.Label(self.root, text="Enter number of values to generate:")
        num_label.pack()

        self.num_entry = tk.Entry(self.root)
        self.num_entry.pack(pady=5)

        generate_btn = tk.Button(self.root, text="Generate", command=self.validate_input)
        generate_btn.pack(pady=10)

    def validate_input(self):
        try:
            input_value = self.num_entry.get().strip()
            if not input_value:
                raise ValueError("Input cannot be empty!")

            if input_value.isalpha():
                raise ValueError("Please enter an integer value, not letters!")

            if input_value.startswith("0") and len(input_value) > 1:
                raise ValueError("Please enter a valid positive integer without leading zeros!")

            if len(input_value) > 6:
                raise ValueError("The number is too long! Please enter a smaller number.")

            num_values_float = float(input_value)

            if num_values_float <= 0:
                raise ValueError("Please enter a positive number!")

            if not num_values_float.is_integer():
                rounded_num_values = round(num_values_float)
                messagebox.showinfo("Rounding Applied", f"The number was rounded to {rounded_num_values}.")
            else:
                rounded_num_values = int(num_values_float)

            if rounded_num_values == 1:
                raise ValueError("Generating 1 value is not allowed. Please enter a value greater than 1.")

            self.show_loading_and_run(rounded_num_values)

        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

    def show_loading_and_run(self, num_values):
        loading_label = tk.Label(self.root, text="Processing...", font=("Helvetica", 10))
        loading_label.pack(pady=10)

        threading.Thread(target=self.generate_sequence, args=(num_values, loading_label)).start()

    def calculate_period(self, sequence):
        first_value = sequence[0]
        for i in range(1, len(sequence)):
            if sequence[i] == first_value:
                return i
        return len(sequence)

    def generate_sequence(self, num_values, loading_label):
        try:
            time.sleep(2)  # Імітація затримки

            start_time_custom = time.time()
            sequence_custom = self.lcg_generator.lcg_generator_numpy(num_values)
            custom_generation_time = time.time() - start_time_custom

            start_time_system = time.time()
            sequence_system = LCGGenerator.system_random_generator(num_values)
            system_generation_time = time.time() - start_time_system

            displayed_sequence_custom = ", ".join(str(x) for x in sequence_custom[:20])
            displayed_sequence_system = ", ".join(str(x) for x in sequence_system[:20])

            period_custom = self.calculate_period(sequence_custom)
            period_system = self.calculate_period(sequence_system)

            chebyshev_start_time_custom = time.time()
            pi_estimate_custom = ChebyshevTest.chebyshev_test_parallel(sequence_custom)
            chebyshev_time_custom = time.time() - chebyshev_start_time_custom

            pi_text_custom = f"Pi Estimate (Custom LCG): {pi_estimate_custom:.5f}" if pi_estimate_custom != float('inf') else "Pi Estimate: Undefined (not enough coprime pairs)"

            chebyshev_start_time_system = time.time()
            pi_estimate_system = ChebyshevTest.chebyshev_test_parallel(sequence_system)
            chebyshev_time_system = time.time() - chebyshev_start_time_system

            pi_text_system = f"Pi Estimate (System): {pi_estimate_system:.5f}" if pi_estimate_system != float('inf') else "Pi Estimate: Undefined (not enough coprime pairs)"
            displayed_sequence_custom = ", ".join(str(x) for x in sequence_custom[:20])
            displayed_sequence_system = ", ".join(str(x) for x in sequence_system[:20])
            result_text = (
                f"\nGenerated {num_values} values.\n"
                f"Custom LCG - Period: {period_custom} (Time: {custom_generation_time:.2f}s)\n"
                f"{pi_text_custom}\n"
                f"Sequence Generation Time (Custom LCG): {custom_generation_time:.2f}s\n"
                f"Chebyshev Test Time (Custom LCG): {chebyshev_time_custom:.2f}s\n\n"

                f"System Random Generator - Period: {period_system} (Time: {system_generation_time:.2f}s)\n"
                f"{pi_text_system}\n"
                f"Sequence Generation Time (System): {system_generation_time:.2f}s\n"
                f"Chebyshev Test Time (System): {chebyshev_time_system:.2f}s"
                f"Generated Sequences (first 20 values):\n"
                f"Custom: {displayed_sequence_custom}\n"
                f"System: {displayed_sequence_system}\n"
            )



            clear_window(self.root)
            result_label = tk.Label(self.root, text=result_text, font=("Helvetica", 10), wraplength=600)
            result_label.pack(pady=10)

            back_btn = tk.Button(self.root, text="Back", command=self.setup_menu)
            back_btn.pack(pady=10)

            self.ask_save_file(sequence_custom, sequence_system)

        except Exception as e:
            loading_label.destroy()
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

    def ask_save_file(self, sequence_custom, sequence_system):
        save = messagebox.askyesno("Save Results", "Do you want to save the results?")
        if save:
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text file", "*.txt")])
            if file_path:
                with open(file_path, 'w') as f:
                    f.write("Custom LCG Generated Sequence:\n")
                    for value in sequence_custom:
                        f.write(f"{value}\n")
                    f.write("\nSystem Random Generator Sequence:\n")
                    for value in sequence_system:
                        f.write(f"{value}\n")
                messagebox.showinfo("Success", "Results saved successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = Lab1App(root)
    root.mainloop()
