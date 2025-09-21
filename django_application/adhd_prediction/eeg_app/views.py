import os
import numpy as np
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
import tensorflow as tf

# Load the model once when the server starts
model_path = os.path.join(settings.BASE_DIR, 'eeg_app', 'model', 'adhd_eeg_model.h5')
try:
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at: {model_path}")
    model = tf.keras.models.load_model(model_path)
except Exception as e:
    print(f"Error loading model: {str(e)}")
    model = None  # Set to None to handle gracefully in predict_adhd

def eeg_input(request):
    return render(request, 'eeg_input.html')

def predict_adhd(request):
    if request.method == 'POST':
        if model is None:
            return JsonResponse({'error': 'Model failed to load. Please check server configuration.'}, status=500)
        try:
            # Get EEG values from form
            eeg_values = [
                float(request.POST.get('Fp1', 0)),
                float(request.POST.get('Fp2', 0)),
                float(request.POST.get('F7', 0)),
                float(request.POST.get('F3', 0)),
                float(request.POST.get('Fz', 0)),
                float(request.POST.get('F4', 0)),
                float(request.POST.get('F8', 0)),
                float(request.POST.get('T3', 0)),
                float(request.POST.get('C3', 0)),
                float(request.POST.get('Cz', 0)),
                float(request.POST.get('C4', 0)),
                float(request.POST.get('T4', 0)),
                float(request.POST.get('T5', 0)),
                float(request.POST.get('P3', 0)),
                float(request.POST.get('Pz', 0)),
                float(request.POST.get('P4', 0)),
                float(request.POST.get('T6', 0)),
                float(request.POST.get('O1', 0)),
                float(request.POST.get('O2', 0)),
            ]
            # Prepare input for model (reshape to [1, 1, 19] to match expected shape)
            input_data = np.array(eeg_values).reshape(1, 1, 19)
            # Make prediction
            prediction = model.predict(input_data)
            prob = float(prediction[0][0])  # Assuming binary classification
            result = "Likely has ADHD" if prob > 0.5 else "Likely does not have ADHD"
            confidence = prob * 100 if prob > 0.5 else (1 - prob) * 100
            return JsonResponse({
                'result': result,
                'confidence': round(confidence, 2)
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=400)