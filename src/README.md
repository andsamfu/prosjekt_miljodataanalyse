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

## 🧹 Datarensing (`data_cleaning/`)

Etter at rådata er hentet, behandles de i `data_cleaning/` for å sikre at de er klare til analyse og visualisering. Dette innebærer en rekke rensetrinn som er nøye tilpasset formålet med prosjektet: å sikre høy datakvalitet, pålitelighet og sporbarhet.

### Rensetrinn og valg

Rensingen av NILU-data følger en strukturert prosess der hvert steg er begrunnet:

1. **Konvertering av datoer**  
   - `dateTime` konverteres til korrekt datetime-format for videre tidsseriebehandling.

2. **Pivottabell**  
   - Målinger transformeres slik at hver luftkomponent (f.eks. NO₂, PM10, PM2.5) får sin egen kolonne.

3. **Fjerning av uønsket kolonne**  
   - **Valg**: *Benzo(a)pyrene in PM10 (aerosol)* fjernes.  
   - **Begrunnelse**: Denne komponenten er ikke relevant for analysen og fjernes for å redusere støy og holde fokus på sentrale luftkvalitetsindikatorer.

4. **Reindeksering for å inkludere alle datoer**  
   - Datoindeksen utvides slik at alle datoer i perioden dekkes, også de uten målinger.  
   - **Begrunnelse**: Dette sikrer en komplett tidsserie og tydeliggjør eventuelle manglende data.

5. **KNN-imputasjon for manglende verdier**  
   - **Valg**: Manglende verdier fylles inn ved hjelp av KNN-imputasjon med 50 nærmeste naboer (k=50).  
   - **Begrunnelse**: KNN gir mer nøyaktige estimater enn enklere metoder som lineær interpolasjon, særlig når store dataintervaller mangler. Metoden tar hensyn til sammenhenger mellom komponenter og fanger opp sesongvariasjoner, noe som gir mer realistiske og pålitelige verdier.

6. **Markering av genererte verdier**  
   - Kolonner på formen `generated_<column>` opprettes for å vise hvilke verdier som er imputert.  
   - **Begrunnelse**: Dette øker transparens og gir mulighet til å skille mellom originale og estimerte data.

7. **Håndtering av negative verdier**  
   - **Valg**: Alle negative verdier settes til 0.  
   - **Begrunnelse**: Negative verdier er ugyldige for luftkvalitetsmålinger og kan skyldes målefeil.

8. **Fjerning av duplikater**  
   - **Valg**: Kun første forekomst beholdes ved duplikate tidsstempler.  
   - **Begrunnelse**: Duplikater kan føre til skjevheter og overrepresentasjon i analysen.

9. **Runding av verdier**  
   - **Valg**: Verdier rundes av til maksimalt 4 desimaler.  
   - **Begrunnelse**: Gir konsistent formatering og økt lesbarhet, uten å ofre nødvendig presisjon.

10. **Lagring av renset data**  
    - **Valg**: Renset datasett lagres som `.json` i `data/clean/`.  
    - **Begrunnelse**: JSON er både lett å lese og kompatibelt med videre analyse- og visualiseringsverktøy. Hver fil inneholder én rad per dato med standardiserte kolonnenavn.

---

### ✅ Oppsummering

Databehandlingen i `data_cleaning_nilu.py` følger prinsipper for god datarensing: fjerning av støy, håndtering av manglende eller ugyldige verdier, tydelig merking av estimerte data og standardisering. Disse grepene danner et solid grunnlag for videre analyse, prediksjon og visualisering, og sikrer at dataene er både pålitelige og transparente.


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

