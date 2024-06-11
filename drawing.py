import pyautogui
import keyboard
import numpy as np


def draw_lines(lines, start_pos, color_positions, step_size=1):
    """
    Dessine des lignes en utilisant pyautogui avec des mouvements optimisés et en changeant de couleur.

    :param lines: Liste de points à dessiner.
    :param start_pos: Position de départ pour le dessin.
    :param color_positions: Liste des positions des couleurs capturées dans la palette.
    :param step_size: Taille de l'échantillonnage pour la réduction des mouvements.
    """
    pyautogui.moveTo(start_pos[0], start_pos[1])
    pyautogui.click()

    current_color = None
    for (x, y, color) in lines:
        if keyboard.is_pressed('esc'):  # Vérifier si la touche Échap est pressée
            print("Dessin annulé par l'utilisateur.")
            break

        real_x = start_pos[0] + x * step_size
        real_y = start_pos[1] + y * step_size

        if current_color is None or not np.array_equal(current_color, color):
            try:
                color_index = find_closest_color_index(color, color_positions)
                pyautogui.click(color_positions[color_index])
                current_color = color
            except ValueError:
                print(f"Couleur {color} non trouvée dans la palette.")
                continue

        pyautogui.moveTo(real_x, real_y)
        pyautogui.mouseDown(button='left')
        pyautogui.dragTo(real_x, real_y, button='left')
    pyautogui.mouseUp(button='left')


def find_closest_color_index(color, color_positions):
    """
    Trouve l'index de la position de couleur la plus proche dans color_positions.
    """
    closest_index = -1
    min_distance = float('inf')
    for i, color_position in enumerate(color_positions):
        screenshot = pyautogui.screenshot(region=(color_position[0], color_position[1], 1, 1))
        captured_color = screenshot.getpixel((0, 0))
        distance = np.sqrt(np.sum((np.array(captured_color) - np.array(color)) ** 2))
        if distance < min_distance:
            min_distance = distance
            closest_index = i
    return closest_index
