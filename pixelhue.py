from colorthief import ColorThief


def extract_palette(image_path, num_colors=6):

    """
    Extracts the dominant colors from an image.

    args:
        image_path (str): The path to the image file.
        num_colors (int): The number of dominant colors to extract.

    returns:
        list of dicts:[{'hex': '#RRGGBB', 'rgb': (R, G, B), 'percentage': 0.34}, ...]
        sorted by how much of the image each color covers, descending.

    """
    ct = ColorThief(image_path)
    palette = ct.get_palette(color_count=num_colors, quality=1)
    dominant = ct.get_color(quality=1)

    total_pixels = 200 * 200
    counts = [0] * len(palette)

    from PIL import Image
    image = Image.open(image_path).convert('RGB')
    image = image.resize((200, 200))
    pixels = list(image.getdata())

    for pixel in pixels:
        best_idx = 0
        best_dist = float('inf')
        for i, c in enumerate(palette):
            dist = (pixel[0] - c[0]) ** 2 + (pixel[1] - c[1]) ** 2 + (pixel[2] - c[2]) ** 2
            if dist < best_dist:
                best_dist = dist
                best_idx = i
        counts[best_idx] += 1

    result = []
    for i, c in enumerate(palette):
        r, g, b = c[0], c[1], c[2]
        hex_color = '#{:02x}{:02x}{:02x}'.format(r, g, b)
        percentage = counts[i] / total_pixels
        result.append({'hex': hex_color, 'rgb': (r, g, b), 'percentage': percentage})

    result.sort(key=lambda x: x['percentage'], reverse=True)
    return result
