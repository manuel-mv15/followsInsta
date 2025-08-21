#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Herramienta simple (Linux/Windows) para Instagram (4 opciones):
1) Ver QUIÉN TE SIGUE (followers_*)
2) Ver A QUIÉNES SIGUES (following.html)
3) Comparar SEGUIDOS vs SEGUIDORES (quiénes no te siguen de vuelta)
4) Ver a QUIÉNES SEGUISTE y NO ACEPTARON (pending_follow_requests.html)

Reglas fijas (no se preguntan):
- Siempre abre enlaces en LOTES de 50 con PAUSA de 0.5s entre enlaces.
- Los archivos se buscan en una sola ruta por defecto elegida por el programador.
- Se generan archivos .txt con los usuarios y con los enlaces.
"""

from __future__ import annotations

import re
import sys
import time
import webbrowser
from pathlib import Path
from typing import Iterable, List, Set, Optional


# =========================
# Configuración por defecto
# =========================

SCRIPT_DIR = Path(__file__).resolve().parent

def _detectar_carpeta_dump() -> Path:
    """
    Heurística MUY SIMPLE:
    1) Si existe ./connections/followers_and_following => usarla.
    2) Si existe exactamente una carpeta "instagram-*/connections/followers_and_following" => usarla.
    3) Si no, usar carpeta del script.
    """
    direct = SCRIPT_DIR / "connections" / "followers_and_following"
    if direct.is_dir():
        return direct

    # buscar patrón instagram-*
    candidatos: List[Path] = []
    for hijo in SCRIPT_DIR.iterdir():
        if hijo.is_dir() and hijo.name.startswith("instagram-"):
            faf = hijo / "connections" / "followers_and_following"
            if faf.is_dir():
                candidatos.append(faf)

    if len(candidatos) == 1:
        return candidatos[0]

    # fallback
    return SCRIPT_DIR

DATA_DIR = _detectar_carpeta_dump()

# Nombres por convención de export de Instagram
FOLLOWING_FILE = DATA_DIR / "following.html"
PENDING_FILE   = DATA_DIR / "pending_follow_requests.html"
FOLLOWERS_GLOB = "followers_*.html"

# Parámetros fijos de apertura
BATCH_SIZE = 50
PAUSE_SEC  = 0.5


# =========================
# Utilidades
# =========================

USERNAME_REGEX = re.compile(r'href="https://www\.instagram\.com/([^/"]+)"')

def leer_texto(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")

def extraer_usernames_html(html: str) -> Set[str]:
    candidatos = set(USERNAME_REGEX.findall(html))
    basura = {"accounts", "explore", "reels", "p", "stories", "direct", "challenge", "web"}
    return {u for u in candidatos if u and u not in basura}

def a_enlaces(users: Iterable[str]) -> List[str]:
    return [f"https://www.instagram.com/{u}" for u in users]

def escribir_lineas(path: Path, lineas: Iterable[str]) -> None:
    path.write_text("\n".join(lineas) + ("\n" if lineas else ""), encoding="utf-8")

def abrir_en_batches(enlaces: List[str]) -> None:
    """
    Abre todos los enlaces en lotes fijos (50) con pausa de 0.5 s.
    Sin confirmaciones intermedias.
    """
    if not enlaces:
        print("No hay enlaces para abrir.")
        return
    total = len(enlaces)
    print(f"Abrir {total} enlaces en lotes de {BATCH_SIZE} (pausa {PAUSE_SEC}s)...")
    for i in range(0, total, BATCH_SIZE):
        lote = enlaces[i:i+BATCH_SIZE]
        print(f"  Lote {i//BATCH_SIZE + 1}: {len(lote)} enlaces")
        for link in lote:
            webbrowser.open_new_tab(link)
            time.sleep(PAUSE_SEC)


# =========================
# Cargas de datos
# =========================

def cargar_followers() -> Set[str]:
    archivos = sorted([p for p in DATA_DIR.glob(FOLLOWERS_GLOB) if p.is_file()])
    users: Set[str] = set()
    for p in archivos:
        html = leer_texto(p)
        users |= extraer_usernames_html(html)
    return users

def cargar_following() -> Set[str]:
    if not FOLLOWING_FILE.exists():
        return set()
    html = leer_texto(FOLLOWING_FILE)
    return extraer_usernames_html(html)

def cargar_pending() -> Set[str]:
    if not PENDING_FILE.exists():
        return set()
    html = leer_texto(PENDING_FILE)
    return extraer_usernames_html(html)


# =========================
# Opciones
# =========================

def opcion_1_ver_followers() -> None:
    users = sorted(cargar_followers())
    print(f"Seguidores encontrados: {len(users)}")
    escribir_lineas(SCRIPT_DIR / "followers.txt", users)
    links = a_enlaces(users)
    escribir_lineas(SCRIPT_DIR / "followers_links.txt", links)
    abrir_en_batches(links)

def opcion_2_ver_following() -> None:
    users = sorted(cargar_following())
    print(f"Seguidos encontrados: {len(users)}")
    escribir_lineas(SCRIPT_DIR / "following.txt", users)
    links = a_enlaces(users)
    escribir_lineas(SCRIPT_DIR / "following_links.txt", links)
    abrir_en_batches(links)

def opcion_3_comparar_no_te_siguen_de_vuelta() -> None:
    following = cargar_following()
    followers = cargar_followers()
    not_back = sorted(following - followers)
    print(f"No te siguen de vuelta: {len(not_back)}")
    escribir_lineas(SCRIPT_DIR / "not_following_back.txt", not_back)
    links = a_enlaces(not_back)
    escribir_lineas(SCRIPT_DIR / "not_following_back_links.txt", links)
    abrir_en_batches(links)

def opcion_4_pendientes_no_aceptados() -> None:
    pending = sorted(cargar_pending())
    print(f"Solicitudes de seguimiento pendientes (enviadas por ti): {len(pending)}")
    escribir_lineas(SCRIPT_DIR / "pending_follow_requests.txt", pending)
    links = a_enlaces(pending)
    escribir_lineas(SCRIPT_DIR / "pending_follow_requests_links.txt", links)
    abrir_en_batches(links)


# =========================
# Menú mínimo
# =========================

def menu() -> None:
    print("Carpeta de datos:", DATA_DIR)
    while True:
        print("\n=== Menú (elige 1-4, 0 para salir) ===")
        print("1) Ver QUIÉN TE SIGUE (followers)")
        print("2) Ver A QUIÉNES SIGUES (following)")
        print("3) Comparar SEGUIDOS vs SEGUIDORES (no te siguen de vuelta)")
        print("4) Ver a QUIÉNES SEGUISTE y NO ACEPTARON (pending)")
        print("0) Salir")
        op = input("> ").strip()
        if op == "1":
            opcion_1_ver_followers()
        elif op == "2":
            opcion_2_ver_following()
        elif op == "3":
            opcion_3_comparar_no_te_siguen_de_vuelta()
        elif op == "4":
            opcion_4_pendientes_no_aceptados()
        elif op == "0":
            print("Listo.")
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    # Atajos con argumentos (opcional):
    #   python ig_follow_tools.py 1|2|3|4
    if len(sys.argv) > 1 and sys.argv[1] in {"1","2","3","4"}:
        {"1": opcion_1_ver_followers,
         "2": opcion_2_ver_following,
         "3": opcion_3_comparar_no_te_siguen_de_vuelta,
         "4": opcion_4_pendientes_no_aceptados}[sys.argv[1]]()
    else:
        menu()
