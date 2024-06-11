from PIL import Image
import numpy as np
from sklearn.cluster import KMeans

def resize_image(image, max_width, max_height):
    """
    Redimensionne l'image pour qu'elle s'adapte à la taille maximale donnée sans étirer ni écraser l'image.
    """
    original_width, original_height = image.size
    aspect_ratio = original_width / original_height

    if max_width / max_height > aspect_ratio:
        new_height = max_height
        new_width = int(max_height * aspect_ratio)
    else:
        new_width = max_width
        new_height = int(max_width / aspect_ratio)

    resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    return resized_image

def get_dominant_colors(image, num_colors=10):
    """
    Extrait les couleurs dominantes de l'image en utilisant K-means clustering.
    """
    image = image.convert('RGB')
    image = np.array(image)
    pixels = image.reshape(-1, 3)

    kmeans = KMeans(n_clusters=num_colors)
    kmeans.fit(pixels)

    colors = kmeans.cluster_centers_.astype(int)
    return colors

def find_closest_palette_color(color, palette):
    """
    Trouve la couleur la plus proche dans la palette donnée.
    """
    palette = np.array(palette)
    distances = np.sqrt(np.sum((palette - color) ** 2, axis=1))
    return palette[np.argmin(distances)]

def image_to_lines(image_path, max_width, max_height, threshold=128, sample_rate=6, num_colors=10):
    """
    Convertit une image en lignes de dessin avec un échantillonnage pour réduire la résolution.
    """
    img = Image.open(image_path)
    img = resize_image(img, max_width, max_height)

    dominant_colors = get_dominant_colors(img, num_colors=num_colors)

    gartic_palette = [
        (0, 0, 0), (255, 255, 255), (128, 128, 128), (192, 192, 192),
        (255, 0, 0), (128, 0, 0), (255, 255, 0), (128, 128, 0),
        (0, 255, 0), (0, 128, 0), (0, 255, 255), (0, 128, 128),
        (0, 0, 255), (0, 0, 128), (255, 0, 255), (128, 0, 128)
    ]

    color_mapping = {tuple(color): find_closest_palette_color(color, gartic_palette) for color in dominant_colors}

    img = img.convert('RGB')
    img_data = np.array(img)
    lines = []

    for y in range(0, img_data.shape[0], sample_rate):
        for x in range(0, img_data.shape[1], sample_rate):
            pixel_color = tuple(img_data[y, x])
            closest_color = find_closest_palette_color(pixel_color, list(color_mapping.keys()))
            if closest_color is not None:
                lines.append((x, y, closest_color))

    return lines, img.size
