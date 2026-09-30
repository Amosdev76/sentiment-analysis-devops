
from flask import Flask, request, jsonify
import pickle
import os
import time

from prometheus_client import (
    Counter,
    Histogram,
    Gauge,
    generate_latest,
    CONTENT_TYPE_LATEST
)

import psutil


# Creazione dell'applicazione Flask
app = Flask(__name__)


# Percorso del modello
MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "model",
    "sentiment_analysis_model.pkl"
)


# Caricamento del modello
with open(MODEL_PATH, "rb") as file:
    model = pickle.load(file)




# ==============================
# Metriche Prometheus
# ==============================

# Numero totale delle richieste di predizione
prediction_counter = Counter(
    "prediction_requests_total",
    "Numero totale delle richieste di predizione"
)

# Numero totale degli errori
error_counter = Counter(
    "prediction_errors_total",
    "Numero totale degli errori di predizione"
)

# Tempo di risposta
response_time = Histogram(
    "prediction_response_time_seconds",
    "Tempo di risposta delle richieste di predizione"
)

# Utilizzo CPU
cpu_usage = Gauge(
    "system_cpu_usage_percent",
    "Utilizzo percentuale della CPU"
)

# Utilizzo memoria
memory_usage = Gauge(
    "system_memory_usage_percent",
    "Utilizzo percentuale della memoria"
)


# ==============================
# Endpoint /predict
# ==============================

@app.route("/predict", methods=["POST"])
def predict():

    start_time = time.time()

    prediction_counter.inc()

    try:

        # Recuperiamo i dati JSON
        data = request.get_json()

        # Verifichiamo che sia presente il campo review
        if not data or "review" not in data:
            error_counter.inc()

            return jsonify({
                "error": "Il campo 'review' è obbligatorio"
            }), 400


        review = data["review"]


        # Verifica che review sia una stringa
        if not isinstance(review, str):
            error_counter.inc()

            return jsonify({
                "error": "Il campo 'review' deve essere una stringa"
            }), 400


        # Predizione
        prediction = model.predict([review])[0]


        # Probabilità delle classi
        probabilities = model.predict_proba([review])[0]


        # Individuiamo la probabilità associata alla classe prevista
        predicted_index = list(model.classes_).index(prediction)

        confidence = probabilities[predicted_index]


        # Tempo di risposta
        elapsed_time = time.time() - start_time

        response_time.observe(elapsed_time)


        return jsonify({
            "sentiment": prediction,
            "confidence": round(float(confidence), 4)
        })


    except Exception as e:

        error_counter.inc()

        return jsonify({
            "error": str(e)
        }), 500


# ==============================
# Endpoint /metrics
# ==============================


@app.route("/metrics", methods=["GET"])
def metrics():

    # Lettura utilizzo CPU
    cpu = psutil.cpu_percent(interval=0.1)

    # Lettura utilizzo memoria
    memory = psutil.virtual_memory().percent

    # Aggiornamento metriche Prometheus
    cpu_usage.set(cpu)
    memory_usage.set(memory)

    return generate_latest(), 200, {
        "Content-Type": CONTENT_TYPE_LATEST
    }



# ==============================
# Endpoint di controllo
# ==============================

@app.route("/", methods=["GET"])
def home():

    return jsonify({
        "service": "Sentiment Analysis API",
        "status": "running"
    })


# ==============================
# Avvio dell'applicazione
# ==============================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )