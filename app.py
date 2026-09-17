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
        # Function to extract k-mers from DNA sequence
    

        # Load the dataset
        df = pd.read_csv("DNA.csv")

        # Step 1: Preprocess the data (Convert DNA sequences into k-mer frequencies)
        k = 5  # You can experiment with different k values (e.g., 3, 4, 5, 6)
        df['kmers'] = df['sequence'].apply(lambda seq: extract_kmers(seq, k))

        # Step 2: TF-IDF Vectorization
        vectorizer = TfidfVectorizer(analyzer='word')
        X = vectorizer.fit_transform(df['kmers'])

        # Step 3: Train the first classifier to predict the species
        X_train, X_test, y_train, y_test = train_test_split(X, df['species'], test_size=0.3, random_state=42)

        # Trying RandomForestClassifier instead of Naive Bayes for species classification
        species_classifier = RandomForestClassifier(random_state=42)
        species_classifier.fit(X_train, y_train)

        # Make predictions and evaluate the species classifier
        species_predictions = species_classifier.predict(X_test)
        species_accuracy = accuracy_score(y_test, species_predictions)
        #print(f"Species Classifier Accuracy: {species_accuracy}")

        # Step 4: Train a separate classifier for each species to predict the class
        # Create dictionaries to store classifiers for each species
        classifiers = {}

        for species in df['species'].unique():
            # Filter the data for the current species
            species_data = df[df['species'] == species]
            X_species = vectorizer.transform(species_data['kmers'])
            y_species = species_data['class']
            
            # Split the data into train and test sets
            X_train_species, X_test_species, y_train_species, y_test_species = train_test_split(X_species, y_species, test_size=0.3, random_state=42)
            
            # Try Random Forest for class classification as well
            class_classifier = RandomForestClassifier(random_state=42)
            class_classifier.fit(X_train_species, y_train_species)
            
            # Store the classifier in the dictionary
            classifiers[species] = class_classifier
        # Get the DNA sequence from the form
        sequence = request.form['sequence']
        
        sequence_kmers = extract_kmers(sequence, k)
        sequence_vector = vectorizer.transform([sequence_kmers])
    
    # Predict the species first
        predicted_species = species_classifier.predict(sequence_vector)[0]
    
    # Predict the class within the predicted species
        class_classifier = classifiers[predicted_species]
        predicted_class = class_classifier.predict(sequence_vector)[0]
        if predicted_species:
            # Redirect to the result page with species and class prediction
            return redirect(url_for('result', species_prediction=predicted_species, class_prediction=predicted_class))
        else:
            # If the species is not recognized, show an error or default behavior
            return render_template('predict.html', prediction='Species prediction error')

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
