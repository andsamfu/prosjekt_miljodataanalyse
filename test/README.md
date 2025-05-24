# 🧪 Testoversikt
Dette er testmappen for datavalidering av værdata. Testene er implementert ved hjelp av Pythons innebygde unittest-rammeverk og følger beste praksis for testing.

## 📋 Teststruktur
Testene er organisert i fire hovedklasser som tilsvarer de fire valideringsklassene i `data_validators.py`:

1. **TestMissingValueValidator** - Tester for validering av manglende verdier
2. **TestOutlierValidator** - Tester for validering av uteliggere
3. **TestDateContinuityValidator** - Tester for validering av datokontinuitet
4. **TestImputationValidator** - Tester for validering av dataimputering

## 🎯 Beste Praksis for Testing

### Arrange-Act-Assert Mønsteret
Alle testene følger AAA-mønsteret:
```python
def test_example(self):
    # Arrange - Sett opp testdata og objekter
    test_data = pd.DataFrame(...)
    
    # Act - Utfør handlingen som skal testes
    result = validator.validate(test_data)
    
    # Assert - Verifiser at resultatet er som forventet
    self.assertEqual(expected, result)
```

### Positive og Negative Tester
- **Positive tester**: Verifiserer at koden fungerer som forventet med gyldig input
- **Negative tester**: Verifiserer at koden håndterer ugyldige eller uventede inputs på en god måte

## 📊 Testdata Struktur
Testdataene er lagret i `mock_weather_data.json` og er organisert i følgende kategorier:

### 1. Positive Tests (Gyldig Data)
Brukes av `MissingValueValidator` og andre validatorer for å teste normal oppførsel med komplett, gyldig data.

### 2. Date Sequence Tests (Datosekvenser)
Brukes primært av `DateContinuityValidator` for å teste:
- Hull i datosekvenser
- Manglende datoer over måneds- og årsgrenser
- Duplikate datoer

### 3. Value Tests (Verdier)
Brukes av både `MissingValueValidator` og `OutlierValidator` for å teste:
- Manglende verdier i kolonner
- Uteliggere utenfor gyldige verdiområder
- Komplette og tomme datasett

### 4. Format/Type Tests (Formatering)
Tester validering av:
- Ugyldige datoformater
- Feil datatyper
- Formatfeil i verdier

### 5. Imputation Tests (Dataimputering)
Brukes av `ImputationValidator` for å teste:
- KNN-imputering av manglende verdier
- Validering av imputerte verdier
- Sporingskolonner for genererte verdier

## ❓ Hvorfor Enhetstesting?
Enhetstestene i dette prosjektet har et spesifikt fokus på datakvalitet og pålitelighet. Hovedmålet er å sikre at datarenseprosessen fungerer som forventet ved å:

- Oppdage og håndtere vanlige datakvalitetsproblemer som manglende verdier og feil formater
- Validere at dataene blir transformert korrekt gjennom renseprosessen
- Sikre at renset data er pålitelig for videre analyse og visualisering

Testene dekker de mest vanlige utfordringene med værdata, som manglende målinger, feilformateringer og uteliggere, uten å prøve å dekke alle tenkelige edge cases.

## 🔄 Datarenseprosessen
Testene følger den samme flyten som datarenseprosessen:

1. **MissingValueValidator**: Sjekker etter og markerer manglende verdier i datasettet
2. **OutlierValidator**: Identifiserer verdier utenfor normale områder
3. **DateContinuityValidator**: Sikrer kontinuitet i tidsserie-dataene
4. **ImputationValidator**: Validerer at imputerte verdier er fornuftige

Hver validator returnerer både resultatene av valideringen og et renset datasett som kan brukes videre i kjeden.

## 🛠️ Kjøre Testene
For å kjøre testene, aktiver først det virtuelle miljøet og kjør unittest:

```powershell
.\venv\Scripts\Activate.ps1
python -m unittest discover test
```

## 📈 Validering og Gyldige Verdiområder
Testene validerer at alle dataverdier ligger innenfor fysisk realistiske områder for Trondheim:

### Temperatur
- Gyldig område: -30°C til 40°C
- Validerer både rådata og imputerte verdier

### Nedbør
- Gyldig område: 0mm til 250mm
- Må alltid være ikke-negativ

### Vindstyrke
- Gyldig område: 0 m/s til 60 m/s
- Må alltid være ikke-negativ


### [**Til samlesiden**](../docs/samleside.md)