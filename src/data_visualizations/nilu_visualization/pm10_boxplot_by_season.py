import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import json

def vis_pm10_boxplot_per_sesong(json_path):
    # 1. Last inn NILU-data
    with open(json_path, "r") as f:
        data = json.load(f)

    # 2. Bygg DataFrame og konverter dato
    df = pd.DataFrame(data)
    df['dateTime'] = pd.to_datetime(df['dateTime'])

    # 3. Legg til sesong
    def month_to_season(month):
        if month in [12, 1, 2]: return "Winter"
        if month in [3, 4, 5]: return "Spring"
        if month in [6, 7, 8]: return "Summer"
        return "Fall"

    df['season'] = df['dateTime'].dt.month.apply(month_to_season)

    # 4. Sørg for riktig rekkefølge på sesonger
    season_order = ["Winter", "Spring", "Summer", "Fall"]
    df['season'] = pd.Categorical(df['season'], categories=season_order, ordered=True)

    # 5. Lag boxplot
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df, x='season', y='PM10', palette='Greens')
    plt.title("PM10-nivå per sesong")
    plt.xlabel("Sesong")
    plt.ylabel("PM10-nivå (μg/m³)")
    plt.tight_layout()
    plt.show()
