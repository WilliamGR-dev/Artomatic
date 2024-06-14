import tkinter as tk
from tkinter import filedialog
import pyautogui
import time
import shared  # Mise à jour de l'importation du module global
from color_selection import capture_all_and_rgb_clicks  # Importer les fonctions nécessaires

def select_image(status_label, start_button):
    shared.file_path = filedialog.askopenfilename(
        title="Sélectionnez une image",
        filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp"), ("All files", "*.*")]
    )
    if shared.file_path:
        start_button.config(state=tk.NORMAL)
        status_label.config(text=f"Fichier sélectionné : {shared.file_path}")

def select_points(status_label):
    status_label.config(text="Déplacez la fenêtre et cliquez sur les points désirés.")

    # Cacher la fenêtre pour permettre la capture des points
    root.withdraw()

    # Capturer les deux points en demandant à l'utilisateur de cliquer
    pyautogui.alert('Cliquez OK, puis cliquez sur le point de départ de la zone de dessin.')
    shared.start_pos = pyautogui.position()
    time.sleep(1)  # Pause pour permettre la capture du point

    pyautogui.alert('Cliquez OK, puis cliquez sur le point de fin de la zone de dessin.')
    shared.end_pos = pyautogui.position()
    time.sleep(1)  # Pause pour permettre la capture du point

    # Réafficher la fenêtre après la capture des points
    root.deiconify()

    # Imprimer les points capturés pour vérification
    print(f"Points capturés : Début {shared.start_pos}, Fin {shared.end_pos}")

    if shared.start_pos and shared.end_pos:
        status_label.config(text=f"Points capturés : Début {shared.start_pos}, Fin {shared.end_pos}")
    else:
        status_label.config(text="Échec de la capture des points. Veuillez réessayer.")

def create_gui(start_drawing, select_colors, capture_all_and_rgb_clicks):
    global status_label, start_button, root

    root = tk.Tk()
    root.title("Bot de Dessin")

    start_button = tk.Button(root, text="Lancer le Dessin", command=start_drawing, state=tk.DISABLED)
    start_button.pack(pady=10)

    select_button = tk.Button(root, text="Sélectionner l'image", command=lambda: select_image(status_label, start_button))
    select_button.pack(pady=10)

    capture_button = tk.Button(root, text="Sélectionner Points", command=lambda: select_points(status_label))
    capture_button.pack(pady=10)

    color_button = tk.Button(root, text="Capturer Couleurs", command=select_colors)
    color_button.pack(pady=10)

    precision_var = tk.BooleanVar()
    precision_checkbox = tk.Checkbutton(root, text="Mode Précision", variable=precision_var, command=lambda: set_precision_mode(precision_var))
    precision_checkbox.pack(pady=10)

    capture_all_button = tk.Button(root, text="Capturer tous les clics et les champs RGB", command=capture_all_and_rgb_clicks)
    capture_all_button.pack(pady=10)

    status_label = tk.Label(root, text="Aucun fichier ou point sélectionné")
    status_label.pack(pady=20)

    root.mainloop()

def set_precision_mode(precision_var):
    shared.precision_mode = precision_var.get()
    print(f"Mode précision activé : {shared.precision_mode}")
