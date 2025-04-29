import pandas as pd
import matplotlib.pyplot as plt

# 1. Les inn CSV-filen riktig (hopper over de to første radene)
df = pd.read_csv('data/analyses_results/frost_aggregated_stats_year.csv', skiprows=2)

# 2. Gi tydelige kolonnenavn
df = df.rename(columns={
    df.columns[0]: 'year',
    df.columns[1]: 'mean_air_temperature_mean',
    df.columns[2]: 'mean_air_temperature_median',
    df.columns[3]: 'mean_air_temperature_std',
    df.columns[4]: 'total_precipitation_mean',
    df.columns[5]: 'total_precipitation_median',
    df.columns[6]: 'total_precipitation_std',
    df.columns[7]: 'mean_wind_speed_mean',
    df.columns[8]: 'mean_wind_speed_median',
    df.columns[9]: 'mean_wind_speed_std'
})


# 3. Lager figur med 3 subplots horisontalt
fig, axes = plt.subplots(1, 3, figsize=(18, 6), sharey=False)

# -------------------------
# Gjennomsnitt
axes[0].plot(df['year'], df['mean_air_temperature_mean'], marker='o', label='Temperatur')
axes[0].plot(df['year'], df['total_precipitation_mean'], marker='o', label='Nedbør')
axes[0].plot(df['year'], df['mean_wind_speed_mean'], marker='o', label='Vind')
axes[0].set_title('Gjennomsnitt')
axes[0].set_xlabel('År')
axes[0].set_ylabel('Verdi')
axes[0].grid(True, linestyle='--')
axes[0].legend()

# -------------------------
# Median
axes[1].plot(df['year'], df['mean_air_temperature_median'], marker='o', label='Temperatur')
axes[1].plot(df['year'], df['total_precipitation_median'], marker='o', label='Nedbør')
axes[1].plot(df['year'], df['mean_wind_speed_median'], marker='o', label='Vind')
axes[1].set_title('Median')
axes[1].set_xlabel('År')
axes[1].grid(True, linestyle='--')
axes[1].legend()

# -------------------------
# Standardavvik
axes[2].plot(df['year'], df['mean_air_temperature_std'], marker='o', label='Temperatur')
axes[2].plot(df['year'], df['total_precipitation_std'], marker='o', label='Nedbør')
axes[2].plot(df['year'], df['mean_wind_speed_std'], marker='o', label='Vind')
axes[2].set_title('Standardavvik')
axes[2].set_xlabel('År')
axes[2].grid(True, linestyle='--')
axes[2].legend()

# -------------------------
# Layout
plt.tight_layout()
plt.show()
