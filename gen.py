#!/usr/bin/env python3
"""Genera inventories/lab.ini: 3 regiones x 3 tiers, 5 hosts por region."""
from pathlib import Path

REGIONES = {"pa": "10.10", "va": "10.20", "az": "10.30"}
TIERS = {
    "web": {"subred": 0, "cantidad": 2},
    "app": {"subred": 1, "cantidad": 2},
    "iac": {"subred": 2, "cantidad": 1},
}
IP_INICIO = 11
RAIZ = Path(__file__).resolve().parent
SALIDA = RAIZ / "inventories" / "lab.ini"


def main():
    lineas = [
        "[all:vars]",
        "ansible_user=ansible",
        f"ansible_ssh_private_key_file={RAIZ / 'keys' / 'id_ed25519'}",
        "",
    ]
    for region, prefijo in REGIONES.items():
        for tier, cfg in TIERS.items():
            lineas.append(f"[{region}_{tier}]")
            for n in range(cfg["cantidad"]):
                nombre = f"{region}-{tier}-{n + 1:02d}"
                ip = f"{prefijo}.{cfg['subred']}.{IP_INICIO + n}"
                lineas.append(f"{nombre} ansible_host={ip}")
            lineas.append("")
    for tier in TIERS:
        lineas.append(f"[{tier}:children]")
        lineas += [f"{region}_{tier}" for region in REGIONES]
        lineas.append("")
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    SALIDA.write_text("\n".join(lineas))
    print(f"Escrito: {SALIDA}")


if __name__ == "__main__":
    main()
