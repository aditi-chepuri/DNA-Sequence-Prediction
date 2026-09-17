import pickle
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer


def extract_kmers(sequence, k=5):
    kmers = [sequence[i:i+k] for i in range(len(sequence) - k + 1)]
    return ' '.join(kmers)


# Load dataset
df = pd.read_csv("DNA.csv")

# Extract k-mers
k = 5
df["kmers"] = df["sequence"].apply(lambda seq: extract_kmers(seq, k))

# TF-IDF
vectorizer = TfidfVectorizer(analyzer="word")
X = vectorizer.fit_transform(df["kmers"])

# Save vectorizer
with open("tfidf_vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

# Species classifier
X_train, X_test, y_train, y_test = train_test_split(
    X,
    df["species"],
    test_size=0.3,
    random_state=42
)

species_classifier = RandomForestClassifier(random_state=42)
species_classifier.fit(X_train, y_train)

with open("species_classifier.pkl", "wb") as f:
    pickle.dump(species_classifier, f)

# Class classifiers
for species in df["species"].unique():

    species_data = df[df["species"] == species]

    X_species = vectorizer.transform(species_data["kmers"])
    y_species = species_data["class"]

    X_train_species, X_test_species, y_train_species, y_test_species = train_test_split(
        X_species,
        y_species,
        test_size=0.3,
        random_state=42
    )

    class_classifier = RandomForestClassifier(random_state=42)
    class_classifier.fit(X_train_species, y_train_species)

    filename = f"{species.lower()}_class_classifier.pkl"

    with open(filename, "wb") as f:
        pickle.dump(class_classifier, f)

    print(f"Saved: {filename}")

print("All models recreated successfully!")