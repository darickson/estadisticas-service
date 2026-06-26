import os

import requests

SPORTSDB_KEY = os.getenv("SPORTSDB_KEY", "123")
LIGA_DEFECTO = os.getenv("SPORTSDB_LIGA", "4335")
LIGA_NOMBRE = os.getenv("SPORTSDB_LIGA_NOMBRE", "Spanish La Liga")
_BASE = "https://www.thesportsdb.com/api/v1/json"
_TIMEOUT = 6  


def obtener_equipos(liga_id: str = LIGA_DEFECTO) -> list[dict]:
    """
    Devuelve [{'nombre': str, 'badge': str|None}, ...] de los equipos de la liga.
    Lista vacía si la API falla (sin lanzar excepción).
    """
    url = f"{_BASE}/{SPORTSDB_KEY}/lookup_all_teams.php?id={liga_id}"
    try:
        resp = requests.get(url, timeout=_TIMEOUT)
        resp.raise_for_status()
        data = resp.json() or {}
    except Exception as err:
        print(f"[sportsdb] sin datos ({err}); se usará fallback", flush=True)
        return []

    equipos = []
    for t in (data.get("teams") or []):
        nombre = (t.get("strTeam") or "").strip()
        badge = t.get("strBadge") or t.get("strTeamBadge") or None
        liga = (t.get("strLeague") or LIGA_NOMBRE).strip()
        if nombre:
            equipos.append({"nombre": nombre, "badge": badge, "liga": liga})
    print(f"[sportsdb] {len(equipos)} equipos obtenidos de liga {liga_id}", flush=True)
    return equipos


def buscar_equipo(nombre: str) -> dict | None:
    """
    Busca un club por nombre y devuelve {'nombre','badge','liga'} con su escudo
    real. Sirve para sembrar equipos famosos/históricos (Real Madrid, Boca, etc.).
    Devuelve None si la API falla o no hay coincidencia.
    """
    url = f"{_BASE}/{SPORTSDB_KEY}/searchteams.php"
    try:
        resp = requests.get(url, params={"t": nombre}, timeout=_TIMEOUT)
        resp.raise_for_status()
        teams = (resp.json() or {}).get("teams") or []
    except Exception as err:  # noqa: BLE001
        print(f"[sportsdb] búsqueda '{nombre}' falló ({err})", flush=True)
        return None
    if not teams:
        return None
    t = teams[0]
    return {
        "nombre": (t.get("strTeam") or nombre).strip(),
        "badge": t.get("strBadge") or t.get("strTeamBadge") or None,
        "liga": (t.get("strLeague") or "").strip() or None,
    }
