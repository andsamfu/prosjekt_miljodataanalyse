# Refleksjonsnotat

Gjennom dette prosjektet har vi fått en dypere innsikt i både tekniske og mer overordnede sider ved å jobbe med datadrevne miljøspørsmål. Prosessen har vært preget av både frustrasjon og mestring, og vi har erfart at slike prosjekter handler om langt mer enn bare koding og analyse: samarbeid, struktur og kontinuerlig vurdering av egne valg er avgjørende.

## Læring om datainnsamling, behandling og analyse

En av de viktigste lærdommene har vært hvor kritisk det er å være grundig fra starten. Rådataene vi hentet fra FROST og NILU krevde omfattende rensing før de kunne brukes. Vi brukte mye tid på å rydde opp i datasettene og innså at datarensing ikke bare er en teknisk øvelse, men krever kontekstforståelse. Hvilke verdier skal beholdes? Hvilke skal fjernes eller estimeres? Slike vurderinger påvirker analysene videre.

Pandas ble vårt viktigste verktøy for databehandling. Gjennom det lærte vi hvordan vi kan filtrere, gruppere og kombinere data effektivt. Vi brukte også NumPy, Matplotlib og Seaborn for analyser og visualisering, og utviklet trygghet i å lage figurer som både er informative og visuelt gode.

## Nye ferdigheter og verktøy

To av oss hadde lite erfaring med Git før prosjektet, men gjennom aktiv bruk av GitHub føler vi oss nå langt tryggere. Vi opprettet egne grener for ulike oppgaver og brukte pull requests til gjennomgang, noe som reduserte feil og styrket forståelsen av god programvarepraksis. Én i gruppa hadde erfaring fra før, og vi lærte mye av hverandre underveis.

## Utfordringer og problemløsning

Den største tekniske utfordringen var håndteringen av manglende verdier i NILU-datasettet. De metodene vi kjente fra undervisningen fungerte dårlig på datasett med store hull. Etter testing og sammenligning endte vi med KNN-imputasjon, som ga betydelig bedre resultater. Dette viste oss hvor viktig det er å utfordre standardløsninger og velge metoder tilpasset datasettet.

Vi støtte også på vanlige utviklingsproblemer som feilmeldinger, pakkeavhengigheter og formateringsproblemer. Her erfarte vi verdien av tydelige kravfiler (`requirements.txt`) og versjonskontroll – det gir kontroll og trygghet i arbeidet.

## Samarbeid og arbeidsflyt

Vi jobbet tett sammen, ofte fysisk på campus. Oppgavene ble i stor grad fordelt etter interesser og styrker: én tok ansvar for NILU-data, én for FROST-data, og én for visualisering og analyse. Samtidig diskuterte vi valg og løsninger i fellesskap. Denne arbeidsformen gjorde at alle holdt seg involvert og at vi raskt løste utfordringer.

GitHub var et uvurderlig samarbeidsverktøy. Det ga oversikt over fremdrift og gjorde det enkelt å unngå konflikter i arbeidet. Samarbeidet fungerte svært godt – vi opplevde både motivasjon, støtte og god struktur gjennom hele prosjektet.

## Vurdering av resultat

Vi er svært fornøyde med sluttproduktet. Visualiseringene er tydelige og meningsfulle, og vi har analysert både temperatur- og luftkvalitetsvariasjoner på en måte som er lett å forstå. Den prediktive modellen vi lagde, ga oss innblikk i hvordan maskinlæring kan brukes i praksis – selv med enkle metoder. Vi har forsøkt å gjøre det lille ekstra, og brukt sensurveiledningene aktivt for å nå de høyeste vurderingskriteriene.

## Forbedringspunkter

Til et lignende prosjekt i fremtiden ønsker vi å forbedre følgende:

- **Brukervennlighet**: Vi skulle gjerne laget et grensesnitt der brukeren selv kan velge by og tidsrom.
- **Struktur fra start**: En enda tydeligere mappestruktur og rollefordeling i starten hadde gjort prosessen enklere.
- **Tidlig testing**: Enhetstesting burde vært introdusert tidligere, særlig ved transformasjon og datarensing.

## Videre utviklingspotensial

Vi har mange idéer til videreutvikling, blant annet:

- Utvide med flere miljøparametere som støy, trafikk og fuktighet
- Lage en sanntidsbasert visualiseringsplattform på nett
- Koble miljødata med helsedata eller policy-endringer

## Oppsummering og personlig utbytte

Vi har lært mye om både datavitenskap og miljøspørsmål. Viktigheten av planlegging, struktur, dokumentasjon og ryddig kode er noe vi tar med oss videre. Dette prosjektet har gjort oss bedre rustet til større prosjekter, både i studier og arbeidsliv – og ikke minst har motivasjonen for videre arbeid med data økt. Vi ser tydelig hvordan dette kan brukes i samfunnsnyttige sammenhenger, fra miljøforvaltning til helseteknologi.

> *(Refleksjonsnotatet kunne vært mer utdypende, men vi hadde maks 800 ord å forholde oss til.)*
