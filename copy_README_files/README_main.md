# Miljødataanalyse

Dette prosjektet er utviklet som en del av faget Anvendt programering på NTNU, og har som mål å gi studentene praktisk erfaring med programmering, dataanalyse, datavisualisering, versjonskontroll og testing. Prosjektet handler om å hente inn miljødata fra åpne kilder – som for eksempel værdata og luftkvalitet – for å analysere, rense og visualisere informasjonen på en måte som kan gi innsikt i miljørelaterte utfordringer.

Dataene vi samler inn kommer fra åpne og pålitelige datakilder, og skal brukes til å:
- Identifisere trender og mønstre i miljøutvikling
- Sammenligne data over tid eller geografisk
- Bidra til datadrevne prediksjoner

---

## 🎯 Målsetning

- Hente miljødata fra åpne API-er og datasett
- Rense, transformere og lagre dataene i strukturert form
- Analysere data med Python og relevante biblioteker
- Visualisere resultater på en forståelig måte
- Utføre predektive analyser på datasettene
- Bruke versjonskontroll og samarbeide effektivt i team
- Etter hvert også implementere enhetstesting

---

## 📁 Mappestruktur

```bash
.
├── data/                             # Datasett (rå, renset)
│   ├── raw/
│   └── clean/
├── docs/                             # Dokumentasjon (inkl. KI-erklæring)
│   └── ki/
├── notebooks/                        # Analyse og visualisering i Jupyter
├── src/                              # Kildekode
│   ├── data_collection/              # Innsamling av data
│   ├── data_cleaning/                # Rensing og klargjøring av data
│   └── graph/                        # Generering av grafer
├── tests/                            # Enhetstester (kommer senere i prosjektet)
├── .gitignore
├── requirements/                     # Liste over nødvendige Python-biblioteker
│   ├── requierments_macOS.txt/       # Innsamling av data
│   └── requierments_windows.txt/     # Rensing og klargjøring av data
└── README.md
```

---

## ⚙️ Kom i gang

### Forutsetninger
- Python 3.13.2 eller nyere
- pip eller annen pakkebehandler
- Git installert

### Installasjon

1. Klon prosjektet:
```bash
git clone https://github.com/dittbrukernavn/miljodataanalyse.git
cd miljodataanalyse
```

2. Lag et virtuelt miljø og aktiver det:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. Installer nødvendige biblioteker:
```bash
pip install -r requirements_macOS.txt  #Windows: requierments_windows.txt
```

---

## 📊 Brukte teknologier og biblioteker

- Python
- Jupyter Notebook
- pandas, numpy (databehandling)
- matplotlib, seaborn, plotly (visualisering)
- requests, dotenv (API-tilgang)
- Git og GitHub (versjonskontroll og samarbeid)

---

## 🔍 Datakilder

Vi benytter åpne og autoritative kilder som:
- [Yr API (Meteorologisk institutt)](https://developer.yr.no/)
- [NILU – Norsk institutt for luftforskning](https://api.nilu.no/)

Alle brukte datakilder dokumenteres kort her, og du finner mer detaljer i README-filene i de respektive mappene som `src/data_collection/` og `data/`

---

## ✅ Enhetstesting

Per nå er det ikke lagt inn noen enhetstester i prosjektet. Mappen `tests/` er opprettet og skal fylles ut senere i prosjektforløpet, i forkant av ferdig innlevering. Vi planlegger å bruke `unittest` for å teste kritiske funksjoner med både gyldige og ugyldige input.

---

## 🔁 Versjonskontroll

Prosjektet benytter Git og GitHub, og følger anbefalte praksiser:

- Separate grener for funksjoner og oppgaver (`feature/`, `fix/`, `upgrade/` osv.)
- GitHub Issues brukes til å fordele og spore oppgaver
- Pull requests og merges til `main`
- `.gitignore` for å unngå innjekking av store eller følsomme filer
- Jevnlige commits med beskrivende meldinger
- README-filer og requirements-fil holdes oppdatert

---

## 🧾 Lisens

Dette prosjektet er laget som en del av et skolefag, og er ment for læring og innlevering. Koden kan gjerne brukes og deles innenfor klassen eller fagmiljøet, men er ikke ment for kommersiell bruk.
