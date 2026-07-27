from PIL import Image
import numpy as np
from sklearn.cluster import KMeans


def extract_palette(image_path, num_colors=6, resize_to=150):

    """
    Extracts the dominant colors from an image.


    args:
        image_path (str): The path to the image file.
        num_colors (int): The number of dominant colors to extract.
        resize_to (int): The size to which the image will be resized for processing.

    returns:
        list of dicts:[{'hex': '#RRGGBB', 'rgb': (R, G, B), 'percentage': 0.34}, ...]   
        sorted by how much of the image each color covers, descending.

    """
    image = Image.open(image_path).convert('RGB')
    image = image.resize((resize_to, resize_to))
    pixels = np.array(image).reshape(-1, 3)
    kmeans = KMeans(n_clusters=num_colors, n_init=10, random_state=42)
    labels = kmeans.fit_predict(pixels)
    centers = kmeans.cluster_centers_.astype(int)
    counts = np.bincount(labels, minlength=num_colors)
    total_count = counts.sum()


    palette = []
    for i, center in enumerate(centers):
        r, g, b = int(center[0]), int(center[1]), int(center[2])
        hex_color = '#{:02x}{:02x}{:02x}'.format(r, g, b)
        percentage = float(counts[i] / total_count)
        palette.append({'hex': hex_color, 'rgb': (r, g, b), 'percentage': percentage})

    palette.sort(key=lambda x: x['percentage'], reverse=True)
    return palette


   