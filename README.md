# 🌳 Miljødataanalyse
Dette prosjektet er utviklet som en del av faget Anvendt programmering ved NTNU, og har som mål å gi oss studenter praktisk erfaring med programmering, dataanalyse, datavisualisering, versjonskontroll og testing.

Prosjektet handler om å hente inn miljødata fra åpne kilder – som for eksempel værdata og luftkvalitet – for å analysere, rense og visualisere informasjonen på en måte som kan gi innsikt i miljørelaterte utfordringer.

I tillegg til dette skal vi også gjennomføre en prediktiv analyse basert på værdata, for å kunne si noe om hvordan klimaet kan utvikle seg fremover. 


## ⚙️ Kom i gang

For å kunne kjøre prosjektet lokalt og følge analysene steg for steg, må du sette opp utviklingsmiljøet ditt med riktig Python-versjon og nødvendige biblioteker. Denne delen hjelper deg i gang med å klone prosjektet, opprette et virtuelt miljø og installere nødvendige biblioteker.

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


## 📖 Oppgavetolkning og tilnærming

I dette prosjektet har vi tolket oppgaven som en mulighet til å hente inn, bearbeide og analysere miljødata for å få innsikt i ulike typer miljøutfordringer. For å gjøre oppgaven mer konkret og målrettet, har vi valgt å dele prosjektet i to deler basert på to forskjellige datakilder:

- **Luftkvalitet**: Måledata fra Trondheim som gir innsikt i lokal luftforurensning og hvordan den varierer over tid.  
- **Værdata**: Historiske værdata fra en valgfri lokasjon, som brukes som grunnlag for en prediktiv analyse av fremtidig klimautvikling.

Ved å analysere luftdata kan man avdekke mønstre og trender i luftforurensning, noe som er nyttig for både innbyggere og beslutningstakere. Værdataen gir oss muligheten til å se på langsiktige klimaendringer, og med prediktiv modellering kan vi forsøke å si noe om hvordan klimaet vil utvikle seg fremover.

Vi har strukturert arbeidet vårt i fire hovedfaser:

1. **Datainnsamling** – hente rådata fra åpne og pålitelige kilder  
2. **Datarensing** – rydde og strukturere dataene for å sikre kvalitet  
3. **Analyse og visualisering** – gjøre dataene forståelige og utforske mønstre og sammenhenger  
4. **Prediktiv analyse** – (for værdata) modellere og forutsi fremtidige klimatiske forhold

Denne fremgangsmåten gir en helhetlig og praktisk innføring i hvordan miljødata kan brukes for å få innsikt, ta bedre beslutninger og forstå utviklingen over tid.



## 📁 Mappestruktur
Under vises en oversikt over prosjektets mappestruktur. Strukturen er laget for å gi god oversikt, skille mellom rådata, kode og dokumentasjon, og legge til rette for en ryddig og effektiv arbeidsflyt.

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


## 🚀 Kom i gang med prosjektet

Nå som prosjektets bakgrunn og struktur er presentert, er neste steg å starte selve gjennomføringen. Vi har laget en hovednotebook som fungerer som inngangspunkt og guider deg gjennom installasjon, oppgavetolkning og første steg i dataanalysen.

👉 Gå videre til [notebooken for datainnsamling og rensing](notebooks/00_project_setup.ipynb) for å sette i gang.



