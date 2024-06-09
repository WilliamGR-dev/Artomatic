import pyautogui
import keyboard

def draw_lines(lines, start_pos, step_size=1):
    """
    Dessine des lignes en utilisant pyautogui avec des mouvements optimisés.

    :param lines: Liste de points à dessiner.
    :param start_pos: Position de départ pour le dessin.
    :param step_size: Taille de l'échantillonnage pour la réduction des mouvements.
    """
    pyautogui.moveTo(start_pos[0], start_pos[1])
    pyautogui.click()

    for (x, y) in lines:
        if keyboard.is_pressed('esc'):  # Vérifier si la touche Échap est pressée
            print("Dessin annulé par l'utilisateur.")
            break

        # Calculer la position réelle à dessiner
        real_x = start_pos[0] + x * step_size
        real_y = start_pos[1] + y * step_size

        # Vérifier que la position est bien dans la zone de dessin
        if real_x < start_pos[0] or real_y < start_pos[1]:
            print(f"Position {real_x}, {real_y} en dehors de la zone de dessin")
            continue

        # Déplacer la souris à la nouvelle position
        pyautogui.moveTo(real_x, real_y)
        pyautogui.mouseDown(button='left')
        pyautogui.dragTo(real_x, real_y, button='left')
    pyautogui.mouseUp(button='left')
