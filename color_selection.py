import pyautogui
import time
import keyboard
import mouse
from PIL import ImageGrab

# Variables globales pour les positions de clic et les couleurs
color_click_positions = []

def capture_color_click():
    """
    Capture la position du clic dans la palette de couleurs et affiche la couleur correspondante.
    """
    # Capturer la position du clic
    position = pyautogui.position()
    color_click_positions.append(position)
    print(f"Position capturée : {position}")

    # Vérifier si la position est dans les limites de l'écran
    screen_width, screen_height = pyautogui.size()
    if not (0 <= position[0] < screen_width and 0 <= position[1] < screen_height):
        print("La position est en dehors des limites de l'écran.")
        return None

    # Capturer la couleur à cette position
    try:
        screenshot = ImageGrab.grab()
        color = screenshot.getpixel(position)
        print(f"Couleur capturée : {color}")
        return color
    except Exception as e:
        print(f"Erreur lors de la capture de la couleur : {e}")
        return None

def select_colors():
    """
    Permet à l'utilisateur de capturer les positions des clics dans la palette de couleurs.
    """
    print("Cliquez sur les couleurs de la palette. Appuyez sur 'Échap' pour terminer.")

    def on_click(event):
        # Cette fonction est appelée à chaque clic de souris
        if event.event_type == 'down' and event.button == 'left':
            color = capture_color_click()
            if color is not None:
                print(f"Couleur sélectionnée : {color}")

    # Attacher la fonction de gestion des clics
    mouse.hook(on_click)

    try:
        # Boucle principale pour arrêter la capture avec 'Échap'
        while True:
            if keyboard.is_pressed('esc'):
                print("Sélection des couleurs terminée.")
                break
            time.sleep(0.1)
    finally:
        # Détacher la fonction de gestion des clics
        mouse.unhook(on_click)

    print("Positions des clics de couleur : ", color_click_positions)
