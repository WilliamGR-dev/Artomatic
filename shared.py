# shared.py

# Variables globales pour stocker les informations partagées
file_path = None  # Chemin du fichier d'image sélectionné
start_pos = None  # Position de début de la zone de dessin
end_pos = None  # Position de fin de la zone de dessin
color_click_positions = []  # Liste des positions cliquées pour les couleurs
gartic_palette = []  # Palette des couleurs capturées
precision_mode = False  # Mode précision activé ou non
rgb_input_positions = []  # Positions des champs de saisie RGB

# Fonction pour réinitialiser les variables partagées
def reset_shared_variables():
    global file_path, start_pos, end_pos, color_click_positions, gartic_palette, precision_mode, rgb_input_positions
    file_path = None
    start_pos = None
    end_pos = None
    color_click_positions = []
    gartic_palette = []
    precision_mode = False
    rgb_input_positions = []

# Appelez cette fonction pour réinitialiser toutes les variables partagées
reset_shared_variables()
