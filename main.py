import tkinter as tk
from tkinter import ttk, messagebox
from yt_dlp import YoutubeDL
import re  # Importar re para eliminar caracteres ANSI
import threading  # Importar threading para manejar la descarga en un hilo separado

def iniciar_descarga():
    enlace = entrada_enlace.get()
    formato = formato_var.get()
    calidad = calidad_var.get()
    
    if not enlace:
        messagebox.showerror("Error", "Por favor, introduce un enlace de Twitch.")
        return
    if not formato or not calidad:
        messagebox.showerror("Error", "Por favor, selecciona un formato y una calidad.")
        return

    # Ejecutar la descarga en un hilo separado
    hilo_descarga = threading.Thread(target=descargar_video, args=(enlace, formato, calidad))
    hilo_descarga.start()

def descargar_video(enlace, formato, calidad):
    opciones = {
        "format": "best" if calidad == "mejor" else "worst",
        "outtmpl": "%(title)s.%(ext)s",
        "progress_hooks": [actualizar_progreso],
        "postprocessors": []
    }

    if formato == "mp3":
        opciones["postprocessors"].append({
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192"
        })
    elif formato == "mp4":
        opciones["postprocessors"].append({
            "key": "FFmpegVideoConvertor",
            "preferedformat": "mp4"
        })

    try:
        barra_progreso["value"] = 0
        with YoutubeDL(opciones) as ydl:
            ydl.download([enlace])
        messagebox.showinfo("Éxito", "¡Descarga completada!")
    except Exception as e:
        messagebox.showerror("Error", f"Error al descargar: {e}")

def limpiar_ansi(texto):
    """Elimina secuencias de escape ANSI del texto"""
    return re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])', '', texto)

def actualizar_progreso(d):
    if d["status"] == "downloading":
        porcentaje = limpiar_ansi(d["_percent_str"]).strip().replace("%", "")
        try:
            # Actualiza la barra de progreso en el hilo principal
            barra_progreso["value"] = float(porcentaje)
            root.update_idletasks()  # Actualiza la interfaz
        except ValueError:
            barra_progreso["value"] = 0
    elif d["status"] == "finished":
        barra_progreso["value"] = 100

# Configuración de la ventana
root = tk.Tk()
root.title("Trollitch Downloader")
root.geometry("650x600")  # Tamaño de la ventana ajustado
root.configure(bg="#B9D6F3")  # Fondo azul claro

# Creación del estilo personalizado para ttk
style = ttk.Style()
style.configure("TRadiobutton", background="#B9D6F3", foreground="#121212", font=("Helvetica", 10))
style.configure("TButton", font=("Helvetica", 10), background="#9147FF", foreground="#FFFFFF")  # Cambiar fondo y texto del botón
style.map("TButton", background=[("active", "#B9D6F3"), ("!active", "#9147FF")], foreground=[("active", "#121212"), ("!active", "#FFFFFF")])
style.configure("TProgressbar", troughcolor="#B9D6F3", background="#00FF00", thickness=10)  # Barra de progreso en verde

# Título
titulo = tk.Label(root, text="Trollitch", font=("Helvetica", 24, "bold"), bg="#B9D6F3", fg="#9147FF")
titulo.pack(pady=10)

# Widgets
tk.Label(root, text="Introduce el enlace del directo de Twitch:", bg="#B9D6F3", fg="#121212", font=("Helvetica", 12)).pack(pady=10)
entrada_enlace = ttk.Entry(root, width=50)
entrada_enlace.pack(pady=5)

formato_var = tk.StringVar(value=None)  # Aseguramos que no haya valor seleccionado por defecto
calidad_var = tk.StringVar(value=None)  # Aseguramos que no haya valor seleccionado por defecto

ttk.Label(root, text="Formato:", background="#B9D6F3", foreground="#121212").pack(pady=5)
ttk.Radiobutton(root, text="MP4", variable=formato_var, value="mp4", style="TRadiobutton").pack()
ttk.Radiobutton(root, text="MP3", variable=formato_var, value="mp3", style="TRadiobutton").pack()

ttk.Label(root, text="Calidad:", background="#B9D6F3", foreground="#121212").pack(pady=5)
ttk.Radiobutton(root, text="Mejor", variable=calidad_var, value="mejor", style="TRadiobutton").pack()
ttk.Radiobutton(root, text="Peor", variable=calidad_var, value="peor", style="TRadiobutton").pack()

# Botón de descarga
boton_descarga = tk.Button(root, text="Descargar", command=iniciar_descarga, bg="#9147FF", fg="white", font=("Helvetica", 12), relief="flat", bd=2)
boton_descarga.pack(pady=20)
boton_descarga.config(borderwidth=1, highlightbackground="gray", highlightcolor="gray")  # Bordes redondeados

# Barra de progreso
barra_progreso = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate", style="TProgressbar")
barra_progreso.pack(pady=10)

root.mainloop()
