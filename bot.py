import os
import time
from datetime import datetime

from numpy import *
from PIL import ImageGrab, ImageOps
import pyautogui as py


ANCHO_INICIAL_MUESTRA = 170

# ATENCIÓN: Solo poner GUARDAR_IMAGENES = True para ver los resultados de las imágenes en pruebas,
# no dejarlo activado para jugar, ya que acumulará muchas imágenes en el directorio imagenes_temp
# en un breve lapso de tiempo.
GUARDAR_IMAGENES = False
TEMP_IMAGE_DIR = "./imagenes_temp"

tiempo_de_juego = 0


def obtener_rectangulos(x, y, ancho, alto, desplazamiento_control):
    """Obtiene los rectángulos de la imagen de la pantalla

    Args:
        x (int): posición x del rectángulo
        y (int): posición y del rectángulo
        ancho (int): ancho del rectángulo
        alto (int): alto del rectángulo
        desplazamiento_control (int): cantidad de píxeles en y que
        desplazaremos para la captura de comparación

    Returns:
        tuple: rectángulo_de_control, rectángulo_de_comparación
    """
    rect = (x, y, x + ancho, y + alto)
    rect_control = (
        x,
        y + desplazamiento_control,
        x + ancho,
        y + alto + desplazamiento_control,
    )

    return rect, rect_control


def cuantificar_area(rectangulo, prefijo_imagen=""):
    """Calcula el valor numérico de la imagen capturada

    Args:
        rectangulo (int): _description_
        prefijo_imagen (str, optional): nombre que definimos como prefijo para guardar la captura. Defaults to "".

    Returns:
        int: sumatoria de los valores de la imagen
    """
    image = ImageGrab.grab(rectangulo)
    if GUARDAR_IMAGENES:
        os.makedirs(TEMP_IMAGE_DIR, exist_ok=True)
        image.save(
            os.path.join(
                TEMP_IMAGE_DIR,
                f"{prefijo_imagen}_{datetime.now().strftime('%Y%m%d_%I%M%S%f')}.png",
            )
        )
    image = ImageOps.grayscale(image)
    arr = array(image.getcolors())
    return arr.sum()


def verificar_area_requiere_accion(
    x, y, ancho, alto, desplazamiento_control, tolerancia=0, mostrar_resultados=False
):
    """_summary_

    Args:
        x (int): posición x del rectángulo
        y (int): posición y del rectángulo
        ancho (int): ancho del rectángulo
        alto (int): alto del rectángulo
        desplazamiento_control (int): cantidad de píxeles en y que
        desplazaremos para la captura de comparación.
        tolerancia (int, optional): Valor de tolerancia aplicado a la diferencia entre imágenes (control/comparación). Defaults to 0.
        mostrar_resultados (bool, optional): muestra en pantalla los valores calculados de las imágenes. Defaults to False.

    Returns:
        bool: Si es verdadero debemos realizar una acción (por ejemplo saltar)
    """
    area_muestra, area_control = obtener_rectangulos(
        x, y, ancho, alto, desplazamiento_control
    )

    valor_area_muestra = cuantificar_area(area_muestra, prefijo_imagen="muestra")
    valor_area_control = cuantificar_area(area_control, prefijo_imagen="control")

    # Se calcula un porcentaje de la diferencia entre el área de la muestra y el área de control
    # (Esto es porque hay casos en los que requiere tener una tolerancia,
    # por ejemplo cuando se realiza la transición de día a noche)
    resultado = abs(valor_area_control - valor_area_muestra) / valor_area_muestra * 100
    if mostrar_resultados and resultado != 0:
        print(f"ancho: {ancho} \nresultado: {resultado} tolerancia: {tolerancia}")
    return resultado > tolerancia


def verificar_saltar(x=135, y=400, ancho_muestra=170, alto_muestra=75):
    """Verifica si es necesario saltar según los parámetros requeridos para tal acción

    Args:
        x (int, optional): posición x del rectángulo. Defaults to 135.
        y (int, optional): posición y del rectángulo. Defaults to 400.
        ancho_muestra (int, optional): ancho del rectángulo. Defaults to 170.
        alto_muestra (int, optional): alto del rectángulo. Defaults to 75.

    Returns:
        bool: Verdadero si detectamos un objeto en el área de la muestra
    """
    desplazamiento_control = 150
    tolerancia = 0.5
    return verificar_area_requiere_accion(
        x,
        y,
        ancho_muestra,
        alto_muestra,
        desplazamiento_control,
        tolerancia,
        mostrar_resultados=True,
    )


# def verificar_agacharse(x=135, y=390):
#     time.sleep(0.2)
#     alto = 20
#     desplazamiento_control = 0
#     tolerancia = 0
#     return verificar_area_requiere_accion(
#         x, y, ancho, alto, desplazamiento_control, tolerancia
#     )


def verificar_game_over(x=450, y=250, ancho=465, alto=63):
    """Verifica si el juego finalizó

    Args:
        x (int, optional): posición x del rectángulo. Defaults to 450.
        y (int, optional): posición y del rectángulo. Defaults to 250.
        ancho_muestra (int, optional): ancho del rectángulo. Defaults to 465.
        alto_muestra (int, optional): alto del rectángulo. Defaults to 63.

    Returns:
        bool: Verdadero si detectamos que apareció un mensaje en el áre de "game over"
    """
    desplazamiento_control = 300
    tolerancia = 0.8
    return verificar_area_requiere_accion(
        x, y, ancho, alto, desplazamiento_control, tolerancia
    )


def saltar():
    """Simulamos la acción de saltar presionando la tecla direccional 'arriba'"""
    # Según el tiempo transcurrido asumimos que aumenta
    # la velocidad por lo que reducimos el tiempo de salto
    duracion = 0.3  # con 0.5 o más realiza doble salto
    if tiempo_de_juego > 500:
        duracion = 0.2

    print(f"Saltar duracion: {duracion}")
    py.keyDown("up")
    time.sleep(duracion)
    py.keyUp("up")


# def agacharse():
#     duracion = 0.5
#     if tiempo_de_juego > 200:
#         duracion = 0.4
#     elif tiempo_de_juego > 500:
#         duracion = 0.3

#     py.keyDown("down")
#     time.sleep(duracion)
#     py.keyUp("down")


if __name__ == "__main__":
    time.sleep(1)
    ancho = ANCHO_INICIAL_MUESTRA
    while True:
        # Según el tiempo transcurrido asumimos que aumenta
        # la velocidad por lo que ampliamos el área de control para anticipar movimientos
        tiempo_de_juego += 1
        if tiempo_de_juego > 350:
            ancho = 350
        elif tiempo_de_juego > 170:
            ancho += 1

        if verificar_saltar(ancho_muestra=ancho):
            saltar()

        if verificar_game_over():
            ancho = ANCHO_INICIAL_MUESTRA
            tiempo_de_juego = 0
            saltar()  # reiniciar juego
            print("Game Over")
