from os.path import dirname, abspath, join
from PIL import Image
import numpy as np


ROOT = dirname(abspath(dirname(__file__)))
GRADIENT = [
    (0.0, "#ffffff"),   # sombras
    (0.3, "#6F8A83"),   # tonos oscuros-medios
    (0.6, "#404443"),   # medios
    (1.0, "#161616"),   # luces
]


def hex_to_rgb(hex_color: str):
    hex_color = hex_color.lstrip("#")
    if len(hex_color) != 6:
        raise ValueError(f"Color inválido: {hex_color}")
    return np.array([
        int(hex_color[0:2], 16),
        int(hex_color[2:4], 16),
        int(hex_color[4:6], 16)
    ], dtype=np.float32)


def build_gradient_lut(stops, size=256):
    stops = sorted(stops, key=lambda x: x[0])

    positions = [p for p, _ in stops]
    colors = [hex_to_rgb(c) for _, c in stops]

    lut = np.zeros((size, 3), dtype=np.float32)

    for i in range(len(stops) - 1):
        p0, c0 = positions[i], colors[i]
        p1, c1 = positions[i + 1], colors[i + 1]

        start = int(round(p0 * (size - 1)))
        end = int(round(p1 * (size - 1)))

        if end == start:
            lut[start] = c1
            continue

        for j in range(start, end + 1):
            t = (j - start) / (end - start)
            lut[j] = (1 - t) * c0 + t * c1

    first_idx = int(round(positions[0] * (size - 1)))
    last_idx = int(round(positions[-1] * (size - 1)))

    lut[:first_idx] = colors[0]
    lut[last_idx:] = colors[-1]

    return np.clip(lut, 0, 255).astype(np.uint8)


def recolor_image(img, preserve_alpha=True):
    arr = np.array(img)

    rgb = arr[..., :3].astype(np.float32)
    alpha = arr[..., 3]

    luminance = 0.299 * rgb[..., 0] + 0.587 * rgb[..., 1] + 0.114 * rgb[..., 2]
    luminance = np.clip(luminance, 0, 255).astype(np.uint8)

    lut = build_gradient_lut(GRADIENT, size=256)

    recolored_rgb = lut[luminance]

    if preserve_alpha:
        result = np.dstack([recolored_rgb, alpha])
        out = Image.fromarray(result, mode="RGBA")
    else:
        out = Image.fromarray(recolored_rgb, mode="RGB")

    return out


def add_gaussian_noise(img, mean=0.0, std=25.0, preserve_alpha=True):
    arr = np.array(img)
    rgb = arr[..., :3]
    alpha = arr[..., 3]

    noise = np.random.normal(loc=mean, scale=std, size=rgb.shape).astype(np.float32)
    noisy_rgb = rgb + noise
    noisy_rgb = np.clip(noisy_rgb, 0, 255).astype(np.uint8)

    if preserve_alpha:
        result = np.dstack([noisy_rgb, alpha.astype(np.uint8)])
        return Image.fromarray(result, mode="RGBA")
    else:
        return Image.fromarray(noisy_rgb, mode="RGB")


def process_img(img):
    img = recolor_image(img)
    img = add_gaussian_noise(img)
    
    return img


def get_img(path):
    img = Image.open(path).convert("RGBA")
    return img


def main():
    imgs_path = join(ROOT, "input", "test.png")
    output_path = join(ROOT, "output", "output.png")
    img = get_img(imgs_path)
    processed_img = process_img(img)
    processed_img.save(output_path)
    


if __name__ == "__main__":
    main()