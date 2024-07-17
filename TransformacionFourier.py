import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
import scipy.special
from matplotlib.figure import Figure

def plot_signal_and_transform(signal, t, ax1, ax2):
    # Graficar la señal original
    ax1.clear()
    ax1.plot(t, signal)
    ax1.set_title('Señal Original')
    ax1.set_xlabel('Tiempo')
    ax1.set_ylabel('Amplitud')

    # Calcular y graficar la Transformada de Fourier
    fourier = np.fft.fft(signal)
    freq = np.fft.fftfreq(signal.shape[-1], t[1] - t[0])

    ax2.clear()
    ax2.plot(freq, np.abs(fourier))
    ax2.set_title('Transformada de Fourier')
    ax2.set_xlabel('Frecuencia')
    ax2.set_ylabel('Amplitud')

def create_signal(func, t):
    return eval(func)

def update_plot():
    func = function_entry.get()
    try:
        signal = create_signal(func, t)
        plot_signal_and_transform(signal, t, ax1, ax2)
        canvas.draw()
        error_label.config(text="")
    except Exception as e:
        error_label.config(text=f"Error: {str(e)}")

def on_example_select(event):
    selected = example_listbox.get(example_listbox.curselection())
    function_entry.delete(0, tk.END)
    function_entry.insert(0, examples[selected]['function'])

    # Actualizar las ecuaciones LaTeX
    original_eq.set_text(examples[selected]['notation']['original'])
    transform_eq.set_text(examples[selected]['notation']['transform'])
    eq_fig.canvas.draw()

    explanation_text.delete('1.0', tk.END)
    explanation_text.insert(tk.END, f"Explicación: {examples[selected]['explanation']}")
    update_plot()

# Crear la ventana principal
window = tk.Tk()
window.title('Aprendiendo Transformadas de Fourier')
window.geometry('1400x900')

# Crear el marco principal
main_frame = ttk.Frame(window)
main_frame.pack(fill=tk.BOTH, expand=True)

# Crear el marco izquierdo para la lista de ejemplos
left_frame = ttk.Frame(main_frame, width=200)
left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

# Crear la lista de ejemplos
example_listbox = tk.Listbox(left_frame, width=30)
example_listbox.pack(fill=tk.BOTH, expand=True)
example_listbox.bind('<<ListboxSelect>>', on_example_select)

# Crear el marco central para los gráficos
center_frame = ttk.Frame(main_frame)
center_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

# Crear los gráficos
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8))
canvas = FigureCanvasTkAgg(fig, master=center_frame)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Crear el marco derecho para la explicación, ecuaciones y entrada de función
right_frame = ttk.Frame(main_frame, width=400)
right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

# Crear figura para las ecuaciones LaTeX
eq_fig = Figure(figsize=(5, 2))
eq_ax = eq_fig.add_subplot(111)
eq_ax.axis('off')
original_eq = eq_ax.text(0.05, 0.7, '', fontsize=12)
transform_eq = eq_ax.text(0.05, 0.3, '', fontsize=12)
eq_canvas = FigureCanvasTkAgg(eq_fig, master=right_frame)
eq_canvas.draw()
eq_canvas.get_tk_widget().pack(pady=10)

# Crear el cuadro de texto para la explicación
explanation_text = tk.Text(right_frame, wrap=tk.WORD, width=40, height=10)
explanation_text.pack(fill=tk.BOTH, expand=True)

# Crear la entrada de función y el botón de actualización
function_label = ttk.Label(right_frame, text="Función:")
function_label.pack(pady=(10, 0))
function_entry = ttk.Entry(right_frame, width=40)
function_entry.pack()
update_button = ttk.Button(right_frame, text="Actualizar", command=update_plot)
update_button.pack(pady=10)

# Etiqueta para mostrar errores
error_label = ttk.Label(right_frame, text="", foreground="red", wraplength=350)
error_label.pack()

# Definir el rango de tiempo
t = np.linspace(-10, 10, 1000)

# Definir ejemplos
examples = {
    "1. Delta de Dirac": {
        "function": "np.where(np.abs(t) < 0.01, 1, 0)",
        "notation": {
            "original": r"$\delta(t)$",
            "transform": r"$\mathcal{F}\{\delta(t)\} = 1$"
        },
        "explanation": "La transformada de Fourier de una delta de Dirac es una constante en todas las frecuencias."
    },
    "2. Función escalón unitario": {
        "function": "np.heaviside(t, 0.5)",
        "notation": {
            "original": r"$u(t)$",
            "transform": r"$\mathcal{F}\{u(t)\} = \pi\delta(\omega) + \frac{1}{j\omega}$"
        },
        "explanation": "La transformada del escalón unitario tiene un pico en frecuencia cero y decrece como 1/f."
    },
    "3. Función rampa": {
        "function": "np.maximum(t, 0)",
        "notation": {
            "original": r"$tu(t)$",
            "transform": r"$\mathcal{F}\{tu(t)\} = \pi\delta'(\omega) + \frac{1}{(j\omega)^2}$"
        },
        "explanation": "La transformada de la función rampa tiene un pico agudo en frecuencia cero y decrece como 1/f^2."
    },
    "4. Función exponencial decreciente": {
        "function": "np.exp(-np.abs(t))",
        "notation": {
            "original": r"$e^{-|t|}$",
            "transform": r"$\mathcal{F}\{e^{-|t|}\} = \frac{2}{1+\omega^2}$"
        },
        "explanation": "La transformada de una exponencial decreciente es una función lorentziana."
    },
    "5. Función seno": {
        "function": "np.sin(2 * np.pi * t)",
        "notation": {
            "original": r"$\sin(\omega_0 t)$",
            "transform": r"$\mathcal{F}\{\sin(\omega_0 t)\} = \frac{j}{2}[\delta(\omega-\omega_0) - \delta(\omega+\omega_0)]$"
        },
        "explanation": "La transformada del seno son dos deltas en las frecuencias positiva y negativa correspondientes."
    },
    "6. Función coseno": {
        "function": "np.cos(2 * np.pi * t)",
        "notation": {
            "original": r"$\cos(\omega_0 t)$",
            "transform": r"$\mathcal{F}\{\cos(\omega_0 t)\} = \frac{1}{2}[\delta(\omega-\omega_0) + \delta(\omega+\omega_0)]$"
        },
        "explanation": "Similar al seno, pero con componentes reales en lugar de imaginarias."
    },
    "7. Función sinc": {
        "function": "np.sinc(t)",
        "notation": {
            "original": r"$\mathrm{sinc}(t) = \frac{\sin(\pi t)}{\pi t}$",
            "transform": r"$\mathcal{F}\{\mathrm{sinc}(t)\} = \mathrm{rect}(\omega/2)$"
        },
        "explanation": "La transformada de la función sinc es un pulso rectangular."
    },
    "8. Pulso rectangular": {
        "function": "np.where(np.abs(t) < 1, 1, 0)",
        "notation": {
            "original": r"$\mathrm{rect}(t) = \begin{cases} 1, & |t| < \frac{1}{2} \\ 0, & \text{otherwise} \end{cases}$",
            "transform": r"$\mathcal{F}\{\mathrm{rect}(t)\} = \mathrm{sinc}(\omega/2)$"
        },
        "explanation": "La transformada del pulso rectangular es una función sinc."
    },
    "9. Función triangular": {
        "function": "np.maximum(0, 1 - np.abs(t))",
        "notation": {
            "original": r"$\Lambda(t) = \begin{cases} 1 - |t|, & |t| < 1 \\ 0, & \text{otherwise} \end{cases}$",
            "transform": r"$\mathcal{F}\{\Lambda(t)\} = \mathrm{sinc}^2(\omega/2)$"
        },
        "explanation": "La transformada de la función triangular es el cuadrado de una función sinc."
    },
    "10. Función gaussiana": {
        "function": "np.exp(-t**2)",
        "notation": {
            "original": r"$e^{-t^2}$",
            "transform": r"$\mathcal{F}\{e^{-t^2}\} = \sqrt{\pi}e^{-\omega^2/4}$"
        },
        "explanation": "La transformada de una gaussiana es otra gaussiana."
    },
    "11. Tren de deltas": {
        "function": "np.where(np.mod(t, 1) < 0.01, 1, 0)",
        "notation": {
            "original": r"$\sum_{n=-\infty}^{\infty} \delta(t-nT)$",
            "transform": r"$\mathcal{F}\{\sum_{n=-\infty}^{\infty} \delta(t-nT)\} = \frac{2\pi}{T}\sum_{k=-\infty}^{\infty} \delta(\omega-\frac{2\pi k}{T})$"
        },
        "explanation": "La transformada de un tren de deltas es otro tren de deltas en el dominio de la frecuencia."
    },
    "12. Función signo": {
        "function": "np.sign(t)",
        "notation": {
            "original": r"$\mathrm{sgn}(t)$",
            "transform": r"$\mathcal{F}\{\mathrm{sgn}(t)\} = \frac{2}{j\omega}$"
        },
        "explanation": "La transformada de la función signo es proporcional a 1/f."
    },
    "13. Función cuadrada": {
        "function": "np.sign(np.sin(2 * np.pi * t))",
        "notation": {
            "original": r"$\mathrm{sq}(t) = \mathrm{sgn}(\sin(2\pi t))$",
            "transform": r"$\mathcal{F}\{\mathrm{sq}(t)\} = \frac{4}{\pi}\sum_{n=1,3,5,\ldots}^{\infty} \frac{1}{n}[\delta(\omega-n\omega_0) - \delta(\omega+n\omega_0)]$"
        },
        "explanation": "La transformada de la onda cuadrada contiene sólo armónicos impares, decreciendo como 1/f."
    },
    "14. Función diente de sierra": {
        "function": "2 * (t/1 - np.floor(t/1 + 0.5))",
        "notation": {
            "original": r"$\mathrm{saw}(t) = 2(t/T - \lfloor t/T + 1/2 \rfloor)$",
            "transform": r"$\mathcal{F}\{\mathrm{saw}(t)\} = \frac{j}{\pi}\sum_{n=1}^{\infty} \frac{(-1)^n}{n}[\delta(\omega-n\omega_0) - \delta(\omega+n\omega_0)]$"
        },
        "explanation": "La transformada del diente de sierra contiene todos los armónicos, decreciendo como 1/f."
    },
    "15. Chirp lineal": {
        "function": "np.sin(2 * np.pi * (2 * t + 0.5 * t**2))",
        "notation": {
            "original": r"$\sin(2\pi(at + bt^2))$",
            "transform": r"No tiene una forma cerrada simple"
        },
        "explanation": "La transformada del chirp lineal muestra cómo la frecuencia aumenta con el tiempo."
    },
    "16. Modulación de amplitud": {
        "function": "(1 + 0.5 * np.sin(2 * np.pi * 0.5 * t)) * np.sin(2 * np.pi * 10 * t)",
        "notation": {
            "original": r"$(1 + m\sin(\omega_m t))\sin(\omega_c t)$",
            "transform": r"$\frac{1}{2j}[\delta(\omega-\omega_c) - \delta(\omega+\omega_c)] + \frac{m}{4j}[\delta(\omega-(\omega_c+\omega_m)) - \delta(\omega-(\omega_c-\omega_m)) - \delta(\omega+(\omega_c+\omega_m)) + \delta(\omega+(\omega_c-\omega_m))]$"
        },
        "explanation": "La transformada de la AM muestra la portadora y las bandas laterales."
    },
    "17. Función de Bessel": {
        "function": "scipy.special.jv(0, np.abs(t))",
        "notation": {
            "original": r"$J_0(|t|)$",
            "transform": r"$\mathcal{F}\{J_0(|t|)\} = \frac{2}{\sqrt{1-\omega^2}}, |\omega| < 1$"
        },
        "explanation": "La transformada de la función de Bessel de orden cero es un círculo en el dominio de la frecuencia."
    },
    "18. Función secante hiperbólica": {
        "function": "1 / np.cosh(t)",
        "notation": {
            "original": r"$\mathrm{sech}(t)$",
            "transform": r"$\mathcal{F}\{\mathrm{sech}(t)\} = \pi\mathrm{sech}(\pi\omega/2)$"
        },
        "explanation": "La transformada de la secante hiperbólica es proporcional a sí misma."
    }
}

# Poblar la lista de ejemplos
for example in examples:
    example_listbox.insert(tk.END, example)

# Inicializar con el primer ejemplo
example_listbox.selection_set(0)
on_example_select(None)

tk.mainloop()
