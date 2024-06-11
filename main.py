from image_processing import image_to_lines
from drawing import draw_lines
from color_selection import select_colors
from gui import create_gui
import shared  # Importer le module global
import time


def start_drawing():
    start_pos = shared.start_pos
    end_pos = shared.end_pos

    print(f"Valeur de start_pos: {start_pos}")
    print(f"Valeur de end_pos: {end_pos}")

    if start_pos is None or end_pos is None:
        print("Veuillez sélectionner deux points pour dessiner.")
        return

    min_x = min(start_pos[0], end_pos[0])
    min_y = min(start_pos[1], end_pos[1])
    max_x = max(start_pos[0], end_pos[0])
    max_y = max(start_pos[1], end_pos[1])

    max_width = max_x - min_x
    max_height = max_y - min_y

    print(f"Taille de la zone de dessin: {max_width}x{max_height}")

    print("Préparation pour dessiner dans 5 secondes...")
    time.sleep(5)

    print("Conversion de l'image en lignes...")
    lines, image_size = image_to_lines(shared.file_path, max_width, max_height)

    print(f"Démarrage du dessin... Taille de l'image redimensionnée: {image_size}")
    print("Appuyez sur Échap pour annuler.")

    draw_start_pos = (
        min_x + (max_width - image_size[0]) // 2,
        min_y + (max_height - image_size[1]) // 2
    )

    print(f"Position de départ pour le dessin: {draw_start_pos}")

    color_positions = shared.color_click_positions

    # Organiser les points par couleur
    points_by_color = {}
    for x, y, color in lines:
        color_tuple = tuple(color)
        if color_tuple not in points_by_color:
            points_by_color[color_tuple] = []
        points_by_color[color_tuple].append((x, y))

    draw_lines(points_by_color, draw_start_pos, color_positions)

    print("Dessin terminé ou annulé par l'utilisateur !")


if __name__ == "__main__":
    create_gui(start_drawing, select_colors)
