# Release Notes – Miljødataanalyse

## Versjon 1.0 – Sluttlevering (mai 2025)

Dette er første versjon av prosjektet. Den inneholder en komplett løsning for innhenting, rensing, analyse, visualisering og prediksjon basert på miljødata fra Trondheim.

### Innhold i denne versjonen

- Datainnhenting fra Frost (vær) og NILU (luftkvalitet) via API
- Datavalidering og rensing implementert i egne Python-moduler
- Manglende verdier behandlet med KNN-imputasjon (NILU-data)
- Datavisualisering med Matplotlib, Plotly og Seaborne
- Prediktiv analyse med lineær regresjon på temperatur og luftkvalitet
- Enhetstester for alle datavalideringsklasser
- Strukturert prosjekt med tydelig mappestruktur og god dokumentasjon

### Begrensninger

- Enkel modell for prediksjon (kun en variabel)
- Ikke implementert grafisk interaktivt brukergrensesnitt
- Kun testet med datasett fra Trondheim

### Laget av

- Anders Meyer Hegre
- Ahmed Salameh
- Oliver Røddesnes
