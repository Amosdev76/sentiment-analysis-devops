
import os
import pickle


MODEL_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "app",
    "model",
    "sentiment_analysis_model.pkl"
)


def load_model():
    with open(MODEL_PATH, "rb") as file:
        return pickle.load(file)


def test_model_loading():
    
    #Verifica che il modello venga caricato correttamente.
    

    model = load_model()

    assert model is not None


def test_model_prediction():
    
    #Verifica che il modello produca una delle tre
    #categorie di sentiment previste dal progetto.
    

    model = load_model()

    review = [
        "This product is amazing! I love it."
    ]

    prediction = model.predict(review)[0]

    assert prediction in [
        "positive",
        "negative",
        "neutral"
    ]


def test_model_probability():
    
    # Verifica che il modello produca una probabilità
    # associata alla predizione.
    

    model = load_model()

    review = [
        "This product is amazing! I love it."
    ]

    probabilities = model.predict_proba(review)[0]

    assert len(probabilities) == 3

    assert all(
        0 <= probability <= 1
        for probability in probabilities
    )