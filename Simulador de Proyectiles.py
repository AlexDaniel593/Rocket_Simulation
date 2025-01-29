import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.image import imread
import tkinter as tk
from tkinter import Label, Entry, Button

def projectile_motion(v0, angle):
    angle_rad = np.radians(angle)

    v0x = v0 * np.cos(angle_rad)
    v0y = v0 * np.sin(angle_rad)

    g = 9.81

    t_flight = 2 * v0y / g  # Tiempo de vuelo
    dt = 0.01

    t = np.arange(0, t_flight, dt)
    x = v0x * t
    y = v0y * t - 0.5 * g * t ** 2

    x_max = max(x)  # Distancia máxima alcanzada
    y_max = (v0y ** 2) / (2 * g)  # Altura máxima alcanzada

    return x, y, t_flight, x_max, y_max

def animate(x, y):
    fig, ax = plt.subplots()
    ax.set_xlim(0, 100)  # Establecer límites de la longitud máxima (100 metros)
    ax.set_ylim(0, 150)   # Establecer límites de la altura máxima (150 metros)
    line, = ax.plot([], [], 'bo')

    rocket_img = imread('Rocket.png')  
    rocket_annotation = ax.imshow(rocket_img)
    rocket_annotation.set_visible(False)

    def update(i):
        line.set_data(x[:i], y[:i])

        if i > 0:
            rocket_annotation.set_visible(True)
            rocket_annotation.set_extent([x[i - 1], x[i - 1] + 10, y[i - 1], y[i - 1] + 10])
        else:
            rocket_annotation.set_visible(False)

        return line, rocket_annotation

    ani = animation.FuncAnimation(fig, update, frames=len(x), interval=10, blit=True)
    plt.xlabel('Distancia (m)')
    plt.ylabel('Altura (m)')
    plt.title('Movimiento del proyectil')
    plt.grid(True)
    plt.show()

def on_submit():
    try:
        v0 = float(entry_v0.get())
        angle = float(entry_angle.get())

        if not (0 <= angle <= 90):
            error_label.config(text="¡El ángulo de lanzamiento debe estar entre 0 y 90 grados!")
            return

        x, y, t_flight, x_max, y_max = projectile_motion(v0, angle)

        animate(x, y)

        # Mostrar valores calculados en la interfaz
        time_label.config(text=f"Tiempo de vuelo: {t_flight:.2f} s")
        xmax_label.config(text=f"Distancia máxima: {x_max:.2f} m")
        ymax_label.config(text=f"Altura máxima: {y_max:.2f} m")

        error_label.config(text="")
    except ValueError:
        error_label.config(text="¡Ingresa valores numéricos válidos!")

window = tk.Tk()
window.title("Simulador de Proyectiles")

entry_style = {'font': ('Arial', 14), 'width': 10, 'justify': 'center'}
label_style = {'font': ('Arial', 14)}

university_img = tk.PhotoImage(file='espe.png')
university_label = Label(window, image=university_img)
university_label.pack(pady=10)

title_label = Label(window, text="Simulador de Proyectiles", **label_style)
title_label.pack(pady=40)
title_label.config(font=('Arial', 18, 'bold'))

label_v0 = Label(window, text="Velocidad Inicial (m/s):", **label_style)
label_v0.pack()
entry_v0 = Entry(window, **entry_style)
entry_v0.pack(pady=10)

label_angle = Label(window, text="Ángulo de Lanzamiento (grados):", **label_style)
label_angle.pack()
entry_angle = Entry(window, **entry_style)
entry_angle.pack(pady=10)

error_label = Label(window, text="", fg="red", **label_style)
error_label.pack()

button_style = {'font': ('Arial', 16), 'bg': 'green', 'fg': 'white', 'relief': 'raised'}
btn_calculate = Button(window, text="Calcular", command=on_submit, **button_style)
btn_calculate.pack(pady=10)

# Etiquetas para mostrar resultados
time_label = Label(window, text="Tiempo de vuelo: -- s", **label_style)
time_label.pack(pady=5)

xmax_label = Label(window, text="Distancia máxima: -- m", **label_style)
xmax_label.pack(pady=5)

ymax_label = Label(window, text="Altura máxima: -- m", **label_style)
ymax_label.pack(pady=5)

developers_label = Label(window, text="Desarrollado por: Daniel Guaman", **label_style)
developers_label.pack(pady=30)
developers_label.config(font=('Arial', 14, 'italic'))

window.update_idletasks()
window.mainloop()
