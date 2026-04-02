import pandas as pd

df = pd.read_csv("dataset/dataset.csv")

# Select important columns (edit based on your dataset)
important_cols = [
    "diseases",
    "fever",
    "cough",
    "fatigue",
    "headache",
    "nausea",
    "vomiting",
    "dizziness",
    "chest pain",
    "shortness of breath",
    "abdominal pain",
    "diarrhea",
    "weakness",
    "loss of appetite",
    "insomnia"
]

# Keep only available columns
important_cols = [col for col in important_cols if col in df.columns]

df_small = df[important_cols]

df_small.to_csv("dataset/small_dataset.csv", index=False)

print("✅ Reduced dataset saved")