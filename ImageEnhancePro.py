import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
import cv2
from PIL import Image, ImageTk
import numpy as np
import matplotlib.pyplot as plt

# Fungsi untuk membuka file gambar
def open_file():
    global img, img_gray
    file_path = filedialog.askopenfilename()
    if file_path:
        img = cv2.imread(file_path)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        display_image(img, original_image_label)
    else:
        messagebox.showerror("Error", "File tidak ditemukan")

# Fungsi untuk menampilkan gambar pada label
def display_image(image, label):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(image)
    image = ImageTk.PhotoImage(image)
    label.configure(image=image)
    label.image = image

# Fungsi untuk menyimpan gambar yang telah diproses
def save_image():
    if 'filtered_img' in globals():
        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if save_path:
            cv2.imwrite(save_path, filtered_img)
            messagebox.showinfo("Success", "Gambar berhasil disimpan")
    else:
        messagebox.showerror("Error", "Tidak ada gambar yang diproses untuk disimpan")

# Fungsi untuk menerapkan filter median
def apply_median_filter():
    global filtered_img
    kernel_size = int(median_slider.get())
    filtered_img = cv2.medianBlur(img, kernel_size)
    display_image(filtered_img, processed_image_label)
    update_histogram()

# Fungsi untuk menerapkan filter rata-rata
def apply_average_filter():
    global filtered_img
    kernel_size = int(average_slider.get())
    filtered_img = cv2.blur(img, (kernel_size, kernel_size))
    display_image(filtered_img, processed_image_label)
    update_histogram()

# Fungsi untuk menampilkan histogram
def update_histogram():
    if 'filtered_img' in globals():
        fig, axs = plt.subplots(1, 2, figsize=(10, 4))

        axs[0].hist(img_gray.ravel(), bins=256, color='gray')
        axs[0].set_title('Histogram Gambar Asli')

        gray_filtered = cv2.cvtColor(filtered_img, cv2.COLOR_BGR2GRAY)
        axs[1].hist(gray_filtered.ravel(), bins=256, color='gray')
        axs[1].set_title('Histogram Gambar yang Diproses')

        plt.show()

# Membuat jendela utama aplikasi
app = ctk.CTk()
app.title("Image Enhancement Application")
app.geometry("1000x700")

# Menu Bar
menu_bar = tk.Menu(app)
app.config(menu=menu_bar)

file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_image)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=app.quit)

# Menambahkan frame untuk gambar
frame = ctk.CTkFrame(app)
frame.pack(pady=10)

# Menambahkan label untuk menampilkan gambar asli dan hasil perbaikan
original_image_label = ctk.CTkLabel(frame, text="")  # Tidak ada teks yang ditampilkan
original_image_label.grid(row=0, column=0, padx=10)

processed_image_label = ctk.CTkLabel(frame, text="")  # Tidak ada teks yang ditampilkan
processed_image_label.grid(row=0, column=1, padx=10)

# Tombol dan slider untuk filter
controls_frame = ctk.CTkFrame(app)
controls_frame.pack(pady=10)

median_label = ctk.CTkLabel(controls_frame, text="Median Filter Kernel Size:")
median_label.grid(row=0, column=0, padx=10, pady=5)

median_slider = ctk.CTkSlider(controls_frame, from_=1, to=10, number_of_steps=9)
median_slider.set(3)
median_slider.grid(row=0, column=1, padx=10, pady=5)

median_button = ctk.CTkButton(controls_frame, text="Apply Median Filter", command=apply_median_filter)
median_button.grid(row=0, column=2, padx=10, pady=5)

average_label = ctk.CTkLabel(controls_frame, text="Average Filter Kernel Size:")
average_label.grid(row=1, column=0, padx=10, pady=5)

average_slider = ctk.CTkSlider(controls_frame, from_=1, to=10, number_of_steps=9)
average_slider.set(3)
average_slider.grid(row=1, column=1, padx=10, pady=5)

average_button = ctk.CTkButton(controls_frame, text="Apply Average Filter", command=apply_average_filter)
average_button.grid(row=1, column=2, padx=10, pady=5)

# Menjalankan aplikasi
app.mainloop()
