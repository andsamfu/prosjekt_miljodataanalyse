import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
def vis_korrelasjoner_sammen(frost_csv, nilu_csv):
    frost_df = pd.read_csv(frost_csv, index_col=0)
    nilu_df = pd.read_csv(nilu_csv, index_col=0)

    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    sns.heatmap(frost_df, annot=True, cmap='OrRd', vmin=0, vmax=1, fmt='.2f',
                linewidths=0.5, linecolor='gray', ax=axes[0])
    axes[0].set_title('Korrelasjon mellom temperatur, nedbør og vind')

    sns.heatmap(nilu_df, annot=True, cmap='OrRd', vmin=0, vmax=1, fmt='.2f', ax=axes[1])
    axes[1].set_title('Korrelasjon mellom NO2, PM10 og PM2.5')

    plt.tight_layout()
    plt.show()