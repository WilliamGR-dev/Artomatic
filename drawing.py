import pyautogui
import keyboard
import numpy as np
import shared
import time

# Réglages de pyautogui pour réduire les délais
pyautogui.PAUSE = 0.01  # Pause très courte entre les actions
pyautogui.MINIMUM_SLEEP = 0  # Pas de délai minimum de sommeil
pyautogui.DURATION = 0  # Déplacement instantané

def enter_rgb_values(color, rgb_positions):
    """
    Entrer les valeurs RGB dans les champs de saisie.
    """
    r, g, b = color
    r_position, g_position, b_position = rgb_positions

    # Entrer la valeur de R
    pyautogui.click(r_position)
    pyautogui.hotkey('ctrl', 'a')  # Sélectionner tout le texte dans le champ
    pyautogui.typewrite(str(r))

    # Entrer la valeur de G
    pyautogui.click(g_position)
    pyautogui.hotkey('ctrl', 'a')  # Sélectionner tout le texte dans le champ
    pyautogui.typewrite(str(g))

    # Entrer la valeur de B
    pyautogui.click(b_position)
    pyautogui.hotkey('ctrl', 'a')  # Sélectionner tout le texte dans le champ
    pyautogui.typewrite(str(b))

    # Attendre que la couleur soit appliquée
    time.sleep(0.1)

def click_to_access_rgb_inputs():
    """
    Clique sur les positions capturées pour accéder aux champs RGB.
    """
    for position in shared.color_click_positions:
        pyautogui.click(position)
        time.sleep(0.1)  # Pause pour s'assurer que le clic est traité

def draw_lines(points_by_color, start_pos, color_positions, step_size=1):
    """
    Dessine des lignes en utilisant pyautogui avec des mouvements optimisés et en changeant de couleur.
    """
    white_color = (255, 255, 255)
    tolerance_for_white = 20

    def is_near_white(color):
        return np.linalg.norm(np.array(color) - np.array(white_color)) < tolerance_for_white

    # Séparer les points blancs des autres couleurs
    white_points = []
    filtered_points_by_color = {}

    for color, points in points_by_color.items():
        if is_near_white(color):
            white_points.extend(points)
        else:
            filtered_points_by_color[color] = points

    # Dessiner les autres couleurs en premier
    for color, points in filtered_points_by_color.items():
        print(f"Dessin avec la couleur : {color}")

        if shared.rgb_input_positions:
            # Cliquer sur les positions capturées (normales) avant d'utiliser les champs RGB
            for pos in shared.color_click_positions:
                pyautogui.click(pos)
                time.sleep(0.1)

            # Utiliser les champs RGB pour définir la couleur exacte
            enter_rgb_values(color, shared.rgb_input_positions)
        elif color_positions:
            # Utiliser la palette si elle est disponible
            color_index = find_closest_color_index(color, color_positions)
            if color_index != -1:
                pyautogui.click(color_positions[color_index])
            else:
                print(f"Impossible de trouver la couleur {color} dans la palette capturée.")
                return
        else:
            print(f"Ni les champs RGB ni la palette ne sont disponibles pour la couleur {color}.")
            return

        if points:
            pyautogui.moveTo(start_pos[0] + points[0][0] * step_size,
                             start_pos[1] + points[0][1] * step_size)
            pyautogui.mouseDown(button='left')

            previous_x, previous_y = points[0]
            for i, (x, y) in enumerate(points):
                if keyboard.is_pressed('esc'):
                    print("Dessin annulé par l'utilisateur.")
                    pyautogui.mouseUp(button='left')
                    return

                if i % 100 == 0:
                    print(f"Dessiné {i} points pour la couleur {color}")

                real_x = start_pos[0] + x * step_size
                real_y = start_pos[1] + y * step_size

                # Vérifier la discontinuité
                if abs(real_x - (start_pos[0] + previous_x * step_size)) > step_size or \
                        abs(real_y - (start_pos[1] + previous_y * step_size)) > step_size:
                    pyautogui.mouseUp(button='left')
                    pyautogui.moveTo(real_x, real_y)
                    pyautogui.mouseDown(button='left')
                else:
                    pyautogui.dragTo(real_x, real_y, duration=0, button='left')

                previous_x, previous_y = x, y

            pyautogui.mouseUp(button='left')

    # Dessiner les points blancs en dernier
    if white_points:
        print("Dessin des points blancs en dernier")
        if shared.rgb_input_positions:
            # Cliquer sur les positions capturées (normales) avant d'utiliser les champs RGB pour le blanc
            for pos in shared.color_click_positions:
                pyautogui.click(pos)
                time.sleep(0.1)

            # Utiliser RGB pour le blanc si en mode RGB
            enter_rgb_values(white_color, shared.rgb_input_positions)
        else:
            color_index = find_closest_color_index(white_color, color_positions)
            pyautogui.click(color_positions[color_index])

        previous_x, previous_y = white_points[0]
        pyautogui.moveTo(start_pos[0] + previous_x * step_size,
                         start_pos[1] + previous_y * step_size)
        pyautogui.mouseDown(button='left')

        for i, (x, y) in enumerate(white_points):
            if keyboard.is_pressed('esc'):
                print("Dessin annulé par l'utilisateur.")
                pyautogui.mouseUp(button='left')
                return

            if i % 100 == 0:
                print(f"Dessiné {i} points pour la couleur blanche")

            real_x = start_pos[0] + x * step_size
            real_y = start_pos[1] + y * step_size

            if abs(real_x - (start_pos[0] + previous_x * step_size)) > step_size or \
                    abs(real_y - (start_pos[1] + previous_y * step_size)) > step_size:
                pyautogui.mouseUp(button='left')
                pyautogui.moveTo(real_x, real_y)
                pyautogui.mouseDown(button='left')
            else:
                pyautogui.dragTo(real_x, real_y, duration=0, button='left')

            previous_x, previous_y = x, y

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
