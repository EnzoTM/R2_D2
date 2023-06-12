import os

path = "/home/enzo/Desktop/data/porte.v1i.yolov8"

files = ["train", "test", "valid"]

new_class = "0"

for file in files:
    full_path = os.path.join(path, file, "labels")       

    for label in os.listdir(full_path):
        with open(os.path.join(full_path, label), 'r') as f:
            texts = f.read()

            for text in texts.split("\n"):
                if text != "":
                    text_modificado = text.replace(text[0], new_class, 1)

                    with open(os.path.join(full_path, label), 'w') as f2:
                        f2.write(text_modificado)