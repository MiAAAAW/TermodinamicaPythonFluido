import tkinter as tk
from tkinter import messagebox
import modules.SimFlu as SimFlu

class Interfaz(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Crear el menú
        self.crear_menu()

        # Iniciar SimFlu por defecto
        self.cambiar_a_sim_flu()

    def crear_menu(self):
        # Menú para la aplicación
        self.barra_menu = tk.Menu(self)

        # Menú de archivo con opción para salir
        menu_archivo = tk.Menu(self.barra_menu, tearoff=0)
        menu_archivo.add_command(label="Salir", command=self.quit)
        self.barra_menu.add_cascade(label="Archivo", menu=menu_archivo)

        # Menú de ayuda
        menu_ayuda = tk.Menu(self.barra_menu, tearoff=0)
        menu_ayuda.add_command(label="Ayuda", command=self.ayuda_simflu)
        menu_ayuda.add_command(label="Acerca de", command=self.acerca_de)
        self.barra_menu.add_cascade(label="Ayuda", menu=menu_ayuda)

        self.config(menu=self.barra_menu)

    def ayuda_simflu(self):
        messagebox.showinfo("Ayuda SimFlu", "Programa de simulación de fluidos...")

    def acerca_de(self):
        messagebox.showinfo("Acerca de", "Esta aplicación fue creada por estudiantes...")

    def cambiar_a_sim_flu(self):
        # Iniciar SimFlu
        print("Cambiando a SimFlu")
        self.app = SimFlu.SimFlu(self)
        self.app.run()

if __name__ == "__main__":
    interfaz = Interfaz()
