"""
Henter data om hetebølgen i Europa i juni 2026 til elevoppgaven i Geofag 2.

Kjøres ÉN gang av læreren. Filene havner i mappen data/ ved siden av
skriptet og kan legges i repoet, slik at elevene slipper å laste ned noe.

Bruk (i terminalen, med miljøet aktivert):

    conda activate geofag2
    python hent_data_hetebolgen.py                    # punktserier + havtemperatur
    python hent_data_hetebolgen.py --era5             # + ERA5-kart (krever CDS-konto)
    python hent_data_hetebolgen.py --frost KLIENT-ID  # + norske stasjonsdata fra MET
    python hent_data_hetebolgen.py --alt --frost KLIENT-ID

Ekstra pakke som bare læreren trenger (for --era5):

    conda install -c conda-forge cdsapi

Datakilder
----------
- Punktserier 1940–2026: ERA5 via Open-Meteo (ingen konto)
- Kart: ERA5 daglig statistikk og månedsmidler (Copernicus Climate Data Store)
- Norske stasjoner: MET Norge, Frost API (gratis klient-ID på frost.met.no)
- Havtemperatur: NOAA OISST v2.1, avvik fra 1991–2020 (CoastWatch ERDDAP)
"""

import argparse
import sys
import zipfile
from pathlib import Path
from urllib.parse import quote

import pandas as pd
import requests
import xarray as xr

DATA = Path(__file__).resolve().parent / "data"
DATA.mkdir(exist_ok=True)

# Byer for punktseriene (breddegrad, lengdegrad)
BYER = {
    "Madrid": (40.42, -3.70),
    "Paris": (48.85, 2.35),
    "London": (51.51, -0.13),
    "Berlin": (52.52, 13.40),
    "Oslo": (59.94, 10.72),
    "Nesbyen": (60.57, 9.11),
    "Bergen": (60.38, 5.33),
}

# MET-stasjoner for Frost (sjekk gjerne nummeret på seklima.met.no)
STASJONER = {
    "Oslo - Blindern": "SN18700",
    "Nesbyen - Todokk": "SN24890",
    "Bergen - Florida": "SN50540",
}


def lagre(ds, fil):
    """Komprimert NetCDF med 32-biters tall (små filer)."""
    enc = {v: {"zlib": True, "complevel": 4, "dtype": "float32"} for v in ds.data_vars}
    ds.to_netcdf(fil, encoding=enc)


def filnavn(by):
    return by.lower().replace(" ", "_").replace("ø", "o").replace("å", "a").replace("æ", "ae")


# ---------------------------------------------------------------------------
# 1 Punktserier 1940–2026 fra ERA5 (Open-Meteo)
# ---------------------------------------------------------------------------
def hent_punktserier():
    print("Henter punktserier 1940–2026 (ERA5 via Open-Meteo) ...")
    url = "https://archive-api.open-meteo.com/v1/archive"
    for by, (lat, lon) in BYER.items():
        r = requests.get(url, timeout=300, params={
            "latitude": lat, "longitude": lon,
            "start_date": "1940-01-01", "end_date": "2026-09-30",
            "daily": "temperature_2m_max,temperature_2m_min",
            "timezone": "auto", "models": "era5"})
        r.raise_for_status()
        d = r.json()["daily"]
        df = pd.DataFrame({"dato": d["time"], "tmaks": d["temperature_2m_max"],
                           "tmin": d["temperature_2m_min"]})
        fil = f"punkt_{filnavn(by)}.csv"
        df.to_csv(DATA / fil, index=False)
        print(f"  {fil} ({len(df)} dager)")


# ---------------------------------------------------------------------------
# 2 Norske stasjoner fra Frost (MET Norge)
# ---------------------------------------------------------------------------
def hent_frost(klient_id):
    print("Henter stasjonsdata fra Frost (MET Norge) ...")
    url = "https://frost.met.no/observations/v0.jsonld"
    for navn, sn in STASJONER.items():
        r = requests.get(url, auth=(klient_id, ""), timeout=300, params={
            "sources": sn,
            "elements": "max(air_temperature P1D),min(air_temperature P1D)",
            "referencetime": "1937-01-01/2026-10-01",
            "timeoffsets": "default", "levels": "default"})
        if r.status_code != 200:
            print(f"  {navn}: feil {r.status_code} {r.text[:200]}")
            continue
        rader = [(d["referenceTime"][:10], o["elementId"], o["value"])
                 for d in r.json()["data"] for o in d["observations"]]
        df = (pd.DataFrame(rader, columns=["dato", "element", "verdi"])
                .pivot_table(index="dato", columns="element", values="verdi", aggfunc="first")
                .rename(columns={"max(air_temperature P1D)": "tmaks",
                                 "min(air_temperature P1D)": "tmin"})
                .reset_index())
        fil = f"stasjon_{filnavn(navn.split(' - ')[-1])}.csv"
        df.to_csv(DATA / fil, index=False)
        print(f"  {fil} ({len(df)} dager, {df.dato.min()} til {df.dato.max()})")


# ---------------------------------------------------------------------------
# 3 Havtemperaturavvik fra OISST
# ---------------------------------------------------------------------------
def hent_oisst():
    print("Henter avvik i havtemperatur (OISST) ...")
    base = "https://coastwatch.pfeg.noaa.gov/erddap/griddap/ncdcOisst21Agg_LonPM180.nc"
    q = ("anom[(2026-06-01T12:00:00Z):1:(2026-07-31T12:00:00Z)][(0.0):1:(0.0)]"
         "[(30.0):1:(62.0)][(-25.0):1:(40.0)]")
    r = requests.get(base + "?" + quote(q, safe="():,.-"), timeout=600)
    r.raise_for_status()
    tmp = DATA / "_tmp_oisst.nc"
    tmp.write_bytes(r.content)
    with xr.open_dataset(tmp) as ds:
        ds = ds.load().rename({"latitude": "lat", "longitude": "lon"}).isel(zlev=0, drop=True)
        ds["time"] = ds.time.dt.floor("D")
        lagre(ds[["anom"]].sortby("lat"), DATA / "oisst_avvik.nc")
    tmp.unlink()
    print("  oisst_avvik.nc")


# ---------------------------------------------------------------------------
# 4 ERA5 (krever konto på https://cds.climate.copernicus.eu og ~/.cdsapirc)
# ---------------------------------------------------------------------------
OMR_BAKKE = [72, -25, 34, 40]     # N, V, S, Ø
OMR_LUFT = [75, -40, 28, 45]


def dager(start, slutt):
    return pd.date_range(start, slutt, freq="D")


def apne(fil):
    """CDS leverer daglig statistikk som zip med NetCDF-filer."""
    if zipfile.is_zipfile(fil):
        mappe = fil.with_suffix("")
        with zipfile.ZipFile(fil) as z:
            z.extractall(mappe)
        filer = sorted(mappe.glob("*.nc"))
        ds = xr.merge([xr.open_dataset(f).load() for f in filer], compat="override")
        for f in filer:
            f.unlink()
        mappe.rmdir()
    else:
        ds = xr.open_dataset(fil).load()
    fil.unlink()
    navn = {"valid_time": "time", "latitude": "lat", "longitude": "lon",
            "pressure_level": "nivaa"}
    ds = ds.rename({k: v for k, v in navn.items() if k in ds.variables})
    ds = ds.drop_vars([v for v in ["expver", "number"] if v in ds.variables])
    return ds.sortby("lat")


def hent_era5():
    import cdsapi

    c = cdsapi.Client()

    def daglig(dataset, variabler, stat, start, slutt, omraade, nivaa=None):
        dd = dager(start, slutt)
        biter = []
        for (aar, mnd), gruppe in dd.to_series().groupby([dd.year, dd.month]):
            req = {"product_type": "reanalysis", "variable": variabler,
                   "year": str(aar), "month": f"{mnd:02d}",
                   "day": [f"{d:02d}" for d in gruppe.index.day],
                   "daily_statistic": stat, "time_zone": "utc+00:00",
                   "frequency": "1_hourly", "area": omraade}
            if nivaa:
                req["pressure_level"] = nivaa
            tmp = DATA / f"_tmp_{stat}_{aar}{mnd:02d}.zip"
            c.retrieve(dataset, req, str(tmp))
            biter.append(apne(tmp))
        return xr.concat(biter, dim="time")

    print("ERA5: høyeste temperatur hvert døgn ...")
    ds = daglig("derived-era5-single-levels-daily-statistics", ["2m_temperature"],
                "daily_maximum", "2026-06-01", "2026-07-31", OMR_BAKKE)
    lagre((ds.rename({"t2m": "tmaks"}) - 273.15), DATA / "era5_tmaks.nc")

    print("ERA5: døgnmiddeltemperatur ...")
    ds = daglig("derived-era5-single-levels-daily-statistics", ["2m_temperature"],
                "daily_mean", "2026-06-01", "2026-07-31", OMR_BAKKE)
    lagre((ds.rename({"t2m": "tmiddel"}) - 273.15), DATA / "era5_tmiddel.nc")

    print("ERA5: geopotensial og temperatur i 500 og 850 hPa ...")
    ds = daglig("derived-era5-pressure-levels-daily-statistics",
                ["geopotential", "temperature"], "daily_mean",
                "2026-06-10", "2026-07-20", OMR_LUFT, nivaa=["500", "850"])
    ds = ds.coarsen(lat=2, lon=2, boundary="trim").mean()      # 0,5° holder
    ut = xr.Dataset({"z500": ds.z.sel(nivaa=500) / 9.80665 / 10,      # gpdam
                     "t850": ds.t.sel(nivaa=850) - 273.15})
    lagre(ut, DATA / "era5_trykkflater.nc")

    print("ERA5: klimatologi 1991–2020 for juni og juli ...")
    aar = [str(a) for a in range(1991, 2021)]
    felles = {"product_type": ["monthly_averaged_reanalysis"], "year": aar,
              "month": ["06", "07"], "time": ["00:00"],
              "data_format": "netcdf", "download_format": "unarchived"}
    tmp = DATA / "_tmp_klima_t2m.nc"
    c.retrieve("reanalysis-era5-single-levels-monthly-means",
               {**felles, "variable": ["2m_temperature"], "area": OMR_BAKKE}, str(tmp))
    t2m = apne(tmp).t2m
    tmp = DATA / "_tmp_klima_z.nc"
    c.retrieve("reanalysis-era5-pressure-levels-monthly-means",
               {**felles, "variable": ["geopotential"], "pressure_level": ["500"],
                "area": OMR_LUFT}, str(tmp))
    z = apne(tmp).z
    if "nivaa" in z.dims:
        z = z.isel(nivaa=0, drop=True)
    z = z.coarsen(lat=2, lon=2, boundary="trim").mean()
    mnd_t, mnd_z = t2m.time.dt.month, z.time.dt.month
    klima_t = (t2m.groupby(mnd_t).mean() - 273.15).rename(month="mnd")
    klima_z = (z.groupby(mnd_z).mean() / 9.80665 / 10).rename(month="mnd")
    lagre(xr.Dataset({"t2m": klima_t}), DATA / "era5_klima_t2m.nc")
    lagre(xr.Dataset({"z500": klima_z}), DATA / "era5_klima_z500.nc")
    print("  era5_klima_t2m.nc, era5_klima_z500.nc")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--era5", action="store_true", help="hent ERA5-kart (CDS-konto)")
    p.add_argument("--frost", metavar="KLIENT_ID", help="hent norske stasjonsdata")
    p.add_argument("--alt", action="store_true", help="punktserier, OISST og ERA5")
    a = p.parse_args()

    hent_punktserier()
    try:
        hent_oisst()
    except Exception as feil:  # noqa: BLE001
        print(f"  OISST feilet: {feil}")
    if a.frost:
        hent_frost(a.frost)
    if a.era5 or a.alt:
        hent_era5()
    print("\nFerdig. Filene ligger i", DATA)
    sys.exit(0)
