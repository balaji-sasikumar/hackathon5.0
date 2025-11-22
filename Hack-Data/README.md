# Synthetic Data Generator
Overview

This project generates synthetic (fake) data for testing and development using Python.
It uses Faker for basic fake data and supports advanced synthetic data generation using:

SDV (Synthetic Data Vault)
CTGAN
https://generatedata.com/

You can use this setup to generate high-quality synthetic datasets without exposing real data.

Installation

Install the required packages:

pip install faker pandas
pip install sdv

# Usage
1. Basic Data Generation (Faker)
from faker import Faker
import pandas as pd
import random

fake = Faker('en_IN')

districts = ["Chennai", "Coimbatore", "Erode", "Salem"]
villages = ["Perumapalayam", "Mettupalayam", "Anjur"]

data = []
num_rows = 10

for _ in range(num_rows):
    row = {
        'Name': fake.name(),
        'Address': fake.address().replace("\n", ", "),
        'Mobile': fake.phone_number(),
        'Village': random.choice(villages),
        'Taluk': fake.city(),
        'District': random.choice(districts)
    }
    data.append(row)

df = pd.DataFrame(data)
print(df)

# Output
Can be saved as CSV
df.to_csv("synthetic_data.csv", index=False)