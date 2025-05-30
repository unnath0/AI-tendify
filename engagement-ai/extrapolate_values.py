import os
import shutil

# Paths
images_dir = "dataset/images"
labels_dir = "dataset/labels"

# Get sorted list of image filenames (no extension)
image_files = sorted(
    [
        os.path.splitext(f)[0]
        for f in os.listdir(images_dir)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ]
)

# Get set of labeled image names
labeled_images = set(
    [os.path.splitext(f)[0] for f in os.listdir(labels_dir) if f.endswith(".txt")]
)

last_label = None

for image in image_files:
    label_path = os.path.join(labels_dir, image + ".txt")

    if image in labeled_images:
        last_label = image  # Update the last known label
    else:
        if last_label:
            src_label = os.path.join(labels_dir, last_label + ".txt")
            shutil.copy(src_label, label_path)
            print(f"Copied label from {last_label} to {image}")
        else:
            print(f"No previous label found for {image}, skipping.")

print("Extrapolation complete.")
