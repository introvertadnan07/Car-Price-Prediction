from flask import Flask, render_template, request
from flask_cors import CORS, cross_origin
import pickle
import pandas as pd
import numpy as np

app = Flask(__name__)
CORS(app)

# Load the trained model
model = pickle.load(open('LinearRegressionModel.pkl', 'rb'))

# Load the car dataset
car = pd.read_csv('Cleaned Car.csv')

@app.route('/', methods=['GET'])
def index():
    companies = sorted(car['company'].unique())
    car_models = sorted(car['name'].unique())
    years = sorted(car['year'].unique(), reverse=True)
    fuel_types = car['fuel_type'].unique()

    return render_template('index.html',
                           companies=companies,
                           car_models=car_models,
                           years=years,
                           fuel_types=fuel_types)

@app.route('/predict', methods=['POST'])
@cross_origin()
def predict():
    company = request.form.get('company')
    car_model = request.form.get('car_model')
    year = int(request.form.get('year'))
    fuel_type = request.form.get('fuel_type')
    kms_driven = float(request.form.get('kilo_driven'))

    # Prepare input for prediction
    input_df = pd.DataFrame(columns=['name', 'company', 'year', 'kms_driven', 'fuel_type'],
                            data=np.array([car_model, company, year, kms_driven, fuel_type]).reshape(1, 5))
    
    prediction = model.predict(input_df)
    
    return str(round(prediction[0], 2))

if __name__ == '__main__':
    app.run(debug=True)
