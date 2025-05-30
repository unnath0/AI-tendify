import os
import random
import shutil

# Paths
train_dir = "dataset/images/train"
val_dir = "dataset/images/val"

# Create val directory if not exists
os.makedirs(val_dir, exist_ok=True)

# List all image files
images = [
    f for f in os.listdir(train_dir) if f.lower().endswith((".png", ".jpg", ".jpeg"))
]

# Shuffle and split 20%
random.shuffle(images)
val_count = int(len(images) * 0.2)
val_images = images[:val_count]

# Move images
for img in val_images:
    src_path = os.path.join(train_dir, img)
    dst_path = os.path.join(val_dir, img)
    shutil.move(src_path, dst_path)

print(f"Moved {val_count} images to validation set.")
