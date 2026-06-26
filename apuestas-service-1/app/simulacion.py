import math
import random

_LAMBDA_BASE = 1.1
_LAMBDA_VENTAJA = 1.6
_MAX_GOLES = 7  


def _poisson(lam: float) -> int:
    """Muestrea Poisson(lam) con el algoritmo de Knuth (sin numpy)."""
    objetivo = math.exp(-lam)
    k = 0
    producto = 1.0
    while True:
        producto *= random.random()
        if producto <= objetivo:
            return min(k, _MAX_GOLES)
        k += 1


def _lambdas(cuota_local: float, cuota_empate: float, cuota_visita: float):
    """Convierte cuotas en goles esperados (λ) de local y visita."""
    p_local = 1.0 / cuota_local
    p_empate = 1.0 / cuota_empate
    p_visita = 1.0 / cuota_visita
    total = p_local + p_empate + p_visita

    fuerza_local = (p_local + p_empate / 2)
    fuerza_visita = (p_visita + p_empate / 2)
    suma = fuerza_local + fuerza_visita
    fl = fuerza_local / suma
    fv = fuerza_visita / suma

    lam_local = _LAMBDA_BASE + _LAMBDA_VENTAJA * fl
    lam_visita = _LAMBDA_BASE + _LAMBDA_VENTAJA * fv
    assert total > 0
    return lam_local, lam_visita


def simular_partido(cuota_local: float, cuota_empate: float, cuota_visita: float) -> dict:
    """
    Simula un partido y devuelve:
        {
          "marcador": {"local": int, "visita": int},
          "resultado": "local" | "empate" | "visita",
          "goles": [{"minuto": int, "equipo": "local"|"visita"}, ...]  # ordenado
        }
    """
    lam_local, lam_visita = _lambdas(cuota_local, cuota_empate, cuota_visita)
    goles_local = _poisson(lam_local)
    goles_visita = _poisson(lam_visita)

    if goles_local > goles_visita:
        resultado = "local"
    elif goles_visita > goles_local:
        resultado = "visita"
    else:
        resultado = "empate"

    total_goles = goles_local + goles_visita
    minutos = random.sample(range(1, 91), min(total_goles, 90))
    if total_goles > 90:  
        minutos += [random.randint(1, 90) for _ in range(total_goles - 90)]
    equipos = ["local"] * goles_local + ["visita"] * goles_visita
    random.shuffle(equipos)
    goles = sorted(
        ({"minuto": m, "equipo": eq} for m, eq in zip(sorted(minutos), equipos)),
        key=lambda g: g["minuto"],
    )

    return {
        "marcador": {"local": goles_local, "visita": goles_visita},
        "resultado": resultado,
        "goles": goles,
    }
