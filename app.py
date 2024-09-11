import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import modules.SimFlu as SimFlu
from tkinter import ttk  # Importar ttk para los estilos

class Interfaz(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Configurar el tamaño de la ventana
        self.geometry("800x600")

        # Configurar el estilo de ttk
        self.style = ttk.Style(self)

        # Cambiar el tema a 'clam'
        self.style.theme_use('clam')

        # Personalizar colores predominantes azules para los botones, etiquetas, y otros widgets
        self.style.configure('TButton', background='#004080', foreground='blue', font=('Arial', 12), padding=6)
        self.style.configure('TLabel', background='#0059b3', foreground='blue', font=('Arial', 12))
        self.style.configure('TEntry', foreground='#004080', fieldbackground='blue')

        # Personalizar la barra de progreso a azul oscuro
        self.style.configure('TProgressbar', troughcolor='#00FFFF', background='#FFA500')

        # Cambiar el color de fondo de la ventana principal a azul oscuro
        self.configure(bg='#003366')

        # Establecer el icono personalizado
        self.establecer_icono()

        # Crear el fondo de imagen
        self.crear_fondo()

        # Crear el menú
        self.crear_menu()

        # Crear la barra de progreso
        self.crear_barra_progreso()

        # Iniciar SimFlu por defecto
        self.cambiar_a_sim_flu()

    def establecer_icono(self):
        # Cargar la imagen del logo
        icono_path = 'C:/Users/INTEL/Desktop/ODIN LABORATORY/software/SimulacionFulidoIncompresible/logosf2.png'  # Asegúrate de que la ruta sea correcta
        if os.path.exists(icono_path):
            icono = ImageTk.PhotoImage(file=icono_path)
            # Establecer el icono de la ventana
            self.iconphoto(False, icono)
        else:
            print("No se pudo encontrar el logo en la ruta especificada.")

    def crear_fondo(self):
        # Ruta de la imagen de fondo
        ruta_imagen = "C:/Users/INTEL/Desktop/ODIN LABORATORY/software/SimulacionFulidoIncompresible/imagex.png"
        
        # Verificar si la imagen existe
        if not os.path.exists(ruta_imagen):
            print(f"El archivo {ruta_imagen} no existe. Verifica la ruta.")
            return

        try:
            # Cargar y redimensionar la imagen
            self.imagen_fondo = Image.open(ruta_imagen)
            self.imagen_fondo = self.imagen_fondo.resize((800, 600), Image.Resampling.LANCZOS)  # Ajustar al tamaño de la ventana
            self.fondo = ImageTk.PhotoImage(self.imagen_fondo)

            # Crear un label para el fondo con el fondo azul oscuro
            self.label_fondo = tk.Label(self, image=self.fondo, bg='#003366')
            self.label_fondo.place(x=0, y=0, relwidth=1, relheight=1)

            # Llevar el label de fondo al fondo
            self.label_fondo.lower()

        except Exception as e:
            print(f"Error al cargar la imagen: {e}")

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

    def crear_barra_progreso(self):
        # Crear una barra de progreso con el nuevo estilo azul oscuro
        self.progress = ttk.Progressbar(self, style='TProgressbar', orient='horizontal', length=400, mode='determinate')
        self.progress.place(x=200, y=500)
        self.progress['value'] = 50  # Establecer el valor de progreso inicial

    def ayuda_simflu(self):
        messagebox.showinfo("Ayuda XSIMFLUD", "Programa de simulación de fluidos - Contacta con el Desarrollador Miaw")

    def acerca_de(self):
        messagebox.showinfo("Acerca de XSIMFLUD", "Esta aplicación fue creada para ofrecer soluciones avanzadas en la simulación de fluidos, permitiendo a los usuarios modelar y analizar el comportamiento de líquidos en diferentes condiciones.")

    def cambiar_a_sim_flu(self):
        # Iniciar SimFlu
        print("Iniciando XSIMFLUD")
        self.app = SimFlu.SimFlu(self)
        self.app.run()

if __name__ == "__main__":
    interfaz = Interfaz()
    interfaz.mainloop()
