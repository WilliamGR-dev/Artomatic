from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
import shared  # Importer le module global


def resize_image(image, max_width, max_height):
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
    image = image.convert('RGB')
    image = np.array(image)
    pixels = image.reshape(-1, 3)

    kmeans = KMeans(n_clusters=num_colors)
    kmeans.fit(pixels)

    colors = kmeans.cluster_centers_.astype(int)
    return colors


def find_closest_palette_color(color, palette, tolerance=5):
    """
    Trouve la couleur la plus proche dans la palette donnée en utilisant une tolérance plus stricte.

    :param color: La couleur à comparer (sous forme de tuple RGB).
    :param palette: La palette de couleurs disponibles (liste de tuples RGB).
    :param tolerance: La tolérance pour considérer les couleurs comme équivalentes.
    :return: La couleur la plus proche dans la palette ou None si aucune couleur n'est suffisamment proche.
    """
    palette = np.array(palette)
    distances = np.sqrt(np.sum((palette - color) ** 2, axis=1))

    min_distance = np.min(distances)
    if min_distance <= tolerance:
        return tuple(palette[np.argmin(distances)])
    else:
        return None


def image_to_lines(image_path, max_width, max_height, sample_rate=6, num_colors=10, tolerance=100):
    img = Image.open(image_path)
    img = resize_image(img, max_width, max_height)

    dominant_colors = get_dominant_colors(img, num_colors=num_colors)

    gartic_palette = shared.gartic_palette

    color_mapping = {tuple(color): find_closest_palette_color(color, gartic_palette, tolerance) for color in
                     dominant_colors}

    img = img.convert('RGB')
    img_data = np.array(img)
    lines = []

    for y in range(0, img_data.shape[0], sample_rate):
        for x in range(0, img_data.shape[1], sample_rate):
            pixel_color = tuple(img_data[y, x])
            closest_color = find_closest_palette_color(pixel_color, list(color_mapping.keys()), tolerance)
            if closest_color is not None:
                lines.append((x, y, closest_color))

    return lines, img.size
