import shutil
import sys
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
COLS_T = ["t1_seg", "t2_seg", "t3_seg"]


def promedio_minutos(fila):
    tiempos = []
    for c in COLS_T:
        try:
            tiempos.append(float(str(fila.get(c, "")).replace(",", ".")))
        except ValueError:
            pass
    return round(sum(tiempos) / len(tiempos) / 60, 2) if tiempos else None


def actualizar(ruta_hoja, ruta_aristas=RAIZ / "datos" / "aristas.csv"):
    hoja = pd.read_csv(ruta_hoja, dtype=str, keep_default_na=False)
    aristas = pd.read_csv(ruta_aristas, dtype=str, keep_default_na=False)
    shutil.copy(ruta_aristas, str(ruta_aristas) + ".bak")
    cambios = 0
    for _, f in hoja.iterrows():
        p = promedio_minutos(f)
        if p is None:
            continue
        mask = ((aristas["origen"] == f["origen"]) & (aristas["destino"] == f["destino"])) | \
               ((aristas["origen"] == f["destino"]) & (aristas["destino"] == f["origen"]))
        if mask.any():
            aristas.loc[mask, "peso"] = str(p)
            aristas.loc[mask, "estado"] = "MEDIDO"
            aristas.loc[mask, "fuente"] = f"Cronometraje propio {f.get('fecha', '')} ({f.get('responsable', '')})".strip()
            cambios += 1
    aristas.to_csv(ruta_aristas, index=False, lineterminator="\n")
    return cambios


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    print(f"Tramos actualizados: {actualizar(sys.argv[1])} (copia de seguridad en aristas.csv.bak)")
