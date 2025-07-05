from django.shortcuts import render
from django.core.files.storage import default_storage
from tensorflow.keras.models import load_model # type: ignore
from tensorflow.keras.preprocessing.image import load_img, img_to_array # type: ignore
import numpy as np
import os

# Load your trained model
model = load_model('my_prj/space_object_classifier.h5')

def classify_image(image_path):
    img = load_img(image_path, target_size=(150, 150))
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0

    prediction = model.predict(img_array)
    class_index = np.argmax(prediction)
    class_labels = ['stars', 'planets', 'galaxies']
    
    return class_labels[class_index], prediction

def index(request):
    if request.method == 'POST' and request.FILES.get('imageFile'):
        image = request.FILES['imageFile']
        image_path = default_storage.save(os.path.join('uploads', image.name), image)
        classification, prediction = classify_image(default_storage.path(image_path))
        context = {
            'image_url': default_storage.url(image_path),
            'classification': classification,
            'prediction': prediction
        }
        return render(request, 'index.html', context)
    return render(request, 'index.html')


def home(request):
    return render(request, 'home.html')