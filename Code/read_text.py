import tkinter as tk
from tkinter import filedialog
from PIL import Image , ImageTk, ImageEnhance, ImageFilter
import pytesseract
import numpy as np
import cv2

#Funcion para seleccionar y cargar la imagen 
def load_image():
    archivo = filedialog.askopenfilename()
    if archivo:
        txt_resultado.delete(1.0,tk.END)
        txt_resultado.insert(tk.END,"Loading image","color")
        txt_resultado.insert(tk.END, "\n")
        imagen = Image.open(archivo)
        imagen.thumbnail((400,400)) #ajustamos la imagen a un formato estandar
        img = ImageTk.PhotoImage(imagen) #crea una imagen compatible con tkinter
        lbl_imagen.config(image=img) #actualizar la imagen en la etiqueta
        lbl_imagen.imagen = img #crea la referencia al tkinter
        lbl_imagen.path = archivo #extrae el path
        txt_resultado.insert(tk.END,"Image loaded successfully","color")

#Extraer texto de la imagen 
def extraer_texto():
    try:
        txt_resultado.delete(1.0,tk.END)  # Imprimir mensaje de progreso
        txt_resultado.insert(tk.END, "Extracting text","color")
        if hasattr(lbl_imagen,'path'):
            imagen = Image.open(lbl_imagen.path)
            imagen_mejorada = mejorar_imagen(imagen) #mejorar la imagen
            texto = pytesseract.image_to_string(imagen_mejorada) #Extraer texto
            txt_resultado.insert(tk.END, "\n")  # Insertar salto de linea
            txt_resultado.insert(tk.END, texto,"color")
    except Exception as e:
        print(f"Error al extraer texto: {e}")

def mejorar_imagen(imagen):
    #convertir a escala de grises
    imagen = imagen.convert('L')
    #Eliminar ruido 
    imagen = imagen.filter(ImageFilter.GaussianBlur(1))
    #convertir a un arreglo para binarizar la imagen
    imagen_np = np.array(imagen)
    #binarizar la imagen con umbral 
    _,imagen_binaria = cv2.threshold(imagen_np,128,255,cv2.THRESH_BINARY)
    imagen_mejorada = Image.fromarray(imagen_binaria)
    return imagen_mejorada

#Configuracion de Ventana
ventana = tk.Tk()
ventana.title("Extraer Texto")
ventana.geometry("800x700")

#Boton para cargar imagen
btn_cargar = tk.Button(ventana, text="Cargar Imagen", command=load_image)
btn_cargar.pack(pady=10)

#Label para mostrar la imagen
lbl_imagen = tk.Label(ventana)
lbl_imagen.pack()

#Boton para extraer texto
btn_extraer = tk.Button(ventana, text="Extraer Texto", command=extraer_texto)
btn_extraer.pack()

#Cuadro para mostrar el resultado
txt_resultado = tk.Text(ventana, height=50, width=100)
txt_resultado.pack(pady=10)
txt_resultado.tag_config("color",foreground="#00ff00")
txt_resultado.insert(tk.END, "Carge una imagen para iniciar el analisis","color")

#Ejecutar la aplicacion 
ventana.mainloop()