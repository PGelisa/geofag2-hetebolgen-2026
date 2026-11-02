# Hetebølgen i Europa juni 2026

Dataoppgave i Geofag 2 (REA3043) om hetebølgen i Vest-Europa 18.–30. juni 2026, med en egen del om varmen i Sør-Norge i juli. Økten tar 120 minutter.

Elevene bruker ekte data til å svare på hvorfor det ble så varmt, og hvor mye av varmen som kan knyttes til klimaendringer. De ser på varmekuppelen i høyden, sammenligner lange tidsserier fra 1940 til i dag og tester MET sin definisjon av hetebølge på data fra Oslo.

## For elever

**Se notatboken uten å installere noe.** Trykk på `hetebolgen_2026_kjort.ipynb` i fillisten ovenfor. Det er en ferdig kjørt versjon, så du ser alle figurene og tallene rett i nettleseren.

**Vil du kjøre koden selv**, trenger du conda-miljøet `geofag2` og mappen `Geofag2-filer` fra guiden [Installere og åpne Jupyter Lab](https://pgelisa.github.io/geofag2-python-opendrift/).

**Hent filene**

1. Trykk den grønne knappen **Code** øverst på denne siden og velg **Download ZIP**.
2. Flytt zip-filen fra Nedlastinger til mappen `Geofag2-filer` før du pakker den ut. Mappen lager du i steg 3 i guiden.
   - **Mac:** dobbeltklikk zip-filen i `Geofag2-filer`.
   - **Windows:** høyreklikk zip-filen og velg **Pakk ut alle**. Velg `Geofag2-filer` som mål.
3. Slett zip-filen fra Nedlastinger.

Finner du ikke `Geofag2-filer`? Skriv `cd Geofag2-filer` i Terminal (Mac) eller Miniforge Prompt (Windows), og deretter `open .` (Mac) eller `explorer .` (Windows). Da åpnes mappen i Finder eller Filutforsker.

Kan du bruke git, går det også fint med `git clone`.

**Åpne notatboken**

```
conda activate geofag2
cd Geofag2-filer
jupyter lab
```

Gå til mappen du pakket ut, og åpne `hetebolgen_2026.ipynb`. Mappen `data` må ligge ved siden av notatboken.

## Hva kan du endre?

I cellene merket 🔧 kan du endre verdier og kjøre cellen på nytt. Dataene dekker bare en bestemt periode og et bestemt område, så hold deg innenfor tabellene nedenfor. I 2a og 2b får du en feilmelding hvis datoen ikke finnes i dataene. Andre steder får du et tomt eller avkortet resultat.

| Del | Variabel | Dette kan du velge |
|---|---|---|
| 1a | `START`, `SLUTT` | En periode fra 01.06 til 31.07.2026. Gjelder også 1b, 1c og fordypning A |
| 1b | `VALGTE` | Noen av byene Madrid, Paris, London, Berlin, Oslo, Nesbyen og Bergen |
| 2a, 2b | `DATOER` | Tre datoer fra 10.06 til 20.07.2026 |
| 2c | `BY` | En av de sju byene |
| 2c | `HOYDE_M` | Høyden (m) luften i 850 hPa synker fra |
| 3a–3c | `BY` | En av de sju byene |
| 3b | `TERSKEL` | Temperaturgrensen (°C) for en varm dag |
| 4a | `TERSKEL_N`, `DAGER_N` | Grensen (°C) og antall dager på rad i definisjonen av hetebølge |
| B | `BY_B` | En av de sju byene |

Avviket i 1c regnes mot normalen for måneden `START` ligger i. Velger du en periode som går fra juni inn i juli, blir hele perioden sammenlignet med juninormalen.

**Hva dataene dekker**

| Data | Periode | Område | Oppløsning |
|---|---|---|---|
| Høyeste temperatur og døgnmiddel (ERA5) | 01.06–31.07.2026 | 34–72° N, 25° V–40° Ø | Ett kart per døgn, 0,25° |
| 500 hPa-flaten og temperatur i 850 hPa (ERA5) | 10.06–20.07.2026 | 28–75° N, 40° V–45° Ø | Ett kart per døgn, 0,5° |
| Normaler 1991–2020 (ERA5) | Bare juni og juli | Som kartene ovenfor | Månedsmiddel |
| Punktserier for sju byer (ERA5) | 01.01.1940–30.09.2026 | Én rute per by | Ett tall per døgn |
| Oslo – Blindern (MET) | 01.01.1937–30.09.2026 | Stasjon | Ett tall per døgn. Januar og februar 1937 mangler |
| Nesbyen – Todokk (MET) | 21.11.2003–30.09.2026 | Stasjon | Ett tall per døgn |
| Avvik i havtemperatur (OISST) | 01.06–31.07.2026 | 30–62° N, 25° V–40° Ø | Ett kart per døgn. 08.06 og 18.07 mangler |

Punktseriene går bare til 30. september 2026, så 2026 er ikke et helt år. For sommeren betyr det ingenting, men årsverdier for 2026 må du tolke med forsiktighet. Stasjonen på Todokk startet i 2003, så den egner seg ikke til lange serier.

## For lærere

Se [laererveiledning.md](laererveiledning.md) for tidsplan, fakta, løsningsforslag og hvordan du henter dataene med `hent_data_hetebolgen.py`.

## Datakilder

- ERA5 (Copernicus Climate Change Service, ECMWF), kart og normaler
- ERA5 punktserier 1940–2026 via Open-Meteo (Weather data by Open-Meteo.com, CC BY 4.0)
- Stasjonsdata fra Meteorologisk institutt (Frost API)
- Havtemperatur: NOAA OISST v2.1
- Bakgrunn: Copernicus Climate Change Service, World Weather Attribution og MET Norge

Laget av Elisabeth Engum, Amalie Skram videregående skole.
