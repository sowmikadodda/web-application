import tensorflow as tf
import numpy as np
from PIL import Image
import cv2
import os

class ImageRecognizer:
    def __init__(self):
        # Load pre-trained MobileNetV2 model
        self.model = tf.keras.applications.MobileNetV2(
            weights='imagenet',
            include_top=True
        )
        
    def preprocess_image(self, image_path):
        """Preprocess image for model prediction"""
        try:
            # Load and resize image
            img = Image.open(image_path).convert('RGB')
            img = img.resize((224, 224))
            
            # Convert to array and normalize
            img_array = tf.keras.preprocessing.image.img_to_array(img)
            img_array = tf.expand_dims(img_array, 0)
            img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)
            
            return img_array
        except Exception as e:
            print(f"Error preprocessing image: {e}")
            return None
    
    def recognize_product(self, image_path):
        """Recognize product from image"""
        try:
            # Preprocess image
            processed_img = self.preprocess_image(image_path)
            if processed_img is None:
                return "Unknown Product"
            
            # Make prediction
            predictions = self.model.predict(processed_img)
            decoded_predictions = tf.keras.applications.mobilenet_v2.decode_predictions(predictions, top=3)[0]
            
            # Extract product category
            top_prediction = decoded_predictions[0]
            class_name = top_prediction[1].lower()
            confidence = top_prediction[2]
            
            # Map predictions to product categories
            product_name = self.map_to_product_category(class_name, confidence)
            
            return product_name
            
        except Exception as e:
            print(f"Error in image recognition: {e}")
            return "Unknown Product"
    
    def map_to_product_category(self, class_name, confidence):
        """Map AI predictions to searchable product categories"""
        
        # Phone/Mobile keywords
        phone_keywords = ['cellular_telephone', 'mobile_phone', 'smartphone', 'iphone', 'android']
        
        # Laptop/Computer keywords  
        laptop_keywords = ['laptop', 'notebook', 'computer', 'desktop', 'monitor', 'screen']
        
        # Camera keywords
        camera_keywords = ['camera', 'digital_camera', 'reflex_camera', 'polaroid', 'lens']
        
        # Watch keywords
        watch_keywords = ['watch', 'wristwatch', 'digital_watch', 'analog_clock']
        
        # Headphone keywords
        headphone_keywords = ['headphone', 'earphone', 'headset', 'earbud']
        
        # Check confidence threshold
        if confidence < 0.1:
            return "Unknown Product"
        
        # Match keywords to categories
        for keyword in phone_keywords:
            if keyword in class_name:
                return "Smartphone"
                
        for keyword in laptop_keywords:
            if keyword in class_name:
                return "Laptop"
                
        for keyword in camera_keywords:
            if keyword in class_name:
                return "Camera"
                
        for keyword in watch_keywords:
            if keyword in class_name:
                return "Smartwatch"
                
        for keyword in headphone_keywords:
            if keyword in class_name:
                return "Headphones"
        
        # Default fallback
        return class_name.replace('_', ' ').title()