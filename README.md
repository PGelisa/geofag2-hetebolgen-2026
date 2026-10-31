# Hetebølgen i Europa juni 2026

Dataoppgave i Geofag 2 (REA3043) om hetebølgen i Vest-Europa 18.–30. juni 2026, med en egen del om varmen i Sør-Norge i juli. Økten tar 120 minutter.

Elevene bruker ekte data til å svare på hvorfor det ble så varmt, og hvor mye av varmen som kan knyttes til klimaendringer. De ser på varmekuppelen i høyden, sammenligner lange tidsserier fra 1940 til i dag og tester MET sin definisjon av hetebølge på data fra Oslo.

## For elever

Du trenger conda-miljøet `geofag2` fra guiden [Installere og åpne Jupyter Lab](https://github.com/Realfag-AmalieSkram/Geofag2-python).

**Hent filene**

1. Trykk den grønne knappen **Code** øverst på denne siden og velg **Download ZIP**.
2. Flytt zip-fila fra Nedlastinger til geofag-mappen din før du pakker den ut.
   - **Mac:** dobbeltklikk zip-fila i geofag-mappen.
   - **Windows:** høyreklikk zip-fila og velg **Pakk ut alle**. Velg geofag-mappen som mål.
3. Slett zip-fila fra Nedlastinger.

Kan du bruke git, går det også fint med `git clone`.

**Åpne notatboken**

```
conda activate geofag2
jupyter lab
```

Gå til mappen du pakket ut, og åpne `hetebolgen_2026.ipynb`. Mappen `data` må ligge ved siden av notatboken.

## For lærere

Se [laererveiledning.md](laererveiledning.md) for tidsplan, fakta, løsningsforslag og hvordan du henter dataene med `hent_data_hetebolgen.py`.

## Datakilder

- ERA5 (Copernicus Climate Change Service, ECMWF), kart og normaler
- ERA5 punktserier 1940–2026 via Open-Meteo (Weather data by Open-Meteo.com, CC BY 4.0)
- Stasjonsdata fra Meteorologisk institutt (Frost API)
- Havtemperatur: NOAA OISST v2.1
- Bakgrunn: Copernicus Climate Change Service, World Weather Attribution og MET Norge

Laget av Elisabeth Engum, Amalie Skram videregående skole.
