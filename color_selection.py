import pyautogui
import time
import keyboard
import mouse
import shared
from PIL import ImageGrab

def capture_color_click():
    """
    Capture la position du clic dans la palette de couleurs et affiche la couleur correspondante.
    """
    position = pyautogui.position()
    shared.color_click_positions.append(position)
    print(f"Position capturée : {position}")

    screen_width, screen_height = pyautogui.size()
    if not (0 <= position[0] < screen_width and 0 <= position[1] < screen_height):
        print("La position est en dehors des limites de l'écran.")
        return None

    try:
        screenshot = ImageGrab.grab()
        color = screenshot.getpixel(position)
        print(f"Couleur capturée : {color}")

        # Ajouter la couleur capturée à la palette
        shared.gartic_palette.append(color)

        return color
    except Exception as e:
        print(f"Erreur lors de la capture de la couleur : {e}")
        return None

def capture_all_clicks():
    """
    Capture tous les clics de l'utilisateur pour les opérations normales jusqu'à ce que 'Échap' soit pressé.
    """
    print("Cliquez n'importe où pour capturer les positions. Appuyez sur 'Échap' pour terminer.")

    def on_click(event):
        if isinstance(event, mouse.ButtonEvent) and event.event_type == 'down' and event.button == 'left':
            position = pyautogui.position()
            shared.color_click_positions.append(position)
            print(f"Position capturée : {position}")

    mouse.hook(on_click)

    try:
        while True:
            if keyboard.is_pressed('esc'):
                print("Capture des clics terminée.")
                break
            time.sleep(0.1)
    finally:
        mouse.unhook(on_click)

    print("Positions des clics capturées : ", shared.color_click_positions)

def separate_rgb_clicks():
    """
    Sépare les clics capturés en clics normaux et clics pour les champs RGB.
    """
    if len(shared.color_click_positions) < 4:
        print("Pas assez de clics capturés pour séparer les champs RGB.")
        return

    # Les trois derniers clics sont pour RGB
    shared.rgb_input_positions = shared.color_click_positions[-3:]
    # Tous les clics avant les trois derniers sont les clics normaux
    shared.color_click_positions = shared.color_click_positions[:-3]
    print("Positions des clics normaux : ", shared.color_click_positions)
    print("Positions des champs RGB : ", shared.rgb_input_positions)

def capture_all_and_rgb_clicks():
    """
    Capture tous les clics pour les opérations normales, puis sépare les trois clics pour les champs RGB.
    """
    capture_all_clicks()
    separate_rgb_clicks()

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
    print("Palette de couleurs capturée : ", shared.gartic_palette)

    # Vérification que la palette n'est pas vide
    if len(shared.gartic_palette) == 0:
        print("Erreur : aucune couleur n'a été capturée dans la palette.")
