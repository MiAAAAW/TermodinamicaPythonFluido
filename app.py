import tkinter as tk
from tkinter import messagebox
import modules.SimFlu as SimFlu
from PIL import Image, ImageTk  # Necesario para imágenes jpg o de otros formatos

class Interfaz(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Crear el menú
        self.crear_menu()

        # Mostrar la imagen de fondo
        self.mostrar_imagen_fondo()

        # Iniciar SimFlu por defecto
        self.cambiar_a_sim_flu()

    def crear_menu(self):
        # Menú para la aplicación
        self.barra_menu = tk.Menu(self)

        # Menú de archivo con opción para salir
        menu_archivo = tk.Menu(self.barra_menu, tearoff=0)
        menu_archivo.add_command(label="Cerrar Ahora", command=self.quit)
        self.barra_menu.add_cascade(label="Salir", menu=menu_archivo)

        # Menú de ayuda
        menu_ayuda = tk.Menu(self.barra_menu, tearoff=0)
        menu_ayuda.add_command(label="Ayuda", command=self.ayuda_simflu)
        menu_ayuda.add_command(label="Acerca de", command=self.acerca_de)
        self.barra_menu.add_cascade(label="Ayuda", menu=menu_ayuda)

        self.config(menu=self.barra_menu)

    def mostrar_imagen_fondo(self):
        # Verificar la ruta de la imagen
        try:
            imagen_fondo = Image.open(r"C:\Users\INTEL\Desktop\ODIN LABORATORY\software\SimulacionFulidoIncompresible\imagex.png")  # Cambia a tu ruta correcta
        except Exception as e:
            print(f"Error al cargar la imagen: {e}")
            return
        
        # Redimensionar la imagen al tamaño de la ventana
        imagen_fondo = imagen_fondo.resize((800, 600), Image.Resampling.LANCZOS)
        self.imagen_fondo_tk = ImageTk.PhotoImage(imagen_fondo)

        # Crear un Label y poner la imagen de fondo
        fondo_label = tk.Label(self, image=self.imagen_fondo_tk)
        fondo_label.place(x=0, y=0, relwidth=1, relheight=1)  # Hacer que ocupe t
        
    def ayuda_simflu(self):
        messagebox.showinfo("Ayuda XSIMFLUD ", "Programa de simulación de fluidos-Contacta con el Desarrollador")

    def acerca_de(self):
        messagebox.showinfo("Acerca de XSIMFLUD ", "Esta aplicación fue creada para ofrecer soluciones avanzadas en la simulación de fluidos, permitiendo a los usuarios modelar y analizar el comportamiento de líquidos en diferentes condiciones. ")

    def cambiar_a_sim_flu(self):
        # Iniciar SimFlu
        print("Iniciando a XSIMFLUD ")
        self.app = SimFlu.SimFlu(self)
        self.app.run()

if __name__ == "__main__":
    interfaz = Interfaz()
