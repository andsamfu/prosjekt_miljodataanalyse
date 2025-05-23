# 📁 data/ – Datamappe

Denne mappen inneholder datasett og analyseresultater brukt i prosjektet. Dataene er organisert i tre undermapper for å skille mellom rådata, rensede data og analyseresultater:

- `raw/` – ubehandlede data hentet fra eksterne kilder
- `clean/` – rensede og strukturerte data klare for analyse
- `analyses_results/` – statistiske analyser og aggregerte resultater

---

## 📁 raw/

Inneholder rådata fra Frost og NILU hentet via egne Python-skript som finnes i `src/data_collection`. Disse dataene brukes som utgangspunkt for all videre rensing, analyse og visualisering i prosjektet.

Eksempler:
- `api_frost_weather.json` – værdata fra Frost API
- `api_frost_weather.db` – samme data i SQLite-format
- `api_nilu_air_quality.json` – luftkvalitetsdata fra NILU

> 🔒 Merk: I prosjektet har vi valgt å legge `raw/`-mappen i `.gitignore` for å unngå store filer i versjonskontroll. Ved innlevering har vi likevel inkludert disse filene manuelt da filene må hentes med en API nøkkel.

---

## 📁 clean/

Her ligger de rensede datasettene som brukes videre i analyse og modellering:

- `cleaned_data_nilu.json` – NILU-data etter outlier-håndtering og KNN-imputasjon
- `frost.db` – Frost-data i strukturert SQLite-format etter filtrering og rensing

Rensingen er dokumentert med valg og metode i `01_data_cleaning.ipynb`. 

---

## 📁 analyses_results/

Inneholder output fra `src/data_analysis` filene, brukt til grafer, modeller og videre analyse.

**Frost:**
- `frost_aggregated_stats_year.csv`
- `frost_aggregated_stats_year_season.csv`
- `frost_correlation_matrix.csv`

**NILU:**
- `nilu_aggregated_stats_year.csv`
- `nilu_aggregated_stats_year_season.csv`
- `nilu_correlation_matrix.csv`

---

## 🔁 Versjonskontroll og `.gitignore`

Vi har valgt å bruke `.gitignore` på store og genererte datafiler, spesielt i `raw/` og `clean/`, for å unngå:
- Unødvendig store commits
- Duplikater og støy i Git-historikken

**Fordeler:**
- Raskere og renere Git-arbeidsflyt
- Mer fokus på kode og struktur

**Ulemper:**
- Data må gjenskapes lokalt for å kjøre prosjektet fullt ut

---

### [**Til samlesiden**](../docs/samleside.md)



