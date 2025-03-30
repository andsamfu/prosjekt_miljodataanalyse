# Svar mappe del 1

## Relevante datakilder:

1. Frost API (MET Norway)
   1. Datatype: Historiske værdata (2010-2019)
   2. Format: DB fil
   3. Nøkkeldata: Temperatur, nedbør, vindhastighet
   4. Autoritet: Meteorologisk institutt (offisiell norsk kilde)
   5. Tilgjengelighet: Krever API-nøkkel
2. NILU API
   1. Datatype: Luftkvalitetsdata (2010-2024)
   2. Format: JSON
   3. Nøkkeldata: PM2.5, NO2, PM10
   4. Autoritet: Norsk institutt for luftforskning
   5. Tilgjengelighet: Åpent API

Vi har også hentet inn andre datakilder som SSB, GlobalCarbonAtlas og world in our data som vi kanskje skal bruke senere.

### Vurderingskriterier for kvalitet:
- **Kildeautoritet**: Alle er offisielle norske institusjoner
- **Dekning**: Minimum 10 års dataserier
- **Konsistens**: Standardiserte målemetoder
- **Tilgjengelighet**: Frost krever autentisering, andre er åpent tilgjengelige
- **Oppdateringsfrekvens**: Varierende (dagligvis til årlig)
 
## Teknikker for datainnlesning og prosessering
### Frost API-data
Brukte teknikker:

- JSON til SQLite-transformasjon

Data hentes som JSON og lagres i en SQLite-database

- Fordeler:
    - Lar oss kjøre avanserte spørringer direkte på dataene
    - Raskere å jobbe med enn store JSON-filer
- Påvirkning:
    - Sikrer nøyaktige beregninger av døgnverdier

**Analyseprosess**:
1.	Data hentes via API som JSON
2.	Transformeres til Pandas DataFrame
3.	Lagres i SQLite-database
4.	Analyseres med Pandas SQL-spørringer

### NILU API-data
Brukte teknikker:
- Direkte JSON-lagring
Data lagres i originalt JSON-format
- Fordeler:
    - Beholder all original informasjon
    - Enkelt å validere mot API-spesifikasjonen
- Påvirkning:
    - Ingen datatap under lagring

**Analyseprosess**:

1.	Data hentes som JSON
2.	Lagres direkte uten transformasjon
3.	Tidssoner konverteres ved behov
 
## Spesifikke API-er og deres viktigste data

### 1. Frost API (MET Norway)
- API-endepunkt: https://frost.met.no/observations/v0.jsonld
- Hoved data:
    - Døgnmiddeltemperatur (°C)
    - Døgnnedbør (mm)
    - Døgnmiddelvindhastighet (m/s)
- Dekning:
    - Historiske data for Trondheim (2010–2019)
- Autentisering:
    - Krever API-nøkkel (registrering hos MET Norway).
 
### 2. NILU API
- API-endepunkt: https://api.nilu.no/stats/day/[from]/[to]/[lat]/[lon]/[radius]
- Hoved data:
    - PM10 – Grovere partikkelforurensning (µg/m³)
    - PM2.5 – Fin partikkelforurensning (µg/m³)
    - NO2 – Nitrogenoksider
- Dekning:
    - Luftkvalitetsdata for Trondheim (2010–2024)
- Autentisering:
    - Åpent tilgjengelig (ingen nøkkel nødvendig).
 
## Hvordan vi har gjort databehandling i vår oppgave
I vår oppgave har vi behandlet data fra to forskjellige kilder: NILU (luftkvalitet) og Frost (værdata). Prosessen har inkludert innhenting, rensing, transformasjon og lagring av data.

1. Innhenting av data:
    1. NILU-dataene er hentet fra en JSON-fil (api_nilu_air_quality.json) som inneholder luftforurensningsmålinger fra Trondheim .
    2. Frost-dataene er hentet via et API-kall til frost.met.no, hvor vi har samlet daglige temperatur-, nedbørs- og vindmålinger fra 2010 til 2019 .
2. Rensing og håndtering av manglende verdier:
   1. NILU-dataene er organisert og pivotert slik at hver komponent (NO2, PM10, PM2.5) blir en egen kolonne.
   2. Vi har interpolert manglende verdier lineært og markert interpolerte verdier i separate kolonner for transparens.
   3. Eventuelle negative verdier er satt til null for å unngå feilaktige målinger.
3. Datatransformasjon:
   1. NILU-dataene er omgjort til en tidsserie med alle datoer inkludert, selv om det mangler målinger på enkelte dager.
   2. Frost-dataene er filtrert og aggregert ved hjelp av SQL-spørringer (Pandas SQL) for å gruppere dataene etter dato og omforme de rå målingene til en mer analysevennlig struktur.
4. Lagring av rensede data:
   1. NILU-dataene er lagret i en JSON-fil (cleaned_data_nilu.json) med manglende verdier erstattet eller interpolert .
   2. Frost-dataene er lagret i en SQLite-database (api_frost_weather.db) i tabellen weather_data.

### 1. Hvilke metoder har vi brukt for å håndtere manglende verdier i datasettet?
- Vi har interpolert manglende verdier lineært (df_pivot.interpolate(method='linear')).
- Vi har reindeksert datasettet slik at alle datoer mellom start- og sluttdato er med, selv om de opprinnelige dataene manglet målinger.
- Vi har markert interpolerte verdier med egne kolonner (generated_NO2, generated_PM10, etc.).
- Negative verdier har blitt satt til null for å unngå feilaktige målinger.
 
### 2. Hvordan kan vi bruke list comprehensions for å manipulere dataene?
- Vi har brukt en løkke for å erstatte NaN-verdier med None i JSON-filen. Dette ble gjort med en list comprehension som dette:

Dette gjør at vi raskt kan iterere gjennom alle rader og erstatte NaN med None.

### 3. Hvordan har vi brukt Pandas SQL (sqldf) for å forbedre datamanipuleringen?
- Ved å bruke SQL-spørringer med pandasSQL kunne vi enkelt aggregere og strukturere Frost-dataene.
- Vi brukte SQL for å hente daglige gjennomsnittsverdier for temperatur, summere nedbør og hente maksimal vindstyrke på en ryddig måte:

Dette gjorde at vi kunne samle inn data mer effektivt sammenlignet med flere separate Pandas-operasjoner.

### 4. Hvilke spesifikke uregelmessigheter i dataene forventet vi å møte, og hvordan håndterte vi dem?
- Manglende datoer: Løst ved å interpolere manglende verdier og reindeksere datasettet.
- Negative verdier: Løst ved å sette dem til null. (ikke temperatur)
- Duplikater: Sjekket og fjernet ved å bruke df_pivot.index.duplicated(keep='first').
- Ulike måleenheter: Frost-dataene har ulike måleenheter, men vi sørget for å opprettholde riktig enhet ved å bruke SQL-spørringer.

