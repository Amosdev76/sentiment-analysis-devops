
import pickle

MODEL_PATH = "app/model/sentiment_analysis_model.pkl"

print("Caricamento del modello...")

with open(MODEL_PATH, "rb") as file:
    model = pickle.load(file)

print("Modello caricato correttamente.")
print()

print("Tipo del modello:")
print(type(model))

print()
print("Classi del modello:")
print(model.classes_)

print()
print("Test delle predizioni:")

reviews = [
    "This product is amazing! I love it.",
    "This product is terrible. I hate it.",
    "The product is okay, nothing special."
]

predictions = model.predict(reviews)

print()
for review, prediction in zip(reviews, predictions):
    print("Recensione:", review)
    print("Predizione:", prediction)
    print()