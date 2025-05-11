# OpenTimber - A cross-platform GUI application
# Created by: Eren Özer
# Version: 1.0
# License: GNU General Public License v3.0

import tkinter as tk
from tkinter import messagebox, filedialog
import math
import csv

class OpenTimber:
    def __init__(self, root):
        self.root = root
        # Store tuples: (formula, d1_cm, d2_cm or '', length_m, volume)
        self.kubaj_list = []
        self.current_formula = None

        self.root.title("OpenTimber")
        self.root.geometry("800x600")

        # Frame for formula-specific content at the top
        self.content_frame = tk.Frame(self.root)
        self.content_frame.pack(fill=tk.X, padx=20, pady=20)

        # Container for results, centered under content
        self.results_container = tk.Frame(self.root)
        self.results_container.pack(pady=(0, 10))

        # Scrollable canvas for results
        self.results_canvas = tk.Canvas(self.results_container, width=600, height=200)
        self.results_scrollbar = tk.Scrollbar(self.results_container, orient="vertical", command=self.results_canvas.yview)
        self.results_canvas.configure(yscrollcommand=self.results_scrollbar.set)
        self.results_canvas.grid(row=0, column=0)
        self.results_scrollbar.grid(row=0, column=1, sticky='ns')

        # Frame inside canvas for result rows
        self.results_frame = tk.Frame(self.results_canvas)
        self.results_canvas.create_window((0,0), window=self.results_frame, anchor='nw')
        self.results_frame.bind(
            '<Configure>',
            lambda e: self.results_canvas.configure(scrollregion=self.results_canvas.bbox('all'))
        )

        # Global mouse wheel bindings for Windows and Linux
        self.root.bind_all('<MouseWheel>', self._on_mousewheel)
        self.root.bind_all('<Button-4>', lambda e: self.results_canvas.yview_scroll(-1, 'units'))  # Linux scroll up
        self.root.bind_all('<Button-5>', lambda e: self.results_canvas.yview_scroll(1, 'units'))   # Linux scroll down

        # Back button, centered under results
        self.back_button = tk.Button(self.root, text="Back", command=self.show_main_menu)
        self.back_button.pack_forget()

        self.show_main_menu()

    def _on_mousewheel(self, event):
        # Windows scroll
        self.results_canvas.yview_scroll(int(-1*(event.delta/120)), 'units')

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_main_menu(self):
        self.clear_content()
        self.back_button.pack_forget()

        tk.Label(self.content_frame, text="Select Formula", font=("Arial", 16)).pack(pady=10)
        tk.Button(self.content_frame, text="Huber Formula", command=self.show_huber_ui, width=20).pack(pady=5)
        tk.Button(self.content_frame, text="Smalian Formula", command=self.show_smalian_ui, width=20).pack(pady=5)

    def show_huber_ui(self):
        self.current_formula = "Huber"
        self.clear_content()
        self.back_button.pack(pady=(5, 10))

        top_frame = tk.Frame(self.content_frame)
        top_frame.pack(fill=tk.X, pady=5)
        tk.Button(top_frame, text="Save to File", command=self.save_to_file).pack(side=tk.LEFT)
        tk.Button(top_frame, text="Clear All", command=self.clear_all).pack(side=tk.RIGHT)

        tk.Label(self.content_frame, text="Huber Formula", font=("Arial", 14)).pack(pady=5)
        tk.Label(self.content_frame, text="Diameter (cm):").pack()
        self.entry_diameter = tk.Entry(self.content_frame)
        self.entry_diameter.pack()

        tk.Label(self.content_frame, text="Length (m):").pack()
        self.entry_length = tk.Entry(self.content_frame)
        self.entry_length.pack()

        tk.Button(self.content_frame, text="Calculate", command=self.calculate_huber).pack(pady=10)

    def show_smalian_ui(self):
        self.current_formula = "Smalian"
        self.clear_content()
        self.back_button.pack(pady=(5, 10))

        top_frame = tk.Frame(self.content_frame)
        top_frame.pack(fill=tk.X, pady=5)
        tk.Button(top_frame, text="Save to File", command=self.save_to_file).pack(side=tk.LEFT)
        tk.Button(top_frame, text="Clear All", command=self.clear_all).pack(side=tk.RIGHT)

        tk.Label(self.content_frame, text="Smalian Formula", font=("Arial", 14)).pack(pady=5)
        tk.Label(self.content_frame, text="Small End Diameter (cm):").pack()
        self.entry_small_d = tk.Entry(self.content_frame)
        self.entry_small_d.pack()

        tk.Label(self.content_frame, text="Large End Diameter (cm):").pack()
        self.entry_large_d = tk.Entry(self.content_frame)
        self.entry_large_d.pack()

        tk.Label(self.content_frame, text="Length (m):").pack()
        self.entry_length = tk.Entry(self.content_frame)
        self.entry_length.pack()

        tk.Button(self.content_frame, text="Calculate", command=self.calculate_smalian).pack(pady=10)

    def calculate_huber(self):
        try:
            d1 = float(self.entry_diameter.get())
            length_m = float(self.entry_length.get())
            volume = (math.pi / 4) * (d1 / 100) ** 2 * length_m
            self.kubaj_list.append(("Huber", d1, "", length_m, volume))
            self.update_results()
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numeric values.")

    def calculate_smalian(self):
        try:
            d1 = float(self.entry_small_d.get())
            d2 = float(self.entry_large_d.get())
            length_m = float(self.entry_length.get())
            dm1 = d1 / 100
            dm2 = d2 / 100
            area_avg = (math.pi / 4) * (dm1 ** 2 + dm2 ** 2) / 2
            volume = area_avg * length_m
            self.kubaj_list.append(("Smalian", d1, d2, length_m, volume))
            self.update_results()
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numeric values.")

    def update_results(self):
        # Clear previous rows
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        # Populate rows
        for idx, (formula, d1, d2, length_m, volume) in enumerate(self.kubaj_list):
            row = tk.Frame(self.results_frame)
            row.pack(fill=tk.X, pady=2)
            text = f"[{formula}] "
            if formula == "Huber":
                text += f"d={d1}cm, l={length_m}m: {volume:.5f} m³"
            else:
                text += f"d1={d1}cm, d2={d2}cm, l={length_m}m: {volume:.5f} m³"
            tk.Label(row, text=text).pack(side=tk.LEFT, expand=True)
            del_btn = tk.Button(row, text="✕", fg="black", command=lambda i=idx: self.delete_result(i))
            del_btn.pack(side=tk.RIGHT, padx=20)
        # Scroll to latest entry
        self.results_canvas.update_idletasks()
        self.results_canvas.yview_moveto(1.0)

    def delete_result(self, index):
        del self.kubaj_list[index]
        self.update_results()

    def save_to_file(self):
        if not self.kubaj_list:
            messagebox.showwarning("Nothing to Save", "No data to save.")
            return
        filepath = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV File", "*.csv")])
        if filepath:
            try:
                with open(filepath, 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(["Formula", "Diameter1 (cm)", "Diameter2 (cm)", "Length (m)", "Volume (m³)"])
                    for formula, d1, d2, length_m, volume in self.kubaj_list:
                        writer.writerow([formula, d1, d2, length_m, f"{volume:.5f}"])
                messagebox.showinfo("Success", "File saved successfully as CSV.")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file:\n{e}")

    def clear_all(self):
        if messagebox.askyesno("Clear All", "Are you sure you want to clear all results?"):
            self.kubaj_list.clear()
            self.update_results()

if __name__ == "__main__":
    root = tk.Tk()
    app = OpenTimber(root)
    root.mainloop()

