import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder

# Load your dataset
df = pd.read_csv("survey_1000_users.csv")

# Encode A/B/C/D → numbers
for col in df.columns[:-1]:
    df[col] = df[col].map({'A':0, 'B':1, 'C':2, 'D':3})

# Encode parties
party_encoder = LabelEncoder()
df['Party'] = party_encoder.fit_transform(df['Party'])

X = df.drop("Party", axis=1)
y = df["Party"]

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestClassifier(n_estimators=300, random_state=42)
model.fit(X_train, y_train)

# Evaluate
pred = model.predict(X_test)
print(classification_report(y_test, pred, target_names=party_encoder.classes_))

# Save model
import joblib
joblib.dump(model, "party_predictor.pkl")
joblib.dump(party_encoder, "party_encoder.pkl")