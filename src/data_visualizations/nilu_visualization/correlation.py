import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Les inn korrelasjonsmatrisen
corr_df = pd.read_csv('data/analyses_results/nilu_correlation_matrix.csv', index_col=0)

# 2. Lager en heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(corr_df, annot=True, cmap='OrRd', vmin=0, vmax=1, fmt='.2f')
plt.title('Korrelasjon mellom NO₂, PM10 og PM2.5')
plt.tight_layout()
plt.show()
