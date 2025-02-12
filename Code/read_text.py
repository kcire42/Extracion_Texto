import tkinter as tk
from tkinter import filedialog
from PIL import Image , ImageTk
import pytesseract

#Funcion para seleccionar y cargar la imagen 
def load_image():
    archivo = filedialog.askopenfilename()
    if archivo:
        print("Loading image")
        imagen = Image.open(archivo)
        imagen.thumbnail((400,400))
        img = ImageTk.PhotoImage(imagen)
        lbl_imagen.image = img
        lbl_imagen.path = archivo

#Extraer texto de la imagen 
def extraer_texto():
    try:
        print("Extracting text")  # Imprimir mensaje de progreso
        if hasattr(lbl_imagen,'path'):
            texto = pytesseract.image_to_string(Image.open(lbl_imagen.path)) #Extraer texto
            txt_resultado.delete(1.0,tk.END) #Borra el texto anteriro del recuadro para despues insertarlo
            txt_resultado.insert(tk.END, texto)
    except Exception as e:
        print(f"Error al extraer texto: {e}")

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

#Ejecutar la aplicacion 
ventana.mainloop()