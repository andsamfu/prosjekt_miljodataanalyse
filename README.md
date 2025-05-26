# 🌳 Miljødataanalyse

Dette prosjektet er utviklet som en del av faget TDT4114 – Anvendt programmering, og har som mål å gi praktisk erfaring med programmering, dataanalyse, datavisualisering, versjonskontroll og testing.

Prosjektet tar for seg miljødata fra åpne kilder – spesielt værdata og luftkvalitet – og viser hvordan slike data kan hentes inn, renses, analyseres og visualiseres for å skape innsikt i miljøutvikling og bærekraftige beslutninger.

Et sentralt element i prosjektet er også prediktiv analyse, der vi prøver å si noe om hvordan temperaturer og luftkvalitet i Trondheim kan utvikle seg fremover, basert på historiske observasjoner.



---

## 📖 Oppgavetolkning og tilnærming

Vi har valgt å fokusere på to hoveddatakilder:

- **Luftkvalitet (NILU)** – daglige målinger av partikler og gasser i Trondheim
- **Værdata (Frost/MET)** – historiske daglige temperaturer og nedbør

Vi har delt prosjektet inn i fire hovedfaser:

1. **Datainnsamling** – Hente rådata via åpne API-er (Frost og NILU)
2. **Datarensing** – Renser data og forbereder til videre analyse
3. **Analyse og visualisering** – Utforske mønstre og utvikling over tid
4. **Prediktiv analyse** – Modellere temperatur og luftkvalitet frem i tid

Hver fase er dokumentert i sin egen Jupyter-notebook. All funksjonell logikk er kapslet i moduler i `src/`.

---

## 🧱 Mappestruktur

```bash
.
├── data/                           # Datasett (rå, renset, analyseresultater)
│   ├── raw/                        # Ubehandlede data fra API
│   ├── clean/                      # Rensede datasett
│   └── analyses_results/           # Aggregerte analyser og korrelasjoner
│   └── README.md                  
│
├── notebooks/                      # Dokumentasjon av arbeidsflyt i Jupyter
│   ├── 00_project_setup.ipynb
│   ├── 01_data_cleaning.ipynb
│   ├── 02_data_analysis_and_visualisation.ipynb
│   ├── 03_predictive_analysis.ipynb
│   ├── data_collection.ipynb
│   ├── KNN_imputation.ipynb
│   └── README.md                   # Forklaring av hver notebook og struktur
│
├── src/                            # All funksjonell Python-kode
│   ├── data_collection/            # API-henting og filskriving
│   ├── data_cleaning/              # Rensing, validering, imputasjon
│   ├── data_analysis/              # Statistisk aggregering
│   ├── data_visualizations/        # Grafer og diagrammer
│   ├── predictive_analysis/        # Prediktive modeller og visualisering
│   └── README.md                  
│
├── docs/                           
│   ├── answer/                     # Svar på oppgaver
│   ├── ki-deklarasjon/             # KI deklarasjoner
│   ├── git_bruk.md                 # Hvordan vi har brukt git
│   ├── refleksjonsnotat.md         # Refleksjonsnotat
│   └── samleside.md                # Samleside med linking til alt
│
├── resources/                      # Bilder av ulike visualiseringer
│   └── images/
│
├── requirements/                   # Bibliotekavhengigheter
│   ├── requirements_macOS.txt
│   ├── requirements_windows.txt
│   └── README.md
│
├── .gitignore                      # Utelater filer fra versjonskontroll
├── .env                            # API-nøkler (lokal bruk)
├── release_notes.md
└── README.md
```

## 🚀 Kom i gang med prosjektet

For å kunne kjøre prosjektet lokalt og følge analysene steg for steg, må du sette opp utviklingsmiljøet ditt med riktig Python-versjon og nødvendige biblioteker. Denne delen hjelper deg i gang med å klone prosjektet, opprette et virtuelt miljø og installere nødvendige biblioteker.

### Forutsetninger
- Python 3.13.2 eller nyere
- pip eller annen pakkebehandler
- Git installert

#### Installasjon

1. Klon prosjektet:
```bash
git clone https://github.com/andsamfu/prosjekt_miljodataanalyse.git
cd miljodataanalyse
```

2. Lag et virtuelt miljø og aktiver det:

Mac og Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

Windows
```bash
python -m venv venv
venv\Scripts\activate
```

Om du får feilmelding på windows kjør kommandoen under, og prøv kommandoen over igjen:
```bash
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

3. Oppdater pip til nyeste versjon (test opp til versjon 25.1.1)
```bash
python.exe -m pip install --upgrade pip
```

4. Installer nødvendige biblioteker:

Mac og Linux
```bash
pip install -r requirements_macOS.txt
```

Windows
```bash
pip install -r requierments_windows.txt
```

### [Videre til datainnsamling](notebooks/00_project_setup.ipynb) 



