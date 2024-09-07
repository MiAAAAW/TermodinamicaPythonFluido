# import numpy as np
# from PIL import Image, ImageTk,ImageFilter
# from scipy.special import erf
# import datetime
# import tkinter as tk
# from tkinter import messagebox
# import tkinter.ttk as ttk
# import threading
# import random
# import time 
# from modules.SimFlu_fluid import Fluid,Fluid2

# import cv2
# from scipy.ndimage import binary_erosion
# from scipy.ndimage import gaussian_filter
# from tkinter.colorchooser import askcolor


# def rgb_to_hsv(r, g, b):
#     r, g, b = r/255.0, g/255.0, b/255.0
#     mx = max(r, g, b)
#     mn = min(r, g, b)
#     df = mx-mn
#     if mx == mn:
#         h = 0
#     elif mx == r:
#         h = (60 * ((g-b)/df) + 360) % 360
#     elif mx == g:
#         h = (60 * ((b-r)/df) + 120) % 360
#     elif mx == b:
#         h = (60 * ((r-g)/df) + 240) % 360
#     if mx == 0:
#         s = 0
#     else:
#         s = (df/mx)*100
#     v = mx*100
#     return h, s, v

# def hex_to_rgb(hex):
#     h = hex.lstrip("#")
#     return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


# class AjoutPointFrame(tk.Frame):
#     def __init__(self, master=None,SimFlu=None):
#         super().__init__(master)
#         self.master = master
#         self.pack()

#         #on va récupérer les variables de la fenêtre principale
#         self.SimFlu = SimFlu

#         self.create_widgets()
#         self._watch_variables(
#             self.slider_posx_var,
#             self.slider_posy_var,
#             self.slider_taille_var,
#             self.slider_vitesse_var,
#             self.slider_direction_var,
#             self.variable_checkbox_encre,
#             self.variable_combobox_mode
#             )
#         self._update_canvas()
    
#     def _watch_variables(self, *variables):
#         for var in variables:
#             var.trace_add("write", self._handle_trace)
    
#     def _handle_trace(self, *args):
#         print("trace", args)
#         self._update_canvas()

#     def _update_canvas(self):
#         # on va récupérer les valeurs des sliders
#         posx = int(self.slider_posx.get())
#         posy = int(self.slider_posy.get())
#         taille = int(self.slider_taille.get())
#         vitesse = int(self.slider_vitesse.get())
#         direction = int(self.slider_direction.get())/180*np.pi
#         encre = int(self.variable_checkbox_encre.get())

#         tree = self.SimFlu.tree
#         #on va créer un canvas pour afficher la position du point
#         #self.canvas = tk.Canvas(self,width=RESOLUTION[0],height=RESOLUTION[1],bg="white")
#         #self.canvas.grid(row=0,column=2,rowspan=6)
#         self.canvas.delete("all")
#         #on va créer un cercle pour afficher le point
#         self.canvas.create_oval(posx,posy,posx+taille,posy+taille,fill="black" if encre == 1 else "white")

#         #on va ajouter une flèche pour afficher la direction et la vitesse 

#         if self.variable_combobox_mode.get()=="Directionnel":
#             self.canvas.create_line(posx+taille//2,posy+taille//2,posx+taille//2+np.cos(direction)*vitesse*10,posy+taille//2+np.sin(direction)*vitesse*10,arrow=tk.LAST)
#         elif self.variable_combobox_mode.get()=="Divergent":
#             nb_fleches = 8
#             for i in range(nb_fleches):
#                 print("creation de la fleche",i)
#                 self.canvas.create_line(posx+taille//2,posy+taille//2,posx+taille//2+np.cos(i/nb_fleches*2*np.pi)*vitesse*10,posy+taille//2+np.sin(i/nb_fleches*2*np.pi)*vitesse*10,arrow=tk.LAST)
        
import numpy as np
from PIL import Image, ImageTk, ImageFilter
from scipy.special import erf
import datetime
import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
import threading
import random
import time 
from modules.SimFlu_fluid import Fluido, Fluido2

import cv2
from scipy.ndimage import binary_erosion
from scipy.ndimage import gaussian_filter
from tkinter.colorchooser import askcolor


def rgb_a_hsv(r, g, b):
    r, g, b = r/255.0, g/255.0, b/255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx - mn
    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g - b) / df) + 360) % 360
    elif mx == g:
        h = (60 * ((b - r) / df) + 120) % 360
    elif mx == b:
        h = (60 * ((r - g) / df) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = (df / mx) * 100
    # Escalar los valores para que estén entre 0 y 255
    h = np.clip(int(h / 360 * 255), 0, 255)
    s = np.clip(int(s / 100 * 255), 0, 255)
    v = np.clip(int(v / 100 * 255), 0, 255)

    return h, s, v

def hex_a_rgb(hex):
    h = hex.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


class FrameAgregarPunto(tk.Frame):
    def __init__(self, master=None, SimFlu=None):
        super().__init__(master)
        self.master = master
        self.pack()

        # vamos a recuperar las variables de la ventana principal
        self.SimFlu = SimFlu

        # Primero se crean los widgets
        

        self.crear_widgets()
        self._observar_variables(
            self.slider_posx_var,
            self.slider_posy_var,
            self.slider_tamaño_var,
            self.slider_velocidad_var,
            self.slider_direccion_var,
            self.variable_checkbox_tinta,
            self.variable_combobox_modo
            )
        self._actualizar_canvas()
    
    def _observar_variables(self, *variables):
        for var in variables:
            var.trace_add("write", self._manejar_trace)
    
    def _manejar_trace(self, *args):
        print("trace", args)
        self._actualizar_canvas()

    def _actualizar_canvas(self):
        # vamos a recuperar los valores de los sliders
        posx = int(self.slider_posx.get())
        posy = int(self.slider_posy.get())
        tamaño = int(self.slider_tamaño.get())
        velocidad = int(self.slider_velocidad.get())
        direccion = int(self.slider_direccion.get()) / 180 * np.pi
        tinta = int(self.variable_checkbox_tinta.get())

        tree = self.SimFlu.tree
        # vamos a crear un canvas para mostrar la posición del punto
        self.canvas.delete("all")
        # vamos a crear un círculo para mostrar el punto
        self.canvas.create_oval(posx, posy, posx + tamaño, posy + tamaño, fill="black" if tinta == 1 else "white")

        # vamos a añadir una flecha para mostrar la dirección y la velocidad 

        if self.variable_combobox_modo.get() == "Direccional":
            self.canvas.create_line(posx + tamaño // 2, posy + tamaño // 2, posx + tamaño // 2 + np.cos(direccion) * velocidad * 10, posy + tamaño // 2 + np.sin(direccion) * velocidad * 10, arrow=tk.LAST)
        elif self.variable_combobox_modo.get() == "Divergente":
            nb_flechas = 8
            for i in range(nb_flechas):
                print("creación de la flecha", i)
                self.canvas.create_line(posx + tamaño // 2, posy + tamaño // 2, posx + tamaño // 2 + np.cos(i / nb_flechas * 2 * np.pi) * velocidad * 10, posy + tamaño // 2 + np.sin(i / nb_flechas * 2 * np.pi) * velocidad * 10, arrow=tk.LAST)


        
    #     #on ajoute les points de départ, qui sont stockés dans tree
    #     for i in tree.get_children():
    #         posy,posx = [int(i) for i in tree.item(i)["values"][0].split(" ")]
    #         taille_point = int(tree.item(i)["values"][1])
    #         vitesse_point = int(tree.item(i)["values"][2])
    #         direction_point = int(tree.item(i)["values"][3])/180*np.pi
    #         encre = int(tree.item(i)["values"][4])
    #         mode = tree.item(i)["values"][5]
            
    #         #on va créer un cercle pour afficher le point
    #         self.canvas.create_oval(posx,posy,posx+taille_point,posy+taille_point,fill="black" if encre == 1 else "white")

    #         #on va ajouter une flèche pour afficher la direction et la vitesse
    #         print(self.variable_combobox_mode.get(),i) 
    #         if mode=="Directionnel":
    #             self.canvas.create_line(posx+taille_point//2,posy+taille_point//2,posx+taille_point//2+np.cos(direction_point)*vitesse_point*10,posy+taille_point//2+np.sin(direction_point)*vitesse_point*10,arrow=tk.LAST)
    #         elif mode=="Divergent":
    #             nb_fleches = 8
    #             for i in range(nb_fleches):
    #                 print("creation de la fleche",i)
    #                 self.canvas.create_line(posx+taille_point//2,posy+taille_point//2,posx+taille_point//2+np.cos(i/nb_fleches*2*np.pi)*vitesse_point*10,posy+taille_point//2+np.sin(i/nb_fleches*2*np.pi)*vitesse_point*10,arrow=tk.LAST)
    #             #self.canvas.create_line(posx+taille_point//2,posy+taille_point//2,posx+taille_point//2-np.cos(direction_point)*vitesse_point*10,posy+taille_point//2-np.sin(direction_point)*vitesse_point*10,arrow=tk.LAST)
    #     #si il y a des murs on les affiche 
    #     if self.SimFlu.variable_checkbox_murs.get() == 1:
    #         murs_width = 5
    #         self.canvas.create_line(0,murs_width,self.SimFlu.RESOLUTION[0],murs_width,fill="black",width=murs_width)
    #         self.canvas.create_line(murs_width,0,murs_width,self.SimFlu.RESOLUTION[1],fill="black",width=murs_width)
    #         self.canvas.create_line(self.SimFlu.RESOLUTION[0],0,self.SimFlu.RESOLUTION[0],self.SimFlu.RESOLUTION[1],fill="black",width=murs_width)
    #         self.canvas.create_line(0,self.SimFlu.RESOLUTION[1],self.SimFlu.RESOLUTION[0],self.SimFlu.RESOLUTION[1],fill="black",width=murs_width)
    #     self.canvas.update()

    
    # def create_widgets(self):
    #     #on va ajouter un canvas pour afficher la position du point
    #     self.canvas = tk.Canvas(self,width=self.SimFlu.RESOLUTION[0],height=self.SimFlu.RESOLUTION[1],bg="grey")
    #     self.canvas.grid(row=0,column=2,rowspan=6)


    #     # on va rendre tout ça plus joli, avec des grid 
    #     #on va donner des noms aux sliders, pour pouvoir récupérer leurs valeurs
    #     # on va ajouter deux labels pour la position
    #     label = tk.Label(self,text="x:")
    #     label.grid(row=0,column=0)

    #     label = tk.Label(self,text="y:")
    #     label.grid(row=1,column=0)

    #     # on va ajouter deux sliders pour la position

    #     self.slider_posx_var = tk.IntVar()
    #     self.slider_posx = tk.Scale(self, from_=0, to=self.SimFlu.RESOLUTION[0], orient=tk.HORIZONTAL,variable=self.slider_posx_var)
    #     self.slider_posx.set(self.SimFlu.RESOLUTION[0]//2)
    #     self.slider_posx.grid(row=0,column=1)

    #     self.slider_posy_var = tk.IntVar()
    #     self.slider_posy = tk.Scale(self, from_=0, to=self.SimFlu.RESOLUTION[1],orient=tk.HORIZONTAL,variable=self.slider_posy_var)
    #     self.slider_posy.set(self.SimFlu.RESOLUTION[1]//2)
    #     self.slider_posy.grid(row=1,column=1)

    #     # on va ajouter un label pour la taille
    #     label = tk.Label(self,text="Taille")
    #     label.grid(row=2,column=0)
    #     # on va ajouter un slider pour la taille
    #     self.slider_taille_var = tk.IntVar()
    #     self.slider_taille = tk.Scale(self, from_=3, to=20, orient=tk.HORIZONTAL,variable=self.slider_taille_var)
    #     self.slider_taille_var.set(10)
    #     self.slider_taille.grid(row=2,column=1)

    #     # on va ajouter un label pour la vitesse
    #     label = tk.Label(self,text="Vitesse")
    #     label.grid(row=3,column=0)
    #     # on va ajouter un slider pour la vitesse
    #     self.slider_vitesse_var = tk.IntVar()
    #     self.slider_vitesse_var.set(1)
    #     self.slider_vitesse = tk.Scale(self, from_=0, to=6, orient=tk.HORIZONTAL,variable=self.slider_vitesse_var)
    #     self.slider_vitesse.grid(row=3,column=1)
        


    #     # on va ajouter un label pour la direction
    #     label = tk.Label(self,text="Direction")
    #     label.grid(row=4,column=0)
    #     # on va ajouter un slider pour la direction
    #     self.slider_direction_var = tk.IntVar()
    #     self.slider_direction = tk.Scale(self, from_=0, to=360, orient=tk.HORIZONTAL,variable=self.slider_direction_var)
    #     self.slider_direction.grid(row=4,column=1)


    #     #on va créer une checkbox pour l'encre 
    #     self.variable_checkbox_encre = tk.IntVar()
    #     checkbox_encre = tk.Checkbutton(self,text="Encre",variable=self.variable_checkbox_encre)
    #     self.variable_checkbox_encre.set(1)
    #     checkbox_encre.grid(row=5,column=0)

    #     #on va créer une combobox pour le mode
    #     self.variable_combobox_mode = tk.StringVar()
    #     combobox_mode = ttk.Combobox(self,textvariable=self.variable_combobox_mode)
    #     combobox_mode['values'] = ('Directionnel',"Divergent")
    #     combobox_mode.current(0)
    #     combobox_mode.grid(row=5,column=1)

    #     #On va mettre les prochains paramètres dans un autre frame
    #     frame = tk.Frame(self,bg="grey")
    #     frame.grid(row=6,column=0,columnspan=2)

    #     #On va ajouter un Slider pour le nombre de points aléatoires
    #     label = tk.Label(frame,text="Nombre de points aléatoires",bg="grey")
    #     label.pack(side=tk.LEFT)
    #     self.slider_nb_points = tk.Scale(frame, from_=1, to=20, orient=tk.HORIZONTAL,bg="grey")
    #     self.slider_nb_points.pack(side=tk.LEFT)

    #     # on va ajouter un bouton pour créer des points aléatoires
    #     button = tk.Button(frame,text="Créer les points aléatoires",command=self.creer_points_aleatoires,bg="grey")
    #     button.pack(side=tk.RIGHT)

    #     # on va ajouter un bouton pour valider
    #     button = tk.Button(self,text="Valider",command=self.valider_point)
    #     button.grid(row=7,column=0)
    #     # on va ajouter un bouton pour annuler
    #     button = tk.Button(self,text="Quitter",command=self.master.destroy)
    #     button.grid(row=7,column=1)

    #     #on va ajouter un bouton pour modifier les paramètres avec du code
    #     button = tk.Button(self,text="Modifier les paramètres avec du code",command=self.secret_bouton)
    #     button.grid(row=8,column=0,columnspan=2)

    # def secret_bouton(self):
    #     self.top = tk.Toplevel(self.master)
    #     self.top.resizable(False,False)
    #     self.top.title("Modifier les paramètres avec du code")
    #     #il n'y a qu'une seule entry, et un bouton pour valider
    #     frame = tk.Frame(self.top)
    #     frame.pack()
    #     self.entry_code = tk.Text(frame)
    #     self.entry_code.insert(tk.INSERT,self.SimFlu.get_secret_buffer())
    #     self.entry_code.grid(row=0,column=1,padx=5,pady=5,ipadx=80,ipady=60)
    #     button = tk.Button(frame,text="Valider",command=self.valider_code)
    #     button.grid(row=1,column=0,columnspan=2)

    # def valider_code(self):
    #     text =self.entry_code.get("1.0",tk.END)
    #     exec_namespace = {}
    #     exec(text,exec_namespace)
    #     #print(points)
        
    #     points = exec_namespace["points"]
    #     print(points)
    #     #on va ajouter les points à la liste
    #     for point in points:
    #         self.SimFlu.tree.insert('', tk.END, values=(point[0],point[1],point[2],point[3],point[4],point[5]))
    #     self.top.destroy()
    #     self._update_canvas()

             # se añaden los puntos de inicio, que están almacenados en tree
        for i in tree.get_children():
            posy, posx = [int(i) for i in tree.item(i)["values"][0].split(" ")]
            tamaño_punto = int(tree.item(i)["values"][1])
            velocidad_punto = int(tree.item(i)["values"][2])
            direccion_punto = int(tree.item(i)["values"][3]) / 180 * np.pi
            tinta = int(tree.item(i)["values"][4])
            modo = tree.item(i)["values"][5]
            
            # se crea un círculo para mostrar el punto
            self.canvas.create_oval(posx, posy, posx + tamaño_punto, posy + tamaño_punto, fill="black" if tinta == 1 else "white")

            # se añade una flecha para mostrar la dirección y la velocidad
            print(self.variable_combobox_modo.get(), i) 
            if modo == "Direccional":
                self.canvas.create_line(posx + tamaño_punto // 2, posy + tamaño_punto // 2, posx + tamaño_punto // 2 + np.cos(direccion_punto) * velocidad_punto * 10, posy + tamaño_punto // 2 + np.sin(direccion_punto) * velocidad_punto * 10, arrow=tk.LAST)
            elif modo == "Divergente":
                nb_flechas = 8
                for i in range(nb_flechas):
                    print("creación de la flecha", i)
                    self.canvas.create_line(posx + tamaño_punto // 2, posy + tamaño_punto // 2, posx + tamaño_punto // 2 + np.cos(i / nb_flechas * 2 * np.pi) * velocidad_punto * 10, posy + tamaño_punto // 2 + np.sin(i / nb_flechas * 2 * np.pi) * velocidad_punto * 10, arrow=tk.LAST)
                #self.canvas.create_line(posx + tamaño_punto // 2, posy + tamaño_punto // 2, posx + tamaño_punto // 2 - np.cos(direccion_punto) * velocidad_punto * 10, posy + tamaño_punto // 2 - np.sin(direccion_punto) * velocidad_punto * 10, arrow=tk.LAST)
        # si hay muros, se muestran 
        if self.SimFlu.variable_checkbox_muros.get() == 1:
            grosor_muros = 5
            self.canvas.create_line(0, grosor_muros, self.SimFlu.RESOLUTION[0], grosor_muros, fill="black", width=grosor_muros)
            self.canvas.create_line(grosor_muros, 0, grosor_muros, self.SimFlu.RESOLUTION[1], fill="black", width=grosor_muros)
            self.canvas.create_line(self.SimFlu.RESOLUTION[0], 0, self.SimFlu.RESOLUTION[0], self.SimFlu.RESOLUTION[1], fill="black", width=grosor_muros)
            self.canvas.create_line(0, self.SimFlu.RESOLUTION[1], self.SimFlu.RESOLUTION[0], self.SimFlu.RESOLUTION[1], fill="black", width=grosor_muros)
        self.canvas.update()

    
    def crear_widgets(self):
        # se añadirá un canvas para mostrar la posición del punto
        self.canvas = tk.Canvas(self, width=self.SimFlu.RESOLUTION[0], height=self.SimFlu.RESOLUTION[1], bg="grey")
        self.canvas.grid(row=0, column=2, rowspan=6)


        # se va a organizar mejor, usando grid 
        # se asignarán nombres a los sliders, para poder recuperar sus valores
        # se añaden dos etiquetas para la posición
        label = tk.Label(self, text="x:")
        label.grid(row=0, column=0)

        label = tk.Label(self, text="y:")
        label.grid(row=1, column=0)

        # se añaden dos sliders para la posición

        self.slider_posx_var = tk.IntVar()
        self.slider_posx = tk.Scale(self, from_=0, to=self.SimFlu.RESOLUTION[0], orient=tk.HORIZONTAL, variable=self.slider_posx_var)
        self.slider_posx.set(self.SimFlu.RESOLUTION[0] // 2)
        self.slider_posx.grid(row=0, column=1)

        self.slider_posy_var = tk.IntVar()
        self.slider_posy = tk.Scale(self, from_=0, to=self.SimFlu.RESOLUTION[1], orient=tk.HORIZONTAL, variable=self.slider_posy_var)
        self.slider_posy.set(self.SimFlu.RESOLUTION[1] // 2)
        self.slider_posy.grid(row=1, column=1)

        # se añade una etiqueta para el tamaño
        label = tk.Label(self, text="Tamaño")
        label.grid(row=2, column=0)
        # se añade un slider para el tamaño
        self.slider_tamaño_var = tk.IntVar()
        self.slider_tamaño = tk.Scale(self, from_=3, to=20, orient=tk.HORIZONTAL, variable=self.slider_tamaño_var)
        self.slider_tamaño_var.set(10)
        self.slider_tamaño.grid(row=2, column=1)

        # se añade una etiqueta para la velocidad
        label = tk.Label(self, text="Velocidad")
        label.grid(row=3, column=0)
        # se añade un slider para la velocidad
        self.slider_velocidad_var = tk.IntVar()
        self.slider_velocidad_var.set(1)
        self.slider_velocidad = tk.Scale(self, from_=0, to=6, orient=tk.HORIZONTAL, variable=self.slider_velocidad_var)
        self.slider_velocidad.grid(row=3, column=1)
        


        # se añade una etiqueta para la dirección
        label = tk.Label(self, text="Dirección")
        label.grid(row=4, column=0)
        # se añade un slider para la dirección
        self.slider_direccion_var = tk.IntVar()
        self.slider_direccion = tk.Scale(self, from_=0, to=360, orient=tk.HORIZONTAL, variable=self.slider_direccion_var)
        self.slider_direccion.grid(row=4, column=1)


        # se crea un checkbox para la tinta 
        self.variable_checkbox_tinta = tk.IntVar()
        checkbox_tinta = tk.Checkbutton(self, text="Tinta", variable=self.variable_checkbox_tinta)
        self.variable_checkbox_tinta.set(1)
        checkbox_tinta.grid(row=5, column=0)

        # se crea un combobox para el modo
        self.variable_combobox_modo = tk.StringVar()
        combobox_modo = ttk.Combobox(self, textvariable=self.variable_combobox_modo)
        combobox_modo['values'] = ('Direccional', "Divergente")
        combobox_modo.current(0)
        combobox_modo.grid(row=5, column=1)

        # se colocarán los próximos parámetros en otro frame
        frame = tk.Frame(self, bg="grey")
        frame.grid(row=6, column=0, columnspan=2)

        # se añade un slider para el número de puntos aleatorios
        label = tk.Label(frame, text="Número de puntos aleatorios", bg="grey")
        label.pack(side=tk.LEFT)
        self.slider_nb_puntos = tk.Scale(frame, from_=1, to=20, orient=tk.HORIZONTAL, bg="grey")
        self.slider_nb_puntos.pack(side=tk.LEFT)

        # se añade un botón para crear puntos aleatorios
        button = tk.Button(frame, text="Crear puntos aleatorios", command=self.crear_puntos_aleatorios, bg="grey")
        button.pack(side=tk.RIGHT)

        # se añade un botón para validar
        button = tk.Button(self, text="Validar", command=self.validar_punto)
        button.grid(row=7, column=0)
        # se añade un botón para salir
        button = tk.Button(self, text="Salir", command=self.master.destroy)
        button.grid(row=7, column=1)

        # se añade un botón para modificar los parámetros con código
        button = tk.Button(self, text="Modificar parámetros con código", command=self.boton_secreto)
        button.grid(row=8, column=0, columnspan=2)

    def boton_secreto(self):
        self.top = tk.Toplevel(self.master)
        self.top.resizable(False, False)
        self.top.title("Modificar parámetros con código")
        # solo hay una entrada de texto y un botón para validar
        frame = tk.Frame(self.top)
        frame.pack()
        self.entrada_codigo = tk.Text(frame)
        self.entrada_codigo.insert(tk.INSERT, self.SimFlu.get_secret_buffer())
        self.entrada_codigo.grid(row=0, column=1, padx=5, pady=5, ipadx=80, ipady=60)
        button = tk.Button(frame, text="Validar", command=self.validar_codigo)
        button.grid(row=1, column=0, columnspan=2)

    def validar_codigo(self):
        texto = self.entrada_codigo.get("1.0", tk.END)
        espacio_ejecucion = {}
        exec(texto, espacio_ejecucion)
        
        puntos = espacio_ejecucion["puntos"]
        print(puntos)
        # se añaden los puntos a la lista
        for punto in puntos:
            self.SimFlu.tree.insert('', tk.END, values=(punto[0], punto[1], punto[2], punto[3], punto[4], punto[5]))
        self.top.destroy()
        self._actualizar_canvas()
   






#     def valider_point(self):
#         posx = int(self.slider_posx.get())
#         posy = int(self.slider_posy.get())
#         taille = int(self.slider_taille.get())
#         vitesse = int(self.slider_vitesse.get())
#         direction = int(self.slider_direction.get())
#         encre = int(self.variable_checkbox_encre.get())
#         mode = self.variable_combobox_mode.get()

#         self.SimFlu.tree.insert('', tk.END, values=((posy,posx),taille,vitesse,direction,encre,mode))
#         #self.master.destroy()
    
#     def creer_points_aleatoires(self):
#         nb_points = int(self.slider_nb_points.get())
#         for i in range(nb_points):
#             posx = np.random.randint(0,self.SimFlu.RESOLUTION[0])
#             posy = np.random.randint(0,self.SimFlu.RESOLUTION[1])
#             taille = np.random.randint(3,20)
#             vitesse = np.random.randint(1,5)
#             direction = np.random.randint(0,360)
#             encre = np.random.randint(0,2)
#             mode = random.choice(['Directionnel',"Divergent"])
#             self.SimFlu.tree.insert('', tk.END, values=((posx,posy),taille,vitesse,direction,encre,mode))
#         self._update_canvas()
#         #newWindow.destroy()


# #Classe principale de cette simulation 
# class SimFlu():
#     def __init__(self,master) -> None:
#         #On commence par définir les paramètres de la simulation ainsi que les constantes
#         self.RESOLUTION = 200, 200
#         self.SCALE = 3

#         #taille du canvas des paramètres
#         self.parameter_size = 350
#         self.SIMULATION_SPEED_MAX = 10
#         self.SIMULATION_SPEED_MIN = 1
#         self.NOM_APPLI = "SimFlu"

#         self.colors = [None,'#8b32a8n',None]

#         #on va créer une liste qui va contenir les frames
#         self.frames = []

#         self.setup_window(master)
#         self.create_widgets()

#     def setup_window(self,master):
#         self.root = master#tk.Tk(master)
#         self.root.title(self.NOM_APPLI)
#         self.root.geometry(f"{self.RESOLUTION[0]*self.SCALE+self.parameter_size}x{self.RESOLUTION[1]*self.SCALE}")
#         self.root.configure(bg="black")
#         self.root.resizable(True,True)

#     def create_widgets(self):
#         #on va créer les widgets 
#         self.create_simulation_window()
#         self.create_parameter_window()
    
#     def create_simulation_window(self):
#         #On va créer un canvas qui va contenir la simulation
#         self.simulation_window = tk.Frame(self.root, bg="black",width=self.RESOLUTION[0]*self.SCALE, height=self.RESOLUTION[1]*self.SCALE)
#         self.root.grid_rowconfigure(0, weight=1)
#         self.root.grid_columnconfigure(0, weight=1)
#         self.simulation_window.grid(row=0,column=0,sticky="nsew")
#         self.my_label = tk.Label(self.simulation_window,bg="black")
#         self.my_label.pack()

#     def create_parameter_window(self):
#         #On va créer un canvas qui va contenir les paramètres
#         self.canvas_param = tk.Canvas(self.root,width=self.parameter_size,height=self.RESOLUTION[1]*self.SCALE,bg="white")
#         self.canvas_param.grid(row=0,column=1,sticky="nsew")

#         #on va ajouter un label pour les paramètres
#         self.label_param = tk.Label(self.canvas_param,text="Paramètres",bg="white")
#         self.label_param.grid(row=0,column=0)

#         #on va créer un treeview pour recenser les points de départ
#         self.colonnes = ("Position","Taille","Vitesse","Direction","Encre","Directionnel")
#         self.tree = ttk.Treeview(self.canvas_param,column=self.colonnes,show="headings")
#         for i in range(len(self.colonnes)):
#             self.tree.heading(i,text=self.colonnes[i])
#             self.tree.column(i,minwidth=65,width=65)
#         self.tree.grid(row=1,column=0,columnspan=2)

#         #On va ajouter un bouton pour ajouter un point
#         self.button_modifier = tk.Button(self.canvas_param,text="Modifier les paramètres",command=self.modifier_parametres)
#         self.button_modifier.grid(row=2,column=0)

#         #On va ajouter un bouton pour supprimer un point
#         self.button_supprimer = tk.Button(self.canvas_param,text="Supprimer",command=self.supprimer_source)
#         self.button_supprimer.grid(row=2,column=1)

#         #On va créer un slider pour la durée de la simulation
#         self.label = tk.Label(self.canvas_param,text="Durée de la simulation")
#         self.label.grid(row=3,column=0)
#         self.slider_duree = tk.Scale(self.canvas_param, from_=10, to=400, orient=tk.HORIZONTAL)
#         self.slider_duree.set(50)
#         self.slider_duree.grid(row=3,column=1)


    def validar_punto(self):
        posx = int(self.slider_posx.get())
        posy = int(self.slider_posy.get())
        tamaño = int(self.slider_tamaño.get())
        velocidad = int(self.slider_velocidad.get())
        dirección = int(self.slider_direccion.get())
        tinta = int(self.variable_checkbox_tinta.get())
        modo = self.variable_combobox_modo.get()

        self.SimFlu.tree.insert('', tk.END, values=((posy, posx), tamaño, velocidad, dirección, tinta, modo))
        #self.master.destroy()
    
    def crear_puntos_aleatorios(self):
        nb_puntos = int(self.slider_nb_puntos.get())
        for i in range(nb_puntos):
            posx = np.random.randint(0, self.SimFlu.RESOLUTION[0])
            posy = np.random.randint(0, self.SimFlu.RESOLUTION[1])
            tamaño = np.random.randint(3, 20)
            velocidad = np.random.randint(1, 5)
            dirección = np.random.randint(0, 360)
            tinta = np.random.randint(0, 2)
            modo = random.choice(['Direccional', "Divergente"])
            self.SimFlu.tree.insert('', tk.END, values=((posx, posy), tamaño, velocidad, dirección, tinta, modo))
        self._actualizar_canvas()
        #newWindow.destroy()


# Clase principal de esta simulación 
class SimFlu():
    def __init__(self, master) -> None:
        # Se comienzan definiendo los parámetros de la simulación, así como las constantes
        self.RESOLUTION = 200, 200
        self.ESCALA = 3

        # tamaño del canvas de los parámetros
        self.tamaño_parametro = 350
        self.VELOCIDAD_SIMULACION_MAX = 10
        self.VELOCIDAD_SIMULACION_MIN = 1
        self.NOMBRE_APLICACION = "Simulador de Fluidos"

        self.colores = [None, '#8b32a8n', None]

        # se crea una lista que contendrá los frames
        self.frames = []

        self.configurar_ventana(master)
        self.crear_widgets()

    def configurar_ventana(self, master):
        self.root = master  # tk.Tk(master)
        self.root.title(self.NOMBRE_APLICACION)
        self.root.geometry(f"{self.RESOLUTION[0]*self.ESCALA+self.tamaño_parametro}x{self.RESOLUTION[1]*self.ESCALA}")
        self.root.configure(bg="black")
        self.root.resizable(True, True)

    def crear_widgets(self):
        # se crean los widgets 
        self.crear_ventana_simulacion()
        self.crear_ventana_parametro()
    
    def crear_ventana_simulacion(self):
        # Se crea un canvas que contendrá la simulación
        self.ventana_simulacion = tk.Frame(self.root, bg="black", width=self.RESOLUTION[0]*self.ESCALA, height=self.RESOLUTION[1]*self.ESCALA)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.ventana_simulacion.grid(row=0, column=0, sticky="nsew")
        self.mi_label = tk.Label(self.ventana_simulacion, bg="black")
        self.mi_label.pack()

    def crear_ventana_parametro(self):
        # Se crea un canvas que contendrá los parámetros
        self.canvas_parametro = tk.Canvas(self.root, width=self.tamaño_parametro, height=self.RESOLUTION[1]*self.ESCALA, bg="white")
        self.canvas_parametro.grid(row=0, column=1, sticky="nsew")

        # se añade una etiqueta para los parámetros
        self.label_parametro = tk.Label(self.canvas_parametro, text="Parámetros", bg="white")
        self.label_parametro.grid(row=0, column=0)

        # se crea un treeview para registrar los puntos de inicio
        self.columnas = ("Posición", "Tamaño", "Velocidad", "Dirección", "Tinta", "Direccional")
        self.tree = ttk.Treeview(self.canvas_parametro, column=self.columnas, show="headings")
        for i in range(len(self.columnas)):
            self.tree.heading(i, text=self.columnas[i])
            self.tree.column(i, minwidth=65, width=65)
        self.tree.grid(row=1, column=0, columnspan=2)

        # Se añade un botón para modificar un punto
        self.boton_modificar = tk.Button(self.canvas_parametro, text="Modificar los parámetros", command=self.modificar_parametros)
        self.boton_modificar.grid(row=2, column=0)

        # Se añade un botón para eliminar un punto
        self.boton_eliminar = tk.Button(self.canvas_parametro, text="Eliminar", command=self.eliminar_fuente)
        self.boton_eliminar.grid(row=2, column=1)

        # Se crea un slider para la duración de la simulación
        self.etiqueta = tk.Label(self.canvas_parametro, text="Duración de la simulación")
        self.etiqueta.grid(row=3, column=0)
        self.slider_duracion = tk.Scale(self.canvas_parametro, from_=10, to=400, orient=tk.HORIZONTAL)
        self.slider_duracion.set(50)
        self.slider_duracion.grid(row=3, column=1)

        # vamos a añadir un checkbox para saber si el usuario quiere estar en modo interactivo
        self.variable_checkbox_interactivo = tk.IntVar()
        self.checkbox_interactivo = tk.Checkbutton(self.canvas_parametro, text="Modo interactivo", variable=self.variable_checkbox_interactivo)
        self.checkbox_interactivo.grid(row=5, column=0)

        # se añade una etiqueta para la velocidad de la simulación
        self.label = tk.Label(self.canvas_parametro, text="Velocidad de la simulación")
        self.label.grid(row=6, column=0)
        # se añade un slider para la velocidad de la simulación

        self.slider_velocidad_sim = tk.Scale(self.canvas_parametro, from_=self.VELOCIDAD_SIMULACION_MIN, to=self.VELOCIDAD_SIMULACION_MAX, orient=tk.HORIZONTAL)
        self.slider_velocidad_sim.set(10)
        self.slider_velocidad_sim.grid(row=6, column=1)

        # se añade un checkbox para saber si el usuario quiere mostrar los muros
        self.variable_checkbox_muros = tk.IntVar()
        self.checkbox_muros = tk.Checkbutton(self.canvas_parametro, text="Mostrar muros", variable=self.variable_checkbox_muros)
        self.checkbox_muros.grid(row=7, column=0)

        # se añade un parámetro (slider) para controlar el aspecto del humo
        self.label = tk.Label(self.canvas_parametro, text="Aspecto del humo")
        self.label.grid(row=8, column=0)
        self.slider_aspecto_humo = tk.Scale(self.canvas_parametro, from_=0, to=7, orient=tk.HORIZONTAL)
        self.slider_aspecto_humo.set(1)
        self.slider_aspecto_humo.grid(row=8, column=1)

        # se añade un checkbox para saber si el usuario quiere mostrar el brillo (glow)
        self.variable_checkbox_glow = tk.IntVar()
        self.checkbox_glow = tk.Checkbutton(self.canvas_parametro, text="Brillo", variable=self.variable_checkbox_glow)
        self.checkbox_glow.grid(row=9, column=0)

        # se añade un checkbox para saber si el usuario quiere elegir un color
        self.variable_checkbox_elegir_color = tk.IntVar()
        self.checkbox_elegir_color = tk.Checkbutton(self.canvas_parametro, text="Elegir color", variable=self.variable_checkbox_elegir_color)
        self.checkbox_elegir_color.grid(row=10, column=0)

        # si la persona elige seleccionar un color, también queremos permitir la elección de color
        self.boton_elegir_color = tk.Button(self.canvas_parametro, text="Color", command=self.elegir_color)
        self.boton_elegir_color.grid(row=10, column=1)

        # se crea un botón para iniciar la simulación
        self.boton_iniciar = tk.Button(self.canvas_parametro, text="Iniciar la simulación", command=self.iniciar_simulacion)
        self.boton_iniciar.grid(row=11, column=0)

        # se crea un botón para guardar la simulación
        self.boton_guardar = tk.Button(self.canvas_parametro, text="Guardar", command=self.guardar_simulacion)
        self.boton_guardar.grid(row=11, column=1)

        # se crea una barra de progreso
        self.barra_progreso = ttk.Progressbar(self.canvas_parametro, orient=tk.HORIZONTAL, length=200, mode='determinate')
        self.barra_progreso.grid(row=12, column=0, columnspan=2)

    def elegir_color(self):
        self.colores = askcolor(title="Elige un color para la animación")

    def iniciar_simulacion(self):
        # se desactiva el botón de inicio
        self.boton_iniciar.configure(state="disabled")
        self.boton_guardar.configure(state="disabled")

        # se recuperan los puntos de inicio
        puntos = []

        # se añaden los puntos de inicio almacenados en tree
        for i in self.tree.get_children():
            puntos.append(self.tree.item(i)["values"])

        # se crea el fluido 
        fluido = Fluido(self.RESOLUTION, 'tinte')
        entrada_tinte = np.zeros(fluido.shape)
        entrada_velocidad = np.zeros_like(fluido.velocidad)

        for punto in puntos:
            posx, posy = [int(i) for i in punto[0].split(" ")]
            tamaño_punto = int(punto[1])
            velocidad_punto = int(punto[2])
            direccion_punto = int(punto[3]) / 180 * np.pi
            punto_arr = np.array([posx + tamaño_punto // 2, posy + tamaño_punto // 2])
            mascara = np.linalg.norm(fluido.indices - punto_arr[:, None, None], axis=0) <= tamaño_punto
            if punto[5] == "Direccional":
                entrada_velocidad[:, mascara] += np.array([np.sin(direccion_punto), np.cos(direccion_punto)])[:, None] * velocidad_punto
            elif punto[5] == "Divergente":
                x0 = posx + tamaño_punto // 2
                y0 = posy + tamaño_punto // 2
                f = lambda x, y: np.array([2 * (x - x0), 2 * (y - y0)])
                arr = np.zeros_like(entrada_velocidad)
                for i in range(fluido.shape[0]):
                    for j in range(fluido.shape[1]):
                        if mascara[i, j]:
                            vec = f(i, j)
                            norm = np.linalg.norm(vec)
                            arr[:, i, j] = vec / (norm if norm != 0 else 1)
                entrada_velocidad += arr * velocidad_punto
            if punto[4]:
                entrada_tinte[mascara] = 1

        # Ahora que todo está bien inicializado, se inicia la simulación
        self.frames = []
        duracion = int(self.slider_duracion.get())

        color_params = np.array([0, 1, 255])

        # se define una función para mostrar las imágenes
        def mostrar_imagen(i):
            try:
                img = ImageTk.PhotoImage(self.frames[i])
                self.mi_label.img = img
                self.mi_label.configure(image=img)
                self.mi_label.after(self.SIMULATION_SPEED_MAX + 1 - int(self.slider_velocidad_sim.get()), mostrar_imagen, (i + 1) % len(self.frames))
            except:
                if self.variable_checkbox_interactivo.get() == 1:
                    time.sleep(0.1)
                    if len(self.frames) > 0:
                        self.mi_label.after(10, mostrar_imagen, i % len(self.frames))
                    else:
                        self.mi_label.after(10, mostrar_imagen, i)

        # Si estamos en modo interactivo, se muestra la simulación a medida que se calcula
        if self.variable_checkbox_interactivo.get() == 1:
            mostrar_imagen(1)
        self.checkbox_interactivo.configure(state="disabled")

        for f in range(duracion):
            print(f'Calculando frame {f + 1} de {duracion}.')

            if f <= duracion:
                fluido.velocidad += entrada_velocidad
                fluido.tinte += entrada_tinte

            divergencia, remolino, presion = fluido.paso(boundary=None, paredes=self.variable_checkbox_muros.get() == 1)

            remolino = (erf(remolino * 7) + 1) / 8

            color = np.dstack((remolino, np.ones(fluido.shape), fluido.tinte))
            color = (np.clip(color, color_params[0], color_params[1]) * color_params[2]).astype('uint8')
            if int(self.variable_checkbox_elegir_color.get()) == 1:
                color[:, :, 0][color[:, :, 0] > 1] = rgb_a_hsv(*hex_a_rgb(self.colores[1]))[0]
            imagen = Image.fromarray(color, mode='HSV').convert('RGB')
            
            if int(self.variable_checkbox_glow.get()) == 1:
                imagen = imagen.filter(ImageFilter.GaussianBlur(radius=1))
                bordes = imagen.filter(ImageFilter.FIND_EDGES)
                imagen = np.array(imagen)
                bordes = np.array(bordes)
                desenfoque = np.clip(gaussian_filter(bordes, sigma=7), 0, 255).astype('uint8')
                intensidad_desenfoque = 3
                brillo = imagen + desenfoque * intensidad_desenfoque
                brillo = brillo.astype(float)
                brillo *= (255 / brillo.max())
                imagen = Image.fromarray(brillo.astype("uint8"))

            imagen = imagen.resize((self.RESOLUTION[0] * self.ESCALA, self.RESOLUTION[1] * self.ESCALA))
            imagen = imagen.filter(ImageFilter.GaussianBlur(radius=int(self.slider_aspecto_humo.get())))
            self.frames.append(imagen)
            self.barra_progreso['value'] = f / duracion * 100
            self.root.update()

        # se reactiva el botón de inicio
        self.boton_iniciar.configure(state="normal")
        self.boton_guardar.configure(state="normal")

        if self.variable_checkbox_interactivo.get() == 0:
            print("mostrando simulación")
            mostrar_imagen(1)
        self.checkbox_interactivo.configure(state="normal")                

    def eliminar_fuente(self):
        elementos_seleccionados = self.tree.selection()    
    
        for elemento_seleccionado in elementos_seleccionados:
            self.tree.delete(elemento_seleccionado)

        if hasattr(self, "ajoutFrame"):
            self.ajoutFrame._actualizar_canvas()

    def modificar_parametros(self):
        self.top = tk.Toplevel(self.root)
        self.top.title("Modificar parámetros")
        self.ajoutFrame = FrameAgregarPunto(master=self.top, SimFlu=self)

    def guardar_simulacion(self):
        try:
            self.frames[0].save(f'ejemplo-{datetime.datetime.now()}.gif', save_all=True, append_images=self.frames[1:], duration=20, loop=0)
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar la simulación: {e}")

    def run(self):
        self.root.mainloop()

    def get_secret_buffer(self):
        buffer_secreto = f'''
    # Puedes modificar los parámetros con código
    # Para ello, deberás especificar la siguiente variable:
    # puntos: lista de los puntos de inicio
    # Cada punto es una lista de 6 elementos:
    #  - posición: tupla (x, y)
    #  - tamaño: int
    #  - velocidad: int
    #  - dirección: int
    #  - tinta: int
    #  - modo: str

    import numpy as np
    RESOLUTION = {self.RESOLUTION}
    puntos = []

    tinta = 1 # 1 si se quiere que el punto deje una traza, 0 si no
    modo = "Direccional" # Direccional o Divergente
    velocidad = 1
    tamaño = 7

    # Ejemplo 1:
    puntos = []
    puntos = [[(RESOLUTION[0] // 2, RESOLUTION[1] // 2), tamaño, velocidad, 0, tinta, modo]]
    puntos.append([(RESOLUTION[0] // 2 - tamaño, RESOLUTION[1] // 2), tamaño, velocidad, 180, tinta, modo])


    # Ejemplo 2 (círculo):
    puntos = []

    nb_puntos = 10
    centro = np.floor_divide(RESOLUTION, 2)
    radio = np.min(centro) - 60

    posiciones = np.linspace(-np.pi, np.pi, nb_puntos, endpoint=False)
    posiciones = tuple(np.array((np.cos(p), np.sin(p))) for p in posiciones)
    normales = tuple(-p for p in posiciones)
    posiciones = tuple(radio * p + centro for p in posiciones)

    print(posiciones)
    for i, pos in enumerate(posiciones):
        dirección = (i + 2) * 360 / nb_puntos 
        puntos.append([(int(pos[0]), int(pos[1])), int(tamaño), int(velocidad), int(dirección), tinta, modo])

    '''
        return buffer_secreto

    
      



#         #on va ajouter une checkbox pour savoir si l'utilisateur veut être en mode interactif
#         self.variable_checkbox_interactif = tk.IntVar()
#         self.checkbox_interactif = tk.Checkbutton(self.canvas_param,text="Mode interactif",variable=self.variable_checkbox_interactif)
#         self.checkbox_interactif.grid(row=5,column=0)

#         #on ajoute un label pour la vitesse de la simulation
#         self.label = tk.Label(self.canvas_param,text="Vitesse de la simulation")
#         self.label.grid(row=6,column=0)
#         #on ajoute un slider pour la vitesse de la simulation
#         self.slider_vitesse_sim = tk.Scale(self.canvas_param, from_=self.SIMULATION_SPEED_MIN, to=self.SIMULATION_SPEED_MAX, orient=tk.HORIZONTAL)
#         self.slider_vitesse_sim.set(10)
#         self.slider_vitesse_sim.grid(row=6,column=1)

#         #on ajoute une checkbox pour savoir si l'utilisateur veut afficher les murs
#         self.variable_checkbox_murs = tk.IntVar()
#         self.checkbox_murs = tk.Checkbutton(self.canvas_param,text="Afficher les murs",variable=self.variable_checkbox_murs)
#         self.checkbox_murs.grid(row=7,column=0)

#         #on ajoute un paramètre (scale) pour contrôler l'aspect fumée
#         self.label = tk.Label(self.canvas_param,text="Aspect fumée")
#         self.label.grid(row=8,column=0)
#         self.slider_aspect_fumee = tk.Scale(self.canvas_param, from_=0, to=7, orient=tk.HORIZONTAL)
#         self.slider_aspect_fumee.set(1)
#         self.slider_aspect_fumee.grid(row=8,column=1)

#         #on ajouter une checkbox pour savoir si l'utilisateur veut afficher le glow 
#         self.variable_checkbox_glow = tk.IntVar()
#         self.checkbox_glow = tk.Checkbutton(self.canvas_param,text="Glow",variable=self.variable_checkbox_glow)
#         self.checkbox_glow.grid(row=9,column=0)

#         #on va ajouter une checkbox pour savoir si l'utilisateur veut choisir une couleur 
#         self.variable_checkbox_color_chooser = tk.IntVar()
#         self.checkbox_color_choser = tk.Checkbutton(self.canvas_param,text="Choisir couleur",variable=self.variable_checkbox_color_chooser)
#         self.checkbox_color_choser.grid(row=10,column=0)

#         #si la personne choisit de prendre une couleur, on veut aussi pouvoir choisir la couleur 
#         self.choisir_couleur_button = tk.Button(self.canvas_param,text="couleur",command=self.choisir_couleur)
#         self.choisir_couleur_button.grid(row=10,column=1)


#         #on va créer un bouton pour lancer la simulation
#         self.button = tk.Button(self.canvas_param,text="Lancer la simulation",command=self.lancer_simulation)
#         self.button.grid(row=11,column=0)

#         #on va créer un bouton pour sauvegarder la simulation
#         self.button_sauvegarde = tk.Button(self.canvas_param,text="Sauvegarder",command=self.save_simulation)
#         self.button_sauvegarde.grid(row=11,column=1)

#         #on va créer une barre de progression
#         self.progress_bar = ttk.Progressbar(self.canvas_param,orient=tk.HORIZONTAL,length=200,mode='determinate')
#         self.progress_bar.grid(row=12,column=0,columnspan=2)

#     def choisir_couleur(self):
#         self.colors = askcolor(title="Choisit une couleur pour l'animation")

#     def lancer_simulation(self):
#         #on desactive le bouton de lancement
#         self.button.configure(state="disabled")
#         self.button_sauvegarde.configure(state="disabled")

#         #on va récupérer les points de départ
#         #on va créer un tableau qui va contenir les points de départ
#         points = []

#         #On y ajoute les points de départ qui sont stockés dans tree
#         for i in self.tree.get_children():
#             points.append(self.tree.item(i)["values"])

#         #On créer le fluide 
#         fluid = Fluid(self.RESOLUTION, 'dye')
#         inflow_dye = np.zeros(fluid.shape)
#         inflow_velocity = np.zeros_like(fluid.velocity)


#         for point in points:
#             #print(point)
#             posx,posy = [int(i) for i in point[0].split(" ")]
#             #print(posx,posy)
#             taille_point = int(point[1])
#             vitesse_point = int(point[2])
#             direction_point = int(point[3])/180*np.pi
#             point_arr = np.array([posx+taille_point//2,posy+taille_point//2])
#             mask = np.linalg.norm(fluid.indices - point_arr[:, None, None], axis=0) <= taille_point
#             if point[5]=="Directionnel":
#                 inflow_velocity[:, mask] += np.array([np.sin(direction_point),np.cos(direction_point)])[:, None] * vitesse_point
#             elif point[5]=="Divergent":
#                 x0 = posx+taille_point//2
#                 y0 = posy+taille_point//2
#                 #print(fluid.shape)
#                 f = lambda x,y: np.array([2*(x-x0),2*(y-y0)])
#                 arr = np.zeros_like(inflow_velocity)
#                 for i in range(fluid.shape[0]):
#                     for j in range(fluid.shape[1]):
#                         if mask[i, j]:
#                             vec = f(i, j)
#                             norm = np.linalg.norm(vec)
#                             # We place the vector in the last dimension of 'arr'
#                             arr[:,i, j] = vec / (norm if norm != 0 else 1)

#                 # Now 'arr' is constructed to have the same shape as 'inflow_velocity'
#                 # and can be directly used in operations with 'inflow_velocity
#                 inflow_velocity += arr * vitesse_point
#             if point[4]: inflow_dye[mask] = 1

#         #Maintenant que tout est bien initialisé, on va lancer la simulation
#         self.frames = []
#         duree = int(self.slider_duree.get())

#         color_params = np.array([0, 1, 255])
#         #if self.variable_checkbox_couleur.get()==1:
#         #    a = random.random()
#         #    b = random.random()
#         #    color_params = np.array([min(a,b),max(a,b), random.randint(30,220)])

#         #on définit une fonction qui va afficher les images
#         def afficher_image(i):
#             #print(int(slider_vitesse_sim.get()))
#             try:
#                 img = ImageTk.PhotoImage(self.frames[i])
#                 self.my_label.img = img
#                 self.my_label.configure(image=img)
                
#                 self.my_label.after(self.SIMULATION_SPEED_MAX+1-int(self.slider_vitesse_sim.get()),afficher_image,(i+1)%len(self.frames))
#             except:
#                 #img = ImageTk.PhotoImage(frames[i-1])
#                 #my_label.img = img
#                 #my_label.configure(image=img)
#                 if self.variable_checkbox_interactif.get() == 1:
#                     time.sleep(0.1)
#                     if len(self.frames) > 0:
#                         self.my_label.after(10,afficher_image,(i)%len(self.frames))
#                     else:
#                         self.my_label.after(10,afficher_image,(i))
        
#         calculating = True
#         #Si on est en mode interactif on va afficher la simulation au fur et à mesure
#         if self.variable_checkbox_interactif.get() == 1:
#             #t = threading.Thread(target=afficher_image,args=(1,))
#             #t.start()
#             afficher_image(1)
#         self.checkbox_interactif.configure(state="disabled")

#         for f in range(duree):
#             print(f'Computing frame {f + 1} of {duree}.')

#             #On ajoute les points de départ
#             if f <= duree:
#                 fluid.velocity += inflow_velocity
#                 fluid.dye += inflow_dye

#             divergence,curl,pressure = fluid.step(boundary=None,walls=self.variable_checkbox_murs.get()==1)
            
#             curl = (erf(curl * 7)+1) / 8

#             color = np.dstack((curl, np.ones(fluid.shape), fluid.dye))
#             color = (np.clip(color, color_params[0], color_params[1]) * color_params[2]).astype('uint8') 
#             if int(self.variable_checkbox_color_chooser.get())==1:
#                 color[:,:,0][color[:,:,0]>1] = rgb_to_hsv(*hex_to_rgb(self.colors[1]))[0]
#             #arr[arr > 255] = x
#             #Image.fromarray(color, mode='HSV').convert('RGB')
#             #on ajoute un peu de transparence là où la couleur est moins forte 
#             #alpha = Image.fromarray(np.clip(fluid.dye * 255, 0, 255).astype('uint8'),mode='L')
#             #image.putalpha(alpha)
#             image = Image.fromarray(color, mode='HSV').convert('RGB')
            
#             if int(self.variable_checkbox_glow.get()) == 1:
#                 #hue_index = 0
#                 #other_indices = [0,1,2] 
#                 #other_indices.remove(hue_index)
#                 #hue = color[:,:,hue_index]
                
#                 #eroded = binary_erosion(image, iterations=3)
#                 image = image.filter(ImageFilter.GaussianBlur(radius = 1)) 
#                 edges = image.filter(ImageFilter.FIND_EDGES)
#                 # Make the outlined rectangles.
#                 #outlines = image - eroded
#                 image = np.array(image)
#                 edges = np.array(edges)
#                 # Convolve with a Gaussian to effect a blur.
#                 blur = np.clip(gaussian_filter(edges, sigma=7),0,255).astype('uint8')
#                 # Combine the images and constrain to [0, 1].
#                 blur_strength = 3
#                 glow =image + blur*blur_strength
#                 glow = glow.astype(float)
#                 glow *= (255/glow.max())
#                 #on ajoute un flou gaussien
#                 #print(glow.shape)
#                 #glow[:,:,2][glow[:,:,2]<40] = 0
#                 #image = Image.fromarray(glow, mode='HSV').convert('RGB')
#                 image =  Image.fromarray(glow.astype("uint8"))

            
#             image = image.resize((self.RESOLUTION[0]*self.SCALE,self.RESOLUTION[1]*self.SCALE))
#             image = image.filter(ImageFilter.GaussianBlur(radius = int(self.slider_aspect_fumee.get()))) 
#             self.frames.append(image)
#             #on change la progression
#             self.progress_bar['value'] = f/duree*100
#             self.root.update()
#         calculating = False
#         #une fois la simulation terminée, on va l'afficher

#         #on reactive le bouton de lancement
#         self.button.configure(state="normal")
#         self.button_sauvegarde.configure(state="normal")

#         if self.variable_checkbox_interactif.get() == 0:
#             print("displaying simulation")
#             afficher_image(1)
#         self.checkbox_interactif.configure(state="normal")                

#     def supprimer_source(self):
#         selected_items = self.tree.selection()    
       
#         for selected_item in selected_items:
#             self.tree.delete(selected_item)

#         #On regarde si l'ajout frame existe, si oui on met à jour le canvas
#         if hasattr(self,"ajoutFrame"):
#             self.ajoutFrame._update_canvas()

#     def modifier_parametres(self):
#         #on va créer une fenêtre pour modifier les paramètres
#         self.top = tk.Toplevel(self.root)
#         self.top.title("Modifier les paramètres")
#         self.ajoutFrame = AjoutPointFrame(master=self.top,SimFlu=self)



#     def save_simulation(self):
#         try:
#             self.frames[0].save(f'example-{datetime.datetime.now()}.gif', save_all=True, append_images=self.frames[1:], duration=20, loop=0)
#         except Exception as e :
#             messagebox.showerror("Erreur",f"Erreur lors de la sauvegarde de la simulation: {e}")

#     def run(self):
#         self.root.mainloop()


#     def get_secret_buffer(self):
#         buffer_secret = f'''
# #Vous pouvez modifier les paramètres avec du code
# #Pour cela, vous allez devoir spécifier la variable suivante:
# # points: liste des points de départ
# # Chaque point est une liste de 6 éléments:
# #  - position: tuple (x,y)
# #  - taille: int
# #  - vitesse: int
# #  - direction: int
# #  - encre: int
# #  - mode: str

# import numpy as np
# RESOLUTION = {self.RESOLUTION}
# points = []

# encre = 1 #1 si on veut que le point laisse une trace, 0 sinon
# mode = "Directionnel" #Directionnel ou Divergent
# vitesse = 1
# taille = 7

# #Exemple1:
# points = []
# points = [[(RESOLUTION[0]//2,RESOLUTION[1]//2),taille,vitesse,0,encre,mode]]
# points.append([(RESOLUTION[0]//2-taille,RESOLUTION[1]//2),taille,vitesse,180,encre,mode])


# #Exemple2 (cercle):
# points = []

# nb_points = 10
# center = np.floor_divide(RESOLUTION, 2)
# radius = np.min(center) - 60

# positions = np.linspace(-np.pi, np.pi, nb_points, endpoint=False)
# positions = tuple(np.array((np.cos(p), np.sin(p))) for p in positions)
# normals = tuple(-p for p in positions)
# positions = tuple(radius * p + center for p in positions)

# print(positions)
# for i,pos in enumerate(positions):
#     direction = (i+2)*360/nb_points 
#     points.append([(int(pos[0]),int(pos[1])),int(taille),int(vitesse),int(direction),encre,mode])

# '''
#         return buffer_secret

