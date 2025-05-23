# 🧠 src/ – Kildekode

Denne mappen inneholder all prosjektlogikk og funksjonell Python-kode, organisert i moduler etter formål. Ved å samle koden i `src/` holder vi Jupyter-notebookene rene og fokuserte på dokumentasjon, mens all logikk og behandling skjer i importerbare `.py`-filer.

---

## ✅ Hvorfor bruke `src/`?

Å skille ut koden i egne moduler gir flere fordeler:

-  **Gjenbruk:** Funksjoner kan enkelt gjenbrukes i flere notebooks og scripts.
-  **Testbarhet:** Koden kan testes separat uten å kjøre hele notebooken.
-  **Oversikt:** Hver modul har et tydelig ansvar, og det blir lettere å finne frem.
-  **Skalerbarhet:** Prosjektet kan vokse uten at notebookene blir uoversiktlige.
-  **Lesbarhet:** Notebookene viser kun hva som gjøres, ikke *hvordan* det gjøres.

---

## 📁 Mappestruktur og innhold

### `data_collection/`
Kode for innhenting og strukturering av rådata fra eksterne API-er:

- `data_collection_frost_weather.py` – henter og lagrer værdata fra Frost API
- `data_collection_nilu_air_quality.py` – henter luftkvalitetsdata fra NILU API


### `data_cleaning/`
Moduler for rensing og kvalitetskontroll av rådata:

- `data_cleaning_frost.py` – filtrering og standardisering av Frost-data
- `data_cleaning_nilu.py` – rensing og KNN-imputasjon av NILU-data
- `data_validators.py` – verktøy for å oppdage outliers, manglende verdier og datohull


### `data_analysis/`
Moduler som utfører statistiske analyser og aggregerer data:

- `data_analysis_frost.py` – beregner årlige og sesongvise værstatistikker
- `data_analysis_nilu.py` – analyserer luftkvalitetsdata over tid


### `data_visualizations/`
Kode for å generere visualiseringer brukt i analyse og rapport:

- `frost_visualization/` – grafer, boxplots og interaktive figurer for værdata
- `nilu_visualization/` – visualisering av luftkomponenter
- `frost_vs_nilu_visualization/` – sammenligninger på tvers av datakilder
- `dataframes.py` – funksjoner for visualisering av dataframes

---

### `predictive_analysis/`
Alt som handler om prediktive modeller og visuell fremstilling av fremtidsscenarier:

- `data_prediction_frost.py` – temperaturmodell basert på sesongvariasjon
- `data_prediction_nilu.py` – enkel trendmodell for luftforurensning

---

## 🧪 Bruk i notebooks

Modulene i `src/` brukes direkte i prosjektets notebooks, f.eks.:

```python
from data_cleaning.data_cleaning_nilu import load_and_clean_data_nilu
from data_visualizations.frost_visualization.temperature_boxplot import plot_temperature_distribution
```

---

### [**Til samlesiden**](../docs/samleside.md)
