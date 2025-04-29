import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Lese inn korrelasjonsmatrise
corr_df = pd.read_csv('data/analyses_results/frost_correlation_matrix.csv', index_col=0)

# 2. Lage heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(corr_df, annot=True, cmap='OrRd', vmin=0, vmax=1, fmt='.2f', linewidths=0.5, linecolor='gray')
plt.title('Korrelasjon mellom temperatur, nedbør og vind')
plt.tight_layout()




plt.show()
