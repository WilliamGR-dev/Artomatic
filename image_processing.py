from PIL import Image
import numpy as np

def resize_image(image, max_width, max_height):
    """
    Redimensionne l'image pour qu'elle s'adapte à la taille maximale donnée sans étirer ni écraser l'image.

    :param image: Instance de l'image PIL.
    :param max_width: Largeur maximale de la zone de dessin.
    :param max_height: Hauteur maximale de la zone de dessin.
    :return: Image redimensionnée.
    """
    original_width, original_height = image.size
    aspect_ratio = original_width / original_height

    if max_width / max_height > aspect_ratio:
        # Limité par la hauteur
        new_height = max_height
        new_width = int(max_height * aspect_ratio)
    else:
        # Limité par la largeur
        new_width = max_width
        new_height = int(max_width / aspect_ratio)

    # Utiliser LANCZOS pour un redimensionnement de haute qualité
    resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    return resized_image

def image_to_lines(image_path, max_width, max_height, threshold=128, sample_rate=6):
    """
    Convertit une image en lignes de dessin avec un échantillonnage pour réduire la résolution.

    :param image_path: Chemin de l'image à dessiner.
    :param max_width: Largeur maximale de la zone de dessin.
    :param max_height: Hauteur maximale de la zone de dessin.
    :param threshold: Seuil de binarisation pour convertir l'image en noir et blanc.
    :param sample_rate: Intervalle d'échantillonnage en pixels.
    :return: Liste de points à dessiner.
    """
    img = Image.open(image_path).convert('L')  # Convertir en niveaux de gris
    img = img.point(lambda p: p > threshold and 255)  # Binariser l'image

    # Redimensionner l'image pour s'adapter à la zone de dessin sans déformation
    resized_image = resize_image(img, max_width, max_height)
    resized_image_array = np.array(resized_image)
    lines = []

    # Parcourir l'image redimensionnée avec un échantillonnage
    for y in range(0, resized_image_array.shape[0], sample_rate):
        for x in range(0, resized_image_array.shape[1], sample_rate):
            if resized_image_array[y, x] == 0:
                lines.append((x, y))

    return lines, resized_image.size  # Retourne aussi la taille de l'image redimensionnée
