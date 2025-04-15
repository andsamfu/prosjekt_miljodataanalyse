# data/ – Datamappe

Denne mappen inneholder datasett som brukes i prosjektet, delt opp i rå og renset data. Vi skiller tydelig mellom data hentet direkte fra kildene (raw) og data som er bearbeidet og klar til analyse (clean).

---

## 📁 raw/

Her lagres rådata hentet via skript i `src/data_collection/`. Per nå bruker vi kun data som er hentet via åpne API-er med nøkkel (Frost/Yr og NILU). I noen tilfeller har vi også testet nedlastet data fra åpne nettressurser, men dette er trolig midlertidig og kan bli slettet.

Eksempler:
- `raw_api_frost_weather_trondheim_2010_to_2019.db`
- `raw_api_nilu_air_quality_trondheim_2010_to_2024.json`

Disse filene skal **ikke pushes til Git**, ettersom de kan være store og enkelt reproduseres via prosjektets Python-skript.

---

## 📁 clean/

Her lagres renset og strukturert data, klar for videre bruk i visualisering og prediktiv analyse. Rensingen skjer i `src/data_cleaning/`, og inkluderer:
- Fjerning av ugyldige og negative verdier
- Interpolasjon av manglende data
- Standardisering av format og datoer
- Pivotering og rydding

Eksempel:
- `cleaned_data_nilu.json`

Disse filene er også utelatt fra Git-versjonen og gjenopprettes enkelt ved å kjøre renselogikken på nytt.

---

## 🚫 Versjonskontroll og `.gitignore`

Alle datafiler i denne mappen er lagt til `.gitignore`, slik at vi unngår å legge inn store filer i Git. Dataene kan gjenskapes via skriptene i prosjektet og er derfor ikke nødvendig å lagre i repoet.

---
