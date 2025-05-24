import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import json

def vis_no2_per_måned(json_path):
    # Laste inn renset NILU-data fra JSON
    with open(json_path, "r") as f:
        data = json.load(f)

    # Bygge DataFrame
    df = pd.DataFrame(data)
    df['dateTime'] = pd.to_datetime(df['dateTime'])

    # Legge til månedskolonne
    df['month'] = df['dateTime'].dt.strftime('%b')
    df['month_num'] = df['dateTime'].dt.month

    # Sortere for riktig månedrekkefølge
    df = df.sort_values('month_num')

    # Lage boxplot
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=df, x='month', y='NO2', palette='Blues', fliersize=3)
    plt.title("Boxplot av månedlige NO2-nivå (μg/m³)")
    plt.xlabel("Måned")
    plt.ylabel("NO2 (μg/m³)")
    plt.tight_layout()
    plt.show()