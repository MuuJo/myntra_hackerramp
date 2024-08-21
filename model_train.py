# train_model.py
import pathlib
import os
import pickle
import pandas as pd
import numpy as np
from tensorflow.keras.applications.mobilenet import MobileNet, preprocess_input
from tensorflow.keras.preprocessing import image

# Define the path to the images directory
image_dir = pathlib.Path('D:/OneDrive/Mukta_OneDrive/Mukta_exploration/Myntra_2024/Final/Database/static/images/model_images')

# Load the MobileNet model
mobilenet_model = MobileNet(weights='imagenet', include_top=False, pooling='avg')

# Function to get embeddings from images
def get_embeddings(image_dir, model, target_size=(128, 128)):
    embeddings = []
    image_paths = []
    
    for img_name in os.listdir(image_dir):
        img_path = image_dir / img_name
        image_paths.append(str(img_path))
        
        # Load and preprocess the image
        img = image.load_img(img_path, target_size=target_size)
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)
        
        # Get the embeddings from the model
        features = model.predict(img_array)
        embeddings.append(features.flatten())
    
    # Convert to DataFrame
    df_embeddings = pd.DataFrame(embeddings)
    df_embeddings['image_path'] = image_paths
    return df_embeddings

# Train the model and save the embeddings
df_embeddings = get_embeddings(image_dir, mobilenet_model)
with open('D:/OneDrive/Mukta_OneDrive/Mukta_exploration/Myntra_2024/Final/Database/embeddings.pkl', 'wb') as f:
    
    pickle.dump(df_embeddings,f)
