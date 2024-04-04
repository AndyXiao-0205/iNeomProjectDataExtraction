import pandas as pd
from collections import Counter
from docx import Document

# The provided data appears to be a list of clinical data types collected.
# This is a simulation of the provided data based on the visible items in the image.
# In a real-world scenario, we would parse this data from a structured file.
clinical_data = [
    "ECG, CI",
    "ECG, HR",
    "EEG, Video of infants",
    "EEG",
    "HR, SpO2",
    "HR, RR, SpO2",
    "BLOOD PERFUSION INDEXES and HEMOGLOBIN",
    "Video of infants",
    "ECG",
    "image of infants",
    "thermal imaging of infants",
    "thermal imaging",
    "SpO2",
    "EEG",
    "HR, SpO2, StO2",
    "ECG",
    "ECG, HR",
    "BP, HR, PR, GA",
    "ICP",
    "HR, SpO2, PIA",
    "bowel sound",
    "HR, GA",
    "Not mentioned",
    "Bowel sounds captured with differential microphone",
    "skin image",
    "EEG",
    "SpO2, RR",
    "RR",
    "vital signs, hospital records, fluid information, laboratory tests, treatment orders, and free-text medical records",
    "HR, SpO2",
    "Chest Sound",
    "Video of infants",
    "HR",
    "ECG, HR, RR, SpO2",
    "video of infants",
    "Chest sound",
    "HR, RR, FiO2, and SpO2",
    "video of infants",
    "video of infants",
    "video of infants",
    "HR, RR, SpO2"
]

# Splitting the combined data types and counting each unique type
data_types = [item.strip() for sublist in [x.split(',') for x in clinical_data] for item in sublist]
data_type_counts = Counter(data_types)

# Creating a DataFrame from the Counter object
df_data_types = pd.DataFrame(data_type_counts.items(), columns=['Clinical Data Type', 'Count'])

# Display the DataFrame sorted by the most common data types
df_data_types_sorted = df_data_types.sort_values(by='Count', ascending=False).reset_index(drop=True)
df_data_types_sorted.to_excel('clinical_data_types.xlsx', index=False)
