import pyautogui
import time
import keyboard
import mouse
from PIL import ImageGrab
import shared  # Importer le module global

def capture_color_click():
    """
    Capture la position du clic dans la palette de couleurs et affiche la couleur correspondante.
    """
    position = pyautogui.position()
    shared.color_click_positions.append(position)  # Utiliser shared.color_click_positions
    print(f"Position capturée : {position}")

    screen_width, screen_height = pyautogui.size()
    if not (0 <= position[0] < screen_width and 0 <= position[1] < screen_height):
        print("La position est en dehors des limites de l'écran.")
        return None

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
        if event.event_type == 'down' and event.button == 'left':
            color = capture_color_click()
            if color is not None:
                print(f"Couleur sélectionnée : {color}")

    mouse.hook(on_click)

    try:
        while True:
            if keyboard.is_pressed('esc'):
                print("Sélection des couleurs terminée.")
                break
            time.sleep(0.1)
    finally:
        mouse.unhook(on_click)

    print("Positions des clics de couleur : ", shared.color_click_positions)
