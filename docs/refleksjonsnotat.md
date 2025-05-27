# Refleksjonsnotat

Gjennom dette prosjektet har vi fått en dypere innsikt i både tekniske og mer overordnede sider ved å jobbe med datadrevne miljøspørsmål. Prosessen har vært preget av både frustrasjon og mestring, og vi har erfart at slike prosjekter handler om langt mer enn bare koding og analyse: samarbeid, struktur og kontinuerlig vurdering av egne valg er avgjørende.

## Læring om datainnsamling, behandling og analyse

En av de viktigste lærdommene har vært hvor avgjørende det er å være grundig fra starten. Rådataene vi hentet fra FROST og NILU krevde omfattende rensing før de kunne brukes, og vi brukte mye tid på å rydde opp i datasettene. Vi innså at datarensing ikke bare er en teknisk øvelse, men krever god kontekstforståelse – hvilke verdier skal beholdes, hvilke skal fjernes eller estimeres, og hvordan påvirker disse valgene analysen videre?

Pandas har vært vårt viktigste verktøy for databehandling, og vi har lært mye om hvordan vi kan filtrere, gruppere og kombinere data effektivt. Vi har også fått innsikt i hvordan NumPy, Matplotlib og Seaborn kan brukes til analyser og visualiseringer, og blitt tryggere på å lage figurer som er både informative og visuelt gode.

## Nye ferdigheter og verktøy

To av oss hadde lite erfaring med Git før prosjektet, men gjennom aktiv bruk av GitHub føler vi oss nå langt tryggere. Oppretting av egne grener for ulike oppgaver og bruk av pull requests har redusert feil og styrket forståelsen av god programvarepraksis. Én i gruppa hadde erfaring fra før, og vi har lært mye av hverandre underveis. Dette har gitt oss innsikt i hvordan profesjonelle utviklingsprosesser kan fungere i praksis.

## Utfordringer og problemløsning

Den største tekniske utfordringen var håndteringen av manglende verdier i NILU-datasettet. Metodene vi kjente fra undervisningen fungerte dårlig på datasett med store hull. Etter testing og sammenligning endte vi med KNN-imputasjon, som ga betydelig bedre resultater. Dette viste oss hvor viktig det er å utfordre standardløsninger og tilpasse metoder til datasettet. I tillegg støtte vi på vanlige utviklingsproblemer som feilmeldinger, pakkeavhengigheter og formateringsproblemer, hvor vi erfarte verdien av tydelige kravfiler (requirements.txt) og versjonskontroll for å ha kontroll og trygghet i arbeidet.

## Samarbeid og arbeidsflyt

Vi jobbet tett sammen, ofte fysisk på campus. Oppgavene ble i stor grad fordelt etter interesser og styrker: én tok ansvar for NILU-data, én for FROST-data, og én for visualisering og analyse. Samtidig diskuterte vi valg og løsninger i fellesskap. Denne arbeidsformen gjorde at alle holdt seg involvert og at vi raskt løste utfordringer. Jevnlige statusmøter og åpenhet rundt egne styrker og svakheter bidro til effektiv kommunikasjon og felles eierskap til prosjektet. GitHub var et uvurderlig samarbeidsverktøy og ga oss oversikt over fremdrift og bidro til å unngå konflikter. Samarbeidet fungerte svært godt – vi opplevde både motivasjon, støtte og god struktur gjennom hele prosjektet.

## Vurdering av resultat

Vi er svært fornøyde med sluttproduktet. Visualiseringene er tydelige og meningsfulle, og vi har analysert både temperatur- og luftkvalitetsvariasjoner på en måte som er lett å forstå. Den prediktive modellen ga oss innblikk i hvordan maskinlæring kan brukes i praksis – selv med enkle metoder. Vi har forsøkt å gjøre det lille ekstra, og brukt sensurveiledningene aktivt for å nå de høyeste vurderingskriteriene. Resultatene viser at vi har fått til både god databehandling og innsiktsfull analyse, samtidig som vi har dokumentert og strukturert arbeidet på en måte som andre kan bygge videre på.

## Forbedringspunkter

Til et lignende prosjekt i fremtiden ønsker vi å forbedre følgende:
- **Brukervennlighet:** Vi skulle gjerne laget et grensesnitt der brukeren selv kan velge by og tidsrom for analysen, for å gjøre verktøyet mer tilgjengelig for flere.
- **Struktur fra start:** En enda tydeligere mappestruktur og rollefordeling i starten hadde gjort prosessen enklere og mer oversiktlig.
- **Tidlig testing:** Enhetstesting burde vært introdusert tidligere, særlig ved transformasjon og datarensing. Dette ville gjort det lettere å oppdage og rette feil tidlig.

For å implementere disse forbedringene vil vi neste gang etablere en tydelig prosjektplan fra første dag, sette opp et minimum av enhetstester tidlig i prosjektet og vurdere bruk av dashbord eller webgrensesnitt for å øke brukervennligheten.

## Videre utviklingspotensial

Vi har mange idéer til videreutvikling, blant annet:
- Utvide med flere miljøparametere som støy, trafikk og fuktighet.
- Lage en sanntidsbasert visualiseringsplattform på nett for å gjøre analysene tilgjengelige for flere.
- Koble miljødata med helsedata eller policy-endringer for å utforske sammenhenger på tvers av fagfelt.
- Bruke erfaringene fra prosjektet i andre sammenhenger, for eksempel i sommerjobb, praksis eller tverrfaglige studentprosjekter.

## Oppsummering og personlig utbytte

Vi har lært mye om både datavitenskap og miljøspørsmål. Viktigheten av planlegging, struktur, dokumentasjon og ryddig kode er noe vi tar med oss videre. Prosjektet har gjort oss bedre rustet til større prosjekter, både i studier og arbeidsliv. Prosjektet har også endret vårt syn på datavitenskap: Det handler ikke bare om programmering, men like mye om samarbeid, kommunikasjon og kritisk tenkning.
**(Refleksjonsnotatet kunne vært mer utdypende, men vi hadde maks 800 ord å forholde oss til.)**

### [**Til samlesiden**](../docs/samleside.md)