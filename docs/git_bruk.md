
# 🔁 Vår bruk av Git i prosjektet

Gjennom hele prosjektet har vi brukt Git og GitHub aktivt for å holde oversikt, samarbeide effektivt og jobbe strukturert. Her reflekterer vi over hvordan vi har brukt verktøyene, hvilke erfaringer vi har gjort oss, og hva vi har lært underveis.

---

## ✅ Hvordan vi har brukt Git

###  Feature branches og oppgavedeling
Vi har jobbet mye med feature branches, der hver oppgave har fått sin egen gren. Dette gjorde det mulig å jobbe parallelt og uavhengig uten at vi forstyrret arbeidet til hverandre eller skapte problemer i `main`.

Vi har stort sett laget en branch for hver GitHub Issue, og denne har vært dedikert til å løse én konkret oppgave. Dette har gitt god struktur, gjort det enkelt å koble commits til spesifikke behov, og hjulpet oss å jobbe målrettet.

###  Issues og pull requests
Vi har brukt GitHub Issues til å fordele arbeidsoppgaver, dokumentere fremdrift og diskutere løsninger. Pull requests ble brukt for å gjøre endringer gjennomsiktige, slik at vi kunne se på og vurdere hverandres arbeid før det ble lagt inn i `main`.

Gjennom å bruke pull requests har vi også blitt flinkere til å skrive presise og forståelige commit-meldinger og beskrivelser, noe som hjelper både oss selv og andre til å forstå hva som er gjort og hvorfor.

---

## ⚠️ Erfaringer og lærdom

Selv om vi har hatt en strukturert tilnærming til Git, har vi også møtt noen utfordringer som vi har lært mye av:

###  Direkte commits til `main`
Tidlig i prosjektet opplevde vi at det ved noen anledninger ble gjort commits direkte til `main`, uten at endringene var knyttet til en pull request eller issue. Dette gjorde det vanskelig å holde oversikt over hva som ble endret og hvorfor, og skapte risiko for at feil kunne snike seg inn uten gjennomgang. Etter disse erfaringene ble vi mer bevisste på viktigheten av å jobbe via egne grener og bruke pull requests – noe som har ført til en ryddigere arbeidsflyt og bedre kontroll på endringer.


###  Merge conflicts
Vi opplevde også merge conflicts når to personer hadde jobbet parallelt med samme fil. Dette lærte oss viktigheten av å:
- Holde egne grener oppdatert med `main`
- Kommunisere tidlig om hvem som jobber på hva
- Merge ofte og i mindre biter

###  Mer bevissthet rundt git-historikk
Etter hvert har vi blitt mer bevisste på hvordan vi bruker commit-meldinger, branch-navn og pull requests til å dokumentere prosessen. Dette har gjort det enklere å navigere i prosjektet og finne tilbake til tidligere beslutninger.

###  Vi burde brukt en `dev`-branch

Underveis i prosjektet innså vi at det kunne vært en fordel å ha en egen `dev`-branch som alt arbeid kunne merges inn i før det eventuelt ble lagt til `main`. Vi valgte å ikke endre arbeidsflyten midt i prosjektet, siden det allerede fungerte greit, men hadde vi startet på nytt, ville vi implementert dette.

En `dev`-gren kunne fungert som en trygg mellomstasjon for å samle og teste endringer før de slippes til `main`. Dette ville gjort det enklere å sikre at `main` alltid inneholder kjørbar og stabil kode, og redusert risikoen for feil ved ferdigstilling.

Vi har lært at en `dev`-branch gir bedre struktur, mer forutsigbarhet i samarbeid, og er nyttig når man jobber på tvers av flere features eller personer.



---

## 🧠 Oppsummert

Git har vært en viktig del av prosjektet vårt – ikke bare for versjonskontroll, men som et samarbeidsverktøy. Vi har lært hvordan man organiserer arbeidet, hvordan man unngår konflikter, og hvordan man bruker issues og pull requests til å skape struktur og trygghet i utviklingsarbeidet. 

