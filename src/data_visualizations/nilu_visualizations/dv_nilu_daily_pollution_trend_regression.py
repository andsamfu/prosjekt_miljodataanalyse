import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def show_regretion(json_path):
    """
    Visualiserer daglig utvikling i luftforurensningsnivåer (NO2, PM10, PM2.5) 
    ved hjelp av regresjonsplot.

    Args:
        json_path (str): Filsti til JSON-filen som inneholder NILU-data.
    """
    # Les inn NILU-data og konverter datoer
    df = pd.read_json(json_path)
    df['dateTime'] = pd.to_datetime(df['dateTime'])

    # Luftkomponenter som skal analyseres
    components = ['NO2', 'PM10', 'PM2.5']
    titles = {
        'NO2': "Utvikling i NO2-nivåer (daglig)",
        'PM10': "Utvikling i PM10-nivåer (daglig)",
        'PM2.5': "Utvikling i PM2.5-nivåer (daglig)"
    }

    # Opprett figur med tre delplott
    sns.set(style="whitegrid")
    fig, axes = plt.subplots(3, 1, figsize=(14, 12), sharex=True)
    fig.subplots_adjust(hspace=0.4)

    for i, comp in enumerate(components):
        # Filtrer data og konverter datoer til numeriske verdier
        data = df[['dateTime', comp]].dropna()
        data['x_temp'] = (data['dateTime'] - data['dateTime'].min()).dt.days

        # Lag regresjonsplot
        sns.regplot(
            data=data,
            x='x_temp',
            y=comp,
            ax=axes[i],
            scatter_kws={"s": 12, "alpha": 0.6},
            line_kws={"color": "crimson"}
        )

        # Tilpass x-aksen med datoetiketter
        tick_step = max(1, int(len(data) / 8))
        tick_pos = data['x_temp'][::tick_step]
        tick_labels = data['dateTime'][::tick_step].dt.strftime('%b %Y')
        axes[i].set_xticks(tick_pos)
        axes[i].set_xticklabels(tick_labels, rotation=45)

        # Legg til tittel og y-akse etikett
        axes[i].set_title(titles[comp], fontsize=13)
        axes[i].set_ylabel(f"{comp} (µg/m³)")

    # Legg til hovedtittel og juster layout
    plt.suptitle(
        "Daglig utvikling i luftforurensningsnivåer med regresjonsmodell (NILU)",
        fontsize=15, y=0.95
    )
    plt.tight_layout(rect=[0, 0, 1, 0.94])
    plt.show()
