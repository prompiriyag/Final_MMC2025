import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import argparse
import csv
import matplotlib

colors_rgb = {
    "เขียวอ่อนมาก":(76, 180, 0),
    "เขียวอ่อน":(49, 133, 0),
    "เขียวเข้ม":(68, 118, 0),
    "น้ำตาลเขียว":(127, 100, 0),
    "น้ำตาลเข้ม":(71, 40, 0),
    "เทาอ่อน":(76, 76, 76),
    "เทาเข้ม":(32, 32, 32),
    "ดำ":(0, 0, 0)
}

def closest_color_label(rgb):
    min_dist = float('inf')
    closest = None
    for label, color in colors_rgb.items():
        dist = np.linalg.norm(np.array(rgb) - np.array(color))
        if dist < min_dist:
            min_dist = dist
            closest = label
    return closest

def classify_grid(image_array, grid_size):
    h, w, _ = image_array.shape
    grid_map = np.empty((grid_size, grid_size), dtype=object)
    color_count = {label: 0 for label in colors_rgb.keys()}

    for i in range(grid_size):
        for j in range(grid_size):
            y1 = round(i * h / grid_size)
            y2 = round((i + 1) * h / grid_size)
            x1 = round(j * w / grid_size)
            x2 = round((j + 1) * w / grid_size)

            cell = image_array[y1:y2, x1:x2]
            avg_rgb = np.mean(cell.reshape(-1, 3), axis=0)
            label = closest_color_label(avg_rgb)
            grid_map[i, j] = label
            color_count[label] += 1

    return grid_map, color_count

def plot_result(grid_map, output_name):
    label_to_color = {label: np.array(rgb) / 255.0 for label, rgb in colors_rgb.items()}
    h, w = grid_map.shape
    color_image = np.zeros((h, w, 3))

    for i in range(h):
        for j in range(w):
            color_image[i, j] = label_to_color[grid_map[i, j]]

    plt.figure(figsize=(6, 6))
    plt.imshow(color_image)
    plt.axis('off')
    plt.savefig(output_name)
    plt.show()

def save_csv(grid_map, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(grid_map)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--image', type=str, required=True)
    parser.add_argument('--grid', type=int, default=30)
    args = parser.parse_args()

    image = Image.open(args.image).convert('RGB')
    image_array = np.array(image)

    grid_map, color_count = classify_grid(image_array, args.grid)

    save_csv(grid_map, 'color_grid.csv')
    plot_result(grid_map, 'color_grid_plot.png')

    print("✅ ผลลัพธ์:")
    total = sum(color_count.values())
    for label, count in color_count.items():
        print(f"{label}: {count} ช่อง ({count / total:.2%})")

if __name__ == '__main__':
    main()