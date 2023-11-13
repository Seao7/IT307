from django.shortcuts import render, HttpResponse
import os
import pickle
import pandas as pd
from django.conf import settings
import csv
from django.utils.html import escape

base_dir = settings.BASE_DIR
model_file_path = os.path.join(base_dir, 'app1/feature_selected_model.pkl')
model = pickle.load(open(model_file_path, 'rb'))

def predictor(request):
    if request.method == 'POST':
        # Get input values
        patient_name = request.POST['patient_name']
        cp = float(request.POST['cp'])
        oldpeak = float(request.POST['oldpeak'])
        thalach = float(request.POST['thalach'])
        thal = float(request.POST['thal'])
        exang = float(request.POST['exang'])
        ca = float(request.POST['ca'])
        fbs = float(request.POST['fbs'])
        sex = request.POST['sex']
        

        if sex == 'Male':
            sex = 1
        else:
            sex = 0

        data = pd.DataFrame({'cp': [cp], 'oldpeak': [oldpeak], 'thalach': [thalach],
                             'thal': [thal], 'exang': [exang], 'ca': [ca], 'sex': [sex], 'fbs': [fbs]})

    
        csv_file_path = os.path.join(base_dir, 'input_data.csv')
        data.to_csv(csv_file_path, index=False)
        y_pred = model.predict(data)

        

        with open(csv_file_path, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            csv_data = list(csv_reader)

        

        if y_pred[0] == 0:
            return render(request, 'main.html', {'result': 'You do not have heart disease', 'csv_content': csv_data, 'name': patient_name})
        elif y_pred[0] == 1:
            return render(request, 'main.html', {'result': 'You have heart disease, visit the nearest hospital', 'csv_content': csv_data, 'name': patient_name})

    return render(request, 'main.html')
