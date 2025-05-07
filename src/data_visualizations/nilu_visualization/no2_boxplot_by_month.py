import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import json

def vis_no2_boxplot_per_måned(json_path):
    # Leser inn renset NILU-data fra JSON
    with open(json_path, "r") as f:
        data = json.load(f)

    df = pd.DataFrame(data)
    df['dateTime'] = pd.to_datetime(df['dateTime'])

    if "NO2" not in df.columns:
        raise ValueError("NO2-kolonnen finnes ikke i data")

    # Legger til måned og sorterer
    df['month'] = df['dateTime'].dt.strftime('%b')
    df['month_num'] = df['dateTime'].dt.month
    df = df.sort_values('month_num')

    # Lager boxplot
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=df, x='month', y='NO2', palette='YlOrBr')
    plt.title("Boxplot av måndelige NO₂-nivå (μg/m³)")
    plt.xlabel("Month")
    plt.ylabel("NO₂ (μg/m³)")
    plt.tight_layout()
    plt.show()
