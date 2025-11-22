import joblib
import pandas as pd

model = joblib.load("party_predictor.pkl")
enc = joblib.load("party_encoder.pkl")


def predict_party(responses: dict) -> str:
    new_person = pd.DataFrame([responses])

    for col in new_person.columns:
        new_person[col] = new_person[col].map({'A':0,'B':1,'C':2,'D':3})

    prediction = model.predict(new_person)[0]
    party = enc.inverse_transform([prediction])[0]

    print("Predicted Party:", party)
    return party