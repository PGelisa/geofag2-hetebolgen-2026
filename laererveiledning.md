# Hetebølgen i Europa juni 2026 – lærerveiledning

Økt på 120 minutter i Geofag 2. Elevene jobber i `hetebolgen_2026.ipynb` i JupyterLab i conda-miljøet `geofag2`. Notatboken bruker bare pakkene fra Miniforge-guiden (numpy, pandas, matplotlib, xarray, netcdf4, cartopy).

**Faglig innhold:** høytrykk og blokkering, geopotensiell høyde, luftmasser (temperatur i 850 hPa), tørradiabatisk oppvarming av synkende luft, energibalansen ved bakken (tørr jord, klar himmel), avvik fra normalen, lange tidsserier og forskyvning av fordelinger, attribusjon, hetebølgedefinisjoner, og reanalyse sammenlignet med stasjonsdata.

## Mappestruktur

```
hetebolgen-2026/
├── hetebolgen_2026.ipynb          elevnotatboken
├── hent_data_hetebolgen.py        kjøres én gang av læreren
├── laererveiledning.md
└── data/                          fylles av skriptet
    ├── punkt_<by>.csv             ERA5 1940–2026 for 7 byer (Open-Meteo, ingen konto)
    ├── oisst_avvik.nc             avvik i havtemperatur juni–juli 2026
    ├── stasjon_<navn>.csv         Blindern, Todokk og Florida (Frost, krever klient-ID)
    ├── era5_tmaks.nc              høyeste temperatur per døgn, juni–juli 2026
    ├── era5_tmiddel.nc            døgnmiddeltemperatur, juni–juli 2026
    ├── era5_trykkflater.nc        500 hPa-flaten og temperatur i 850 hPa, 10.06–20.07
    ├── era5_klima_t2m.nc          normal 1991–2020 for juni og juli
    └── era5_klima_z500.nc         normal 1991–2020 for juni og juli
```

## Forberedelse (ca. 30–45 min, én gang)

1. **CDS-konto for ERA5.** Lag konto på cds.climate.copernicus.eu, godta lisensen for ERA5, og legg API-nøkkelen i `~/.cdsapirc`. Installer `conda install -c conda-forge cdsapi`.
2. **Frost-klient-ID for norske stasjoner.** Gratis på frost.met.no. Velg «Request client credentials», og du får en klient-ID på e-post.
3. Kjør skriptet fra mappen `hetebolgen-2026`:
   ```
   conda activate geofag2
   python hent_data_hetebolgen.py --alt --frost DIN-KLIENT-ID
   ```
   ERA5-bestillingene kan bli liggende i kø hos Copernicus i flere minutter.
4. Åpne notatboken og kjør alle cellene (Run → Run All Cells). Sjekk figurene og fyll inn tallene merket ☐ nedenfor.

Filene lagres komprimert. Anslått samlet størrelse er 15–25 MB, så de kan ligge i GitHub-repoet.

### ERA5 manuelt (hvis cdsapi ikke virker)

| Fil | Datasett | Variabel | Statistikk | Datoer | Område (N, V, S, Ø) |
|---|---|---|---|---|---|
| era5_tmaks | ERA5 post-processed daily statistics on single levels | 2m temperature | Daily maximum, UTC+00:00, 1-hourly | 01.06–31.07.2026 | 72, −25, 34, 40 |
| era5_tmiddel | samme | 2m temperature | Daily mean | 01.06–31.07.2026 | 72, −25, 34, 40 |
| era5_trykkflater | ERA5 post-processed daily statistics on pressure levels | Geopotential, Temperature, 500 og 850 hPa | Daily mean | 10.06–20.07.2026 | 75, −40, 28, 45 |
| klima t2m | ERA5 monthly averaged data on single levels | 2m temperature | Monthly averaged reanalysis | juni og juli 1991–2020 | 72, −25, 34, 40 |
| klima z500 | ERA5 monthly averaged data on pressure levels | Geopotential, 500 hPa | Monthly averaged reanalysis | juni og juli 1991–2020 | 75, −40, 28, 45 |

Skriptet gjør om enhetene (K til °C, geopotensial til gpdam), gir variablene norske navn, og lagrer trykkflatene på 0,5° for å spare plass. Har du lastet ned manuelt, er det enklest å legge filene i `data/` og tilpasse funksjonen `hent_era5()` slik at den åpner dem i stedet for å bestille dem på nytt.

### Stasjonsdata manuelt (uten Frost)

På seklima.met.no kan du laste ned høyeste og laveste temperatur per døgn for Oslo – Blindern (SN18700) og Nesbyen – Todokk (SN24890) som CSV. Lagre dem som `data/stasjon_blindern.csv` og `data/stasjon_todokk.csv` med kolonnene `dato,tmaks,tmin` (dato som ÅÅÅÅ-MM-DD). Uten stasjonsdata bruker notatboken ERA5 for Oslo og viser bare ERA5 for Nesbyen.

## Tidsplan

| Tid | Del | Merknad |
|---|---|---|
| 0–10 | Oppstart og hypotese | Vis gjerne satellittbildet av overflatetemperatur fra Sentinel-3 for 23.06.2026 |
| 10–30 | Del 1 Hvor varmt ble det? | 1a–1c |
| 30–55 | Del 2 Varmekuppelen | 2a–2c. 2c knytter an til tørradiabaten og energibalansen |
| 55–65 | Pause | |
| 65–90 | Del 3 Er dette klimaendringer? | 3a–3c. Kutt 3b hvis tiden blir knapp |
| 90–105 | Del 4 Hva med Norge? | 4a–4b |
| 105–120 | Del 5 Oppsummering | Skriftlig svar med tre tall. Skill mellom vær og klima |

Fordypning A (marin hetebølge) og B (tropenetter) er for elever som blir tidlig ferdige.

## Fakta til gjennomgangen

- **Copernicus (C3S), juli 2026.** Juni 2026 var den varmeste junimåneden som er målt i Vest-Europa, med 20,74 °C i snitt. Det er 3,06 °C over normalen for 1991–2020 og slo rekorden fra juni 2025. Hetebølgen varte omtrent fra 18. til 30. juni. Det var også marine hetebølger i det vestlige Middelhavet og langs atlanterhavskysten. Fennoskandia var våtere enn normalt i juni.
- **World Weather Attribution, 26. juni 2026.** Studien gjaldt 18.–29. juni. Hetebølgen ville vært omtrent 3,5 °C kaldere på dagtid i klimaet fra 1976 og omtrent 2 °C kaldere i klimaet fra 2003. Om natten var tallene 2,4 °C og 1,3 °C. El Niño spilte ingen rolle, og selve værmønsteret var ikke spesielt uvanlig. Av omtrent 850 byer som ble analysert, slo rundt 45 % sin rekord for varmestress.
- **Copernicus, oktober 2026.** Sommeren 2026 var den varmeste som er målt i Vest-Europa, 21,7 °C i snitt (+2,5 °C). Det slo rekorden fra 2003. Vest-Europa hadde 17 dager der minst 60 % av arealet hadde over 30 °C, mot 11 dager i 2003.
- **MET Norge, juli 2026.** Den høyeste temperaturen i juli var 34,2 °C på Nesbyen – Todokk den 15. juli. 30 stasjoner fikk ny julirekord, blant annet Kongsberg (33,6 °C) og Gardermoen (31,9 °C) den 16. juli. Likevel var juli som helhet nær normalen for landet (−0,1 °C), med store regionale forskjeller.
- **MET sin definisjon av norsk hetebølge.** Minst fem sammenhengende dager med høyeste temperatur på 27 °C eller mer.

## Løsningsforslag og stikkord

Fyll inn tallene merket ☐ når du har kjørt notatboken med ekte data.

**1a** ☐ varmeste område og hvor langt nord 35 °C nådde. ☐ varmeste by og dato. Stasjoner måler vanligvis høyere enn ERA5 på de varmeste dagene, fordi en rute på 25 × 25 km er et gjennomsnitt som jevner ut lokale topper (byer, dalbunner, tørr jord).

**1b** ☐ Toppen kom ikke samtidig overalt, fordi varmen flyttet seg med høytrykket. ☐ antall dager på rad over 30 °C i Paris.

**1c** Avviket er størst der det er uvanlig varmt for stedet, ikke nødvendigvis der det er varmest. Sør-Spania er varmt også i en normal juni, mens 35 °C i London er langt over normalen. ☐ eventuelle kalde områder (nordlige deler, nær tråg).

**2a** ☐ hvor H lå. Høytrykket i høyden lå nesten i ro i flere dager, med tråg på begge sider (omegamønster). Blokkeringen stenger lavtrykkene ute, og de blir ledet nord eller sør for høytrykket.

**2b** Varm luft fra Nord-Afrika og Den iberiske halvøy ble ført nordover på vestsiden av høytrykket. ☐ hvor langt nord 20 °C i 850 hPa nådde.

**2c** Tørradiabatisk oppvarming: luft på 1,5 km høyde med 22 °C blir 22 + 15 = 37 °C hvis den synker til bakken uten å bli blandet. På de varmeste dagene ligger den stiplede kurven nær den målte temperaturen, så synkende og varm luft forklarer mye av varmen. Andre faktorer: klar himmel gir mye kortbølget innstråling, og tørr jord gjør at energien går til å varme opp luften (følbar varme) i stedet for til fordampning (latent varme). Dette er et godt sted å skille mellom strålingsbalanse og energibalanse.

**3a** ☐ forskjell mellom 1951–1980 og 1996–2025, og 2026 sammenlignet med 1976 og 2003. Pek på at ERA5 er mer usikker de første tiårene, fordi det var færre målinger.

**3b** ☐ antall dager per periode. Den relative økningen er større for høyere terskler, fordi halen av fordelingen er tynn. En liten forskyvning gir da stor relativ økning.

**3c** Hele fordelingen er forskjøvet mot varmere verdier. ☐ forskjell i middelverdi og i antall dager over terskelen. Kobling til WWA: værmønsteret var vanlig, men det skjedde i et varmere klima, så samme mønster gir høyere temperatur. Det er forskjellen mellom vær og klima.

**4a** ☐ antall hetebølger 1961–1990 og 1991–2020 i Oslo, og om det var hetebølge i 2026. Med lavere terskel blir det mange flere hetebølger. Definisjonen avgjør tallene, og ulike land bruker ulike terskler.

**4b** ☐ forskjell mellom ERA5 og stasjonen. Nesbyen ligger i en dalbunn med lite vind, der luften blir varmet av solvendte dalsider og ikke blir blandet med kjøligere luft. ERA5-ruten tar også med fjellområder, så gjennomsnittet blir lavere.

## Om dataene

- **ERA5** er en reanalyse med ruter på omtrent 0,25° × 0,25°. Døgnstatistikken fra Copernicus er regnet i UTC. Punktseriene fra Open-Meteo er regnet i lokal tid, så de kan avvike litt fra kartene.
- **Open-Meteo** leverer ERA5 som punktserier uten konto (CC BY 4.0, «Weather data by Open-Meteo.com»).
- **OISST v2.1** gir avvik fra normalen for 1991–2020.
- **Status for testingen.** Notatboken er kjørt fra start til slutt med syntetiske testdata, ikke med de ekte filene, fordi Copernicus, Open-Meteo, Frost og NOAA ikke var tilgjengelige der notatboken ble laget. Første gang du kjører med ekte data, bør du se ekstra nøye på ERA5-filene fra døgnstatistikken (zip-format og variabelnavn), på Frost-svaret og på stasjonsnumrene.

## Kilder

- Copernicus Climate Change Service (2026). *Record heatwave brings hottest June for western Europe during second-warmest June globally*. Pressemelding 9. juli 2026.
- Copernicus Climate Change Service (2026). *Record heat stress and low river flows marked Europe's 2026 summer*. Pressemelding 2. oktober 2026.
- World Weather Attribution (2026). Hurtigstudie av hetebølgen i Vest-Europa 18.–29. juni 2026, publisert 26. juni 2026.
- Meteorologisk institutt (2026). *Været i Norge. Klimatologisk månedsoversikt juli 2026*. MET info 7/2026.
- Meteorologisk institutt. *Hetebølger*. met.no
- Hersbach mfl. (2020). ERA5. *QJRMS* 146, 1999–2049.
- Huang mfl. (2021). NOAA OISST v2.1. *J. Climate* 34, 2923–2939.
