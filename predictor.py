import joblib
import pandas as pd

model = joblib.load("party_predictor.pkl")
enc = joblib.load("party_encoder.pkl")

new_person = pd.DataFrame([{
    "Q1": "A",
    "Q2": "D",
    "Q3": "A",
    "Q4": "C",
    "Q5": "D",
    "Q6": "B",
    "Q7": "A",
    "Q8": "C",
    "Q9": "B",
    "Q10": "D"
}])

for col in new_person.columns:
    new_person[col] = new_person[col].map({'A':0,'B':1,'C':2,'D':3})

prediction = model.predict(new_person)[0]
party = enc.inverse_transform([prediction])[0]

print("Predicted Party:", party)