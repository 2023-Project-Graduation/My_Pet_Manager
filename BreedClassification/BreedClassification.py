import cv2
from PIL import Image
import os, glob, numpy as np
from keras.models import load_model
from imutils import paths

def main():
    test_image_paths = sorted(
        list(
            paths.list_images("./img/")
        )
    )
    print(test_image_paths)
    
    model = load_model('models/Classification_Model.h5',compile=False)
    class_labels = ["other_dogs",'retriever','samoyed','yorkshire_terrier']

    for image_path in test_image_paths:
        test_image = cv2.imread(image_path)

        test_image = cv2.resize(
            test_image, (64,64)
        )

        test_image = test_image.astype("float") / 255.0
        test_image = np.expand_dims(test_image, axis=0)

        proba = model.predict(test_image)[0]
        print(np.round(proba, 3))
        idx = np.argmax(proba)
        Breed_label = class_labels[idx]
        print(Breed_label, np.max(proba))
        return Breed_label

if __name__ == "__main__":
    main()
