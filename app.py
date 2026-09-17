import pickle
from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np



app = Flask(__name__)

# Load the saved models and vectorizer
with open('species_classifier.pkl', 'rb') as f:
    species_classifier = pickle.load(f)

# Load class-specific classifiers for each species
classifiers = {}
for species in ['human', 'dog', 'chimp']:  # List all species you have classifiers for
    with open(f'{species}_class_classifier.pkl', 'rb') as f:
        classifiers[species] = pickle.load(f)

# Load the TF-IDF vectorizer
with open('tfidf_vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'admin':
            return redirect(url_for('predict'))
        else:
            return render_template('login.html', error='Invalid Credentials')
    return render_template('login.html', error=None)





def extract_kmers(sequence, k=5):
        kmers = [sequence[i:i+k] for i in range(len(sequence) - k + 1)]
        return ' '.join(kmers)


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    prediction = None

    if request.method == 'POST':
        # Get the DNA sequence from the form
        sequence = request.form['sequence'].strip().upper()

        # Convert DNA sequence into k-mers
        k = 5
        sequence_kmers = extract_kmers(sequence, k)

        # Use the already-trained TF-IDF vectorizer
        sequence_vector = vectorizer.transform([sequence_kmers])

        # Predict the species using the already-trained species classifier
        predicted_species = species_classifier.predict(sequence_vector)[0]

        # Convert species name to lowercase because our dictionary
        # uses lowercase keys: human, dog, chimp
        predicted_species_key = str(predicted_species).lower()

        # Check that the corresponding classifier exists
        if predicted_species_key not in classifiers:
            return render_template(
                'predict.html',
                prediction='Species prediction error'
            )

        # Get the classifier for the predicted species
        class_classifier = classifiers[predicted_species_key]

        # Predict the class
        predicted_class = class_classifier.predict(sequence_vector)[0]

        # Redirect to result page
        return redirect(
            url_for(
                'result',
                species_prediction=predicted_species,
                class_prediction=str(predicted_class)
            )
        )

    return render_template('predict.html', prediction=prediction)


@app.route('/result')
def result():
    species_prediction = request.args.get('species_prediction')
    class_prediction = request.args.get('class_prediction')

    # Mapping class numbers to their interpretations
    class_interpretations = {
        "0": "Non-coding DNA / Introns",
        "1": "Protein-coding genes (Regulatory sequences)",
        "2": "Housekeeping genes (Essential functions)",
        "3": "Enzyme-coding genes (Metabolism-related)",
        "4": "Structural genes (Cell structure proteins)",
        "5": "Immune system genes",
        "6": "Transcription factors (Gene regulation)"
    }

    # Get the class interpretation based on prediction
    class_interpretation = class_interpretations.get(class_prediction, "Unknown class")

    # Set the background image based on the predicted species
    if species_prediction == 'Human':
        bg_image = '../static/img/human.jpg'
    elif species_prediction == 'Dog':
        bg_image = '../static/img/dog.jpg'
    elif species_prediction == 'Chimp':
        bg_image = '../static/img/chimp.jpg'
    else:
        bg_image = '../static/img/p5.jpg'  # Default image

    print("FINAL OUTPUT:", species_prediction, class_prediction, class_interpretation, bg_image)

    return render_template('result.html', 
                           species_prediction=species_prediction, 
                           class_prediction=class_prediction, 
                           class_interpretation=class_interpretation, 
                           bg_image=bg_image)

@app.route('/charts')
def charts():
    # This route can render charts if you have any data visualizations.
    return render_template('charts.html')

@app.route('/logout')
def logout():
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=5001)
