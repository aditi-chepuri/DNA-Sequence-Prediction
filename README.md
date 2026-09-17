# 🧬 DNA Sequence Prediction using NLP and Machine Learning

A machine learning web application that analyzes DNA sequences and predicts the **species** and **genetic class** associated with a given DNA sequence.

The project applies **Natural Language Processing (NLP)** techniques such as **k-mer extraction** and **TF-IDF vectorization**, followed by **Random Forest classification** to perform DNA sequence prediction.

🌐 **Live Demo:** https://dna-sequence-prediction.onrender.com/

---

## 📌 Project Overview

DNA sequences are biological sequences represented using four nucleotide bases:

* **A** – Adenine
* **T** – Thymine
* **G** – Guanine
* **C** – Cytosine

This project treats DNA sequences similarly to text data by breaking them into smaller subsequences called **k-mers**.

The extracted k-mers are converted into numerical features using **TF-IDF vectorization**. These features are then provided to machine learning models to predict the species and class associated with the DNA sequence.

The application provides a simple web interface where users can enter a DNA sequence and receive a prediction.

---

## 🎯 Objectives

* Analyze DNA sequences using machine learning techniques.
* Apply NLP concepts to biological sequence data.
* Extract k-mer features from DNA sequences.
* Convert DNA sequence features into numerical representations using TF-IDF.
* Predict the species associated with a DNA sequence.
* Predict the genetic class associated with the predicted species.
* Provide an easy-to-use web interface.
* Deploy the machine learning application online.

---

## 🔬 How the Project Works

The complete workflow is:

```text
DNA Sequence
      ↓
K-mer Extraction
      ↓
TF-IDF Vectorization
      ↓
Species Classification
      ↓
Predicted Species
      ↓
Species-specific Classification
      ↓
Predicted Class
      ↓
Result Display
```

---

## 🧪 K-mer Extraction

A DNA sequence is divided into overlapping subsequences called **k-mers**.

In this project:

```text
k = 5
```

For example:

```text
DNA Sequence:
ATGCGATC

5-mers:
ATGCG
TGCGA
GCGAT
CGATC
```

These k-mers are treated as textual features for the NLP pipeline.

---

## 📊 TF-IDF Vectorization

The extracted k-mers are converted into numerical feature vectors using **TF-IDF (Term Frequency-Inverse Document Frequency)**.

TF-IDF helps represent the importance of k-mer features within the DNA sequence dataset.

The resulting numerical vectors are used as input to the machine learning classifiers.

---

## 🤖 Machine Learning Model

The project uses **Random Forest Classifiers** for prediction.

### Species Classification

The first model predicts the species from the DNA sequence.

The project currently includes:

* Human
* Dog
* Chimp

### Class Classification

After the species is predicted, the corresponding species-specific classifier is used to predict the class.

```text
DNA Sequence
      ↓
Species Classifier
      ↓
Human / Dog / Chimp
      ↓
Species-specific Classifier
      ↓
Class Prediction
```

---

## 🧠 Class Interpretation

The application provides an interpretation for the predicted class:

| Class | Interpretation                              |
| ----- | ------------------------------------------- |
| 0     | Non-coding DNA / Introns                    |
| 1     | Protein-coding genes / Regulatory sequences |
| 2     | Housekeeping genes / Essential functions    |
| 3     | Enzyme-coding genes / Metabolism-related    |
| 4     | Structural genes / Cell structure proteins  |
| 5     | Immune system genes                         |
| 6     | Transcription factors / Gene regulation     |

---

## 🖥️ Application Features

### 🏠 Home Page

Provides an introduction to the DNA Sequence Prediction application.

### 🔐 Login

A login page is provided before accessing the prediction functionality.

### 🧬 DNA Sequence Prediction

Users can enter a DNA sequence and submit it for prediction.

### 📊 Prediction Result

The result page displays:

* Predicted species
* Predicted class
* Class interpretation

### 📈 Charts

The application also contains a charts section for data visualization.

---

## 🛠️ Technologies Used

| Technology    | Purpose                          |
| ------------- | -------------------------------- |
| Python        | Programming and machine learning |
| Flask         | Web application framework        |
| Pandas        | Dataset processing               |
| NumPy         | Numerical operations             |
| Scikit-learn  | Machine learning                 |
| TF-IDF        | Feature extraction               |
| Random Forest | Classification                   |
| HTML          | Web interface                    |
| CSS           | Styling                          |
| Gunicorn      | Production server                |
| Render        | Cloud deployment                 |
| Git           | Version control                  |
| GitHub        | Source code management           |

---

## 📂 Project Structure

```text
DNA-Sequence-Prediction/
│
├── app.py
├── DNA.csv
├── train_models.py
├── requirements.txt
├── .python-version
│
├── species_classifier.pkl
├── human_class_classifier.pkl
├── dog_class_classifier.pkl
├── chimp_class_classifier.pkl
├── tfidf_vectorizer.pkl
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── predict.html
│   ├── result.html
│   └── charts.html
│
├── static/
│   ├── css/
│   ├── img/
│   └── ...
│
└── README.md
```

---

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/aditi-chepuri/DNA-Sequence-Prediction.git
```

### 2. Navigate to the Project

```bash
cd DNA-Sequence-Prediction
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

For Windows:

```bash
venv\Scripts\activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the Application

```bash
python app.py
```

The application will run locally at:

```text
http://127.0.0.1:5001
```

---

## 📦 Requirements

The main Python dependencies used in the project include:

```text
Flask
Pandas
NumPy
Scikit-learn
Gunicorn
```

The exact versions are available in `requirements.txt`.

---

## ☁️ Deployment

The application is deployed using **Render**.

### Build Command

```bash
pip install -r requirements.txt
```

### Start Command

```bash
gunicorn app:app
```

### Python Version

The project uses Python 3.11, specified through:

```text
.python-version
```

### Live Application

🌐 **https://dna-sequence-prediction.onrender.com/**

---

## 💾 Trained Models

The project contains pre-trained machine learning models saved using Python Pickle.

```text
species_classifier.pkl
human_class_classifier.pkl
dog_class_classifier.pkl
chimp_class_classifier.pkl
tfidf_vectorizer.pkl
```

These models allow the deployed application to perform predictions without retraining the models every time a user submits a DNA sequence.

---

## 🔄 Model Training

The project includes a separate training script:

```text
train_models.py
```

The training process includes:

```text
DNA Dataset
     ↓
K-mer Extraction
     ↓
TF-IDF Vectorization
     ↓
Train/Test Split
     ↓
Random Forest Training
     ↓
Save Trained Models
```

The saved models are then loaded by the Flask application for prediction.

---

## 📚 Concepts Demonstrated

This project demonstrates practical implementation of:

* Natural Language Processing
* DNA sequence analysis
* K-mer extraction
* Feature engineering
* TF-IDF vectorization
* Random Forest classification
* Train-test splitting
* Model serialization
* Flask web development
* HTML/CSS
* Git & GitHub
* Cloud deployment
* Machine learning model integration

---

## 🔮 Future Enhancements

* Add more species to the dataset.
* Support larger DNA sequence datasets.
* Experiment with different k-mer sizes.
* Compare multiple machine learning algorithms.
* Improve model evaluation and validation.
* Add additional biological sequence analysis.
* Add interactive data visualizations.
* Improve authentication and user management.
* Provide more detailed biological interpretations.
* Develop an API for programmatic DNA predictions.

---

## 🔗 Project Links

**GitHub Repository:**
https://github.com/aditi-chepuri/DNA-Sequence-Prediction

**Live Demo:**
https://dna-sequence-prediction.onrender.com/

---

## 👩‍💻 Author

**Aditi Chepuri**

**Data Science Student | Python | Machine Learning | SQL | Web Development**

⭐ If you find this project useful, consider giving the repository a star!
