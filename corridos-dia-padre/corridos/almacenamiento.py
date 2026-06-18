"""Lectura de temas y guardado de corridos en archivos .md y resumen."""

from __future__ import annotations

import csv
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from .generador import Corrido


@dataclass
class Tema:
    """Un tema leido desde el CSV."""

    tema: str
    enfoque: str = ""


def leer_temas(ruta_csv: Path) -> list[Tema]:
    """Lee los temas desde un CSV con columnas 'tema' y opcional 'enfoque'."""
    if not ruta_csv.exists():
        raise FileNotFoundError(f"No se encontro el archivo de temas: {ruta_csv}")

    temas: list[Tema] = []
    with ruta_csv.open(encoding="utf-8-sig", newline="") as fh:
        lector = csv.DictReader(fh)
        if not lector.fieldnames or "tema" not in [
            c.strip().lower() for c in lector.fieldnames
        ]:
            raise ValueError(
                "El CSV debe tener al menos una columna 'tema'. "
                f"Columnas encontradas: {lector.fieldnames}"
            )

        # Normalizamos nombres de columnas a minusculas. Si una fila tiene
        # comas de mas, csv.DictReader agrupa el sobrante en una lista bajo la
        # clave None (restkey); lo reincorporamos al valor de 'enfoque'.
        for fila in lector:
            normalizada: dict[str, str] = {}
            extra: list[str] = []
            for clave, valor in fila.items():
                if isinstance(valor, list):
                    valor = ", ".join(str(x).strip() for x in valor if x)
                valor = (valor or "").strip()
                if clave is None:
                    if valor:
                        extra.append(valor)
                    continue
                normalizada[(clave or "").strip().lower()] = valor

            tema = normalizada.get("tema", "").strip()
            if not tema:
                continue
            enfoque = normalizada.get("enfoque", "").strip()
            if extra:
                enfoque = ", ".join([p for p in [enfoque, *extra] if p])
            temas.append(Tema(tema=tema, enfoque=enfoque))

    if not temas:
        raise ValueError(f"No se encontraron temas validos en {ruta_csv}")

    return temas


def _slug(texto: str, max_len: int = 60) -> str:
    """Convierte un texto en un nombre de archivo seguro."""
    texto = texto.lower().strip()
    reemplazos = {
        "á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u",
        "ä": "a", "ë": "e", "ï": "i", "ö": "o", "ü": "u",
        "ñ": "n", "ç": "c",
    }
    for origen, destino in reemplazos.items():
        texto = texto.replace(origen, destino)
    texto = re.sub(r"[^a-z0-9]+", "-", texto)
    texto = texto.strip("-")
    return texto[:max_len].strip("-") or "corrido"


def guardar_corrido(corrido: Corrido, indice: int, directorio: Path) -> Path:
    """Guarda un corrido individual como archivo Markdown y devuelve la ruta."""
    directorio.mkdir(parents=True, exist_ok=True)
    nombre = f"{indice:02d}-{_slug(corrido.titulo or corrido.tema)}.md"
    ruta = directorio / nombre

    advertencias_md = ""
    if corrido.advertencias:
        items = "\n".join(f"> - {a}" for a in corrido.advertencias)
        advertencias_md = (
            "\n> **Avisos de validacion de estructura:**\n" + items + "\n"
        )

    contenido = f"""# {corrido.titulo}

**Tema:** {corrido.tema}
**Enfoque:** {corrido.enfoque}
**Gancho:** {corrido.gancho}
**Frase para miniatura:** {corrido.frase_miniatura}
{advertencias_md}
---

## Letra

{corrido.letra}

---

## Prompt para Suno

{corrido.prompt_suno}

## Prompt para imagen (16:9)

{corrido.prompt_imagen}
"""
    ruta.write_text(contenido, encoding="utf-8")
    return ruta


def guardar_resumen(
    corridos: list[tuple[int, Corrido, Path]],
    directorio: Path,
) -> Path:
    """Crea el archivo resumen con titulo, gancho, tema, frase y prompts."""
    directorio.mkdir(parents=True, exist_ok=True)
    ruta = directorio / "RESUMEN.md"

    fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
    lineas = [
        "# Resumen de corridos para el Dia del Padre",
        "",
        f"Generados: {len(corridos)}  |  Fecha: {fecha}",
        "",
    ]

    for indice, corrido, ruta_archivo in corridos:
        lineas.extend(
            [
                f"## {indice:02d}. {corrido.titulo}",
                "",
                f"- **Tema:** {corrido.tema}",
                f"- **Gancho:** {corrido.gancho}",
                f"- **Frase para miniatura:** {corrido.frase_miniatura}",
                f"- **Archivo:** `{ruta_archivo.name}`",
                "",
                "**Prompt para Suno:**",
                "",
                f"> {corrido.prompt_suno}",
                "",
                "**Prompt para imagen (16:9):**",
                "",
                f"> {corrido.prompt_imagen}",
                "",
                "---",
                "",
            ]
        )

    ruta.write_text("\n".join(lineas), encoding="utf-8")
    return ruta
