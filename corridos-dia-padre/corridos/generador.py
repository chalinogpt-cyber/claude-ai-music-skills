"""Logica de generacion de corridos: prompts, parseo y validacion."""

from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass, field

from .cliente import ClienteCorridos

logger = logging.getLogger(__name__)

# Reglas estructurales del corrido solicitado.
NUM_SEXTILLAS = 6
VERSOS_POR_SEXTILLA = 6


SYSTEM_PROMPT = (
    "Eres un compositor experto en corrido norteno clasico al estilo de los "
    "anos 90, inspirado en el corrido mexicano tradicional. Escribes letras "
    "originales, emotivas y cantables. NUNCA copias, imitas el nombre, ni "
    "mencionas a artistas reales, ni reproduces letras existentes. Respondes "
    "SIEMPRE en espanol y SOLO con un objeto JSON valido, sin texto adicional "
    "ni bloques de codigo."
)


def _construir_user_prompt(tema: str, enfoque: str) -> str:
    """Crea el prompt de usuario para un tema concreto."""
    return f"""
Crea un corrido viral para el DIA DEL PADRE.

TEMA: {tema}
ENFOQUE: {enfoque}

Devuelve EXCLUSIVAMENTE un objeto JSON con EXACTAMENTE estas claves:

{{
  "titulo": "Titulo con alto CTR, emotivo y llamativo (max 70 caracteres)",
  "gancho": "Gancho emocional corto para la miniatura (max 90 caracteres)",
  "frase_miniatura": "Frase impactante de 3 a 6 palabras para sobreponer en la miniatura",
  "letra": "La letra completa del corrido como texto",
  "prompt_suno": "Prompt en ingles o espanol para generar el audio en Suno (estilo, instrumentos, tempo, voz)",
  "prompt_imagen": "Prompt detallado para generar una imagen 16:9 de portada/miniatura"
}}

REGLAS OBLIGATORIAS DE LA LETRA ("letra"):
- Estilo: corrido norteno clasico de los anos 90 (acordeon, bajo sexto, tololoche).
- Debe tener EXACTAMENTE {NUM_SEXTILLAS} sextillas (estrofas).
- Cada sextilla debe tener EXACTAMENTE {VERSOS_POR_SEXTILLA} versos (lineas).
- Intenta que cada verso sea octosilabo (8 silabas) y cantable.
- Esquema de rima por sextilla: ABCBDB
  (riman entre si el verso 2, 4 y 6 de cada sextilla).
- Separa cada sextilla con UNA linea en blanco.
- No numeres los versos ni las estrofas.
- Contenido 100% original: prohibido mencionar o imitar artistas reales.
- Tono emotivo, narrativo y respetuoso, celebrando la figura paterna.

REGLAS DE FORMATO:
- "letra" debe contener las {NUM_SEXTILLAS} sextillas, con los versos separados
  por saltos de linea (\\n) y una linea en blanco entre sextillas.
- Responde solo con el JSON. Nada de explicaciones ni ```.
""".strip()


@dataclass
class Corrido:
    """Resultado estructurado de un corrido generado."""

    tema: str
    enfoque: str
    titulo: str
    gancho: str
    frase_miniatura: str
    letra: str
    prompt_suno: str
    prompt_imagen: str
    advertencias: list[str] = field(default_factory=list)

    @property
    def sextillas(self) -> list[list[str]]:
        """Divide la letra en sextillas (cada una es una lista de versos)."""
        bloques = re.split(r"\n\s*\n", self.letra.strip())
        resultado = []
        for bloque in bloques:
            versos = [v.strip() for v in bloque.splitlines() if v.strip()]
            if versos:
                resultado.append(versos)
        return resultado


def _extraer_json(texto: str) -> dict:
    """Extrae un objeto JSON de la respuesta del modelo de forma tolerante."""
    limpio = texto.strip()

    # Quitar fences de codigo tipo ```json ... ```
    if limpio.startswith("```"):
        limpio = re.sub(r"^```[a-zA-Z]*\n", "", limpio)
        limpio = re.sub(r"\n```$", "", limpio).strip()

    try:
        return json.loads(limpio)
    except json.JSONDecodeError:
        pass

    # Fallback: tomar desde la primera { hasta la ultima }
    inicio = limpio.find("{")
    fin = limpio.rfind("}")
    if inicio != -1 and fin != -1 and fin > inicio:
        fragmento = limpio[inicio : fin + 1]
        return json.loads(fragmento)

    raise ValueError("No se encontro un objeto JSON valido en la respuesta.")


def _validar_estructura(letra: str) -> list[str]:
    """Verifica el numero de sextillas y versos. Devuelve advertencias."""
    advertencias: list[str] = []
    bloques = [
        [v for v in b.splitlines() if v.strip()]
        for b in re.split(r"\n\s*\n", letra.strip())
        if b.strip()
    ]

    if len(bloques) != NUM_SEXTILLAS:
        advertencias.append(
            f"Se esperaban {NUM_SEXTILLAS} sextillas, se obtuvieron {len(bloques)}."
        )

    for i, versos in enumerate(bloques, start=1):
        if len(versos) != VERSOS_POR_SEXTILLA:
            advertencias.append(
                f"La sextilla {i} tiene {len(versos)} versos "
                f"(se esperaban {VERSOS_POR_SEXTILLA})."
            )

    return advertencias


class GeneradorCorridos:
    """Orquesta la generacion de un corrido a partir de un tema."""

    CLAVES = (
        "titulo",
        "gancho",
        "frase_miniatura",
        "letra",
        "prompt_suno",
        "prompt_imagen",
    )

    def __init__(self, cliente: ClienteCorridos) -> None:
        self.cliente = cliente

    def generar(self, tema: str, enfoque: str = "") -> Corrido:
        """Genera un corrido completo y validado para el tema dado."""
        user_prompt = _construir_user_prompt(tema, enfoque)
        respuesta = self.cliente.completar(SYSTEM_PROMPT, user_prompt)

        datos = _extraer_json(respuesta)

        faltantes = [c for c in self.CLAVES if c not in datos or not str(datos[c]).strip()]
        if faltantes:
            raise ValueError(
                "La respuesta del modelo no incluye las claves requeridas: "
                + ", ".join(faltantes)
            )

        letra = str(datos["letra"]).strip()
        advertencias = _validar_estructura(letra)
        if advertencias:
            logger.warning(
                "Tema '%s': la estructura no es exacta -> %s",
                tema,
                "; ".join(advertencias),
            )

        return Corrido(
            tema=tema,
            enfoque=enfoque,
            titulo=str(datos["titulo"]).strip(),
            gancho=str(datos["gancho"]).strip(),
            frase_miniatura=str(datos["frase_miniatura"]).strip(),
            letra=letra,
            prompt_suno=str(datos["prompt_suno"]).strip(),
            prompt_imagen=str(datos["prompt_imagen"]).strip(),
            advertencias=advertencias,
        )
