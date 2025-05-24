import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def vis_korrelasjon_nilu(csv_path):
    # 1. Leser inn korrelasjonsmatrise fra CSV
    corr_df = pd.read_csv(csv_path, index_col=0)

    # 2. Lager en heatmap
    plt.figure(figsize=(8, 6))
    sns.heatmap(corr_df, annot=True, cmap='OrRd', vmin=0, vmax=1, fmt='.2f')
    plt.title('Korrelasjon mellom NO₂, PM10 og PM2.5')
    plt.tight_layout()
    plt.show()
