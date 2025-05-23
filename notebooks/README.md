# 📓 notebooks/ – Jupyter Notebooks

Denne mappen inneholder alle hovednotebookene som dokumenterer prosjektets utvikling fra start til slutt. Hver notebook representerer ett trinn i prosjektet, og notebookene er navngitt og nummerert i kronologisk rekkefølge for å gjøre navigasjon og forståelse enklere.

---

## 📚 Hvorfor Jupyter Notebooks?

Vi har valgt å bruke Jupyter Notebooks fordi det gir en god balanse mellom **kode, dokumentasjon og visualisering** i ett og samme format. Dette gjør det enklere å:
- Dokumentere valg og metodebruk underveis
- Forklare og vise resultater med visualiseringer
- Strukturere prosjektet pedagogisk og reproduserbart
- Skille ulike faser (henting, rensing, analyse, modellering) uten å lage uoversiktlig kode

---

## 💡 Strukturelle valg

For å gjøre notebookene mest mulig oversiktlige og ryddige har vi valgt å:
- Holde logikken ute av notebookene, og heller definere all funksjonalitet i `.py`-moduler i `src/`
- Importere funksjoner og konstanter i toppen av hver notebook, slik at man får en tydelig og samlet oversikt over hva som brukes
- Skrive notebookene som dokumentasjonsfiler med visualiseringer og forklaringer, ikke som utviklingsmiljø

Dette gjør at hver notebook starter med en kort importblokk, som kan oppdateres raskt og gir god kontroll på avhengigheter.

---

## 📓 Notebook-oversikt

### `00_project_setup.ipynb` – Datastruktur og innhenting
- Dokumenterer prosjektets struktur og oppsett.
- Beskriver kildene vi har valgt og hvorfor

### `01_data_cleaning.ipynb` – Datarensing og strukturering
- Forklarer hvordan rådataene renses og standardiseres.
- Bruker egne rensingsfunksjoner fra `src/data_cleaning/`.
- Viser hvordan ulike strategier brukes for Frost og NILU.
- Reflekterer over valg som er tatt og hvorfor noen teknikker er brukt.

### `02_data_analysis_and_visualisation.ipynb` – Statistisk analyse
- Presentere oppbygningen til datasettet
- Interaktive visualiseringer av hele datasettene
- Andre visualiseringer som boxplots, histogram, scatterplots og korrelasjonsmatrise

### `03_predictive_analysis.ipynb` – Prediktiv modellering
- Bygger modeller for temperatur og luftkvalitet ved hjelp av lineær regresjon.
- Temperaturmodellen tar hensyn til sesongvariasjon via sin/cos-komponenter.
- Luftkvalitet modelleres med enkel trendbasert regresjon.
- Visualiserer og diskuterer begrensninger og nytte.

### `KNN_imputation.ipynb` – Utfyllende om KNN
- Undersøker effekten av ulike imputasjonsmetoder.
- Viser hvorfor KNN ble valgt fremfor enklere metoder.
- Inneholder visualiseringer av verdier før og etter imputasjon.
- Reflekterer kritisk rundt svakheter i modellen.

---

## 🧭 Bruk og avhengigheter

- Notebookene er laget for å kjøres i rekkefølge, men kan også kjøres separat.
- Koden i notebookene er begrenset til funksjonskall og visualisering.
- Krever Python 3.10+ og nødvendige biblioteker (`pandas`, `matplotlib`, `seaborn`, `scikit-learn`, m.fl.)
- Se `requirements.txt` og `requirements_macOS.txt` for full oversikt over avhengigheter.
- For å se mer detaljer i funksjonaliteten, se filer i `src-mappen`

---

## 📌 Oppsummering

Notebookene fungerer som dokumenterte og lesbare rapporter for hele prosjektforløpet, mens all gjenbrukbar logikk er kapslet i `src/`. Denne strukturen gir klar arbeidsdeling, god gjenbruk og profesjonell fremstilling.

### [**Til samlesiden**](../docs/samleside.md)