# src/ – Kildekode

Denne mappen inneholder all kildekode knyttet til prosjektets kjernelogikk. Koden er delt opp i tre hovedmoduler:

- `data_collection/` – Henter inn miljødata fra åpne API-er
- `data_cleaning/` – Renser og strukturerer data for analyse
- `graph/` – Lager visualiseringer basert på analyserte data

Funksjonene her importeres og brukes i hovednotebooken, slik at sluttbrukeren kan fokusere på å utforske og analysere data – uten å måtte forholde seg til store mengder kode.

---

## 📦 `data_collection/` – Datainnsamling

Denne modulen samler inn miljødata fra to åpne API-er: Meteorologisk institutts **Frost API** og **NILU API** for luftkvalitet. Dataene hentes med Python og lagres i `data/raw/` som `.json`- eller `.db`-filer.

---

### 🌦️ Frost API (Meteorologisk institutt)

Vi bruker Frost API til å hente værdata for Trondheim i perioden 2010–2019:

- Gjennomsnittlig lufttemperatur (daglig)
- Total nedbør (daglig)
- Gjennomsnittlig vindstyrke (daglig)

Fremgangsmåte:
- Henter nærmeste værstasjon basert på geografiske koordinater (Trondheim sentrum)
- Henter observasjoner for valgt tidsperiode via `observations`-endepunktet
- Strukturerer dataene i en DataFrame og aggregerer dem med SQL-spørring
- Lagrer resultatet i en SQLite-database (`data/raw/raw_api_frost_weather_trondheim_2010_to_2019.db`)

---

### 🌫️ NILU API (Norsk institutt for luftforskning)

Vi bruker NILU API for å hente luftkvalitetsdata for Trondheim for perioden 2010–2024.

Komponentene inkluderer blant annet:
- PM2.5
- PM10
- NO₂, O₃ m.m.

Fremgangsmåte:
- Bruker `stats/day`-endepunktet med koordinater og radius
- Henter data for alle tilgjengelige komponenter
- Lagrer resultatet som `.json` i `data/raw/raw_api_nilu_air_quality_trondheim_2010_to_2024.json`

---

### 🔐 Nøkkelhåndtering

- Frost API krever klient-ID (API-nøkkel), som lastes inn fra `.env`
- NILU API er offentlig og krever ingen autentisering

---

## 🧹 `data_cleaning/` – Datarensing

Etter at rådata er hentet, behandles de i `data_cleaning/` for å sikre at de er klare til analyse og visualisering.

Rensetrinnene for NILU-data inkluderer:
- Konvertering av `dateTime` til riktig tidsformat
- Pivoterer målinger slik at hver luftkomponent blir en kolonne
- Fjerner irrelevante komponenter (f.eks. benzo(a)pyrene)
- Fyller inn manglende dager med tomme rader
- Bruker lineær interpolasjon for å estimere manglende verdier
- Lager ekstra kolonner som viser hvilke verdier som er generert (interpolert)
- Runder av verdier og fjerner duplikater
- Erstatter negative verdier med 0 for å unngå feil i videre analyser

Den rensede dataen lagres i `data/clean/` som `.json` og inneholder én rad per dato, med enhetlige og ryddige kolonnenavn.

---

## 📊 `graph/` – Visualisering (under utvikling)

Denne modulen er foreløpig under utvikling og vil bli utvidet i neste del av prosjektet. Her skal vi lage funksjoner for å visualisere analyseresultatene på en ryddig og informativ måte.

Planen er å bruke biblioteker som:
- **matplotlib** og **seaborn** for klassiske statiske grafer
- **plotly** for interaktive grafer i Jupyter Notebook

Visualiseringene skal gjøre det lettere å:
- Se trender og variasjoner over tid
- Sammenligne ulike miljøparametere
- Formidle innsikt basert på de analyserte dataene

Funksjonene i denne mappen vil kunne importeres direkte i notebooken og brukes med rensede datasett.

---

## 📌 Merk

- API-nøkler håndteres med `.env`-fil og `python-dotenv`
- Rådata og renset data lagres i egne undermapper for sporbarhet
- Koden er strukturert for å kunne gjenbrukes og testes senere i prosjektet

