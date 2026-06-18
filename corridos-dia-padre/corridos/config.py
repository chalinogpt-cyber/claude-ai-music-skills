"""Carga y validacion de la configuracion desde variables de entorno.

La API key NUNCA se escribe en el codigo. Todo se lee de variables de
entorno (opcionalmente cargadas desde un archivo .env).
"""

from __future__ import annotations

import os
from dataclasses import dataclass

try:
    # python-dotenv es opcional en tiempo de ejecucion: si esta instalado
    # cargamos automaticamente un archivo .env presente en el directorio.
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:  # pragma: no cover - dotenv es una dependencia recomendada
    pass


class ConfigError(RuntimeError):
    """Se lanza cuando falta configuracion obligatoria."""


@dataclass(frozen=True)
class Config:
    """Configuracion de la API compatible con OpenAI."""

    base_url: str
    api_key: str
    model: str

    # Parametros de generacion / robustez
    temperature: float = 0.85
    max_tokens: int = 2048
    max_reintentos: int = 5
    espera_base: float = 2.0  # segundos, para backoff exponencial
    timeout: float = 90.0

    @classmethod
    def desde_entorno(cls) -> "Config":
        """Construye la configuracion leyendo variables de entorno.

        Variables obligatorias:
          - FREEMODEL_BASE_URL
          - FREEMODEL_API_KEY
          - FREEMODEL_MODEL
        """
        base_url = os.getenv("FREEMODEL_BASE_URL", "").strip()
        api_key = os.getenv("FREEMODEL_API_KEY", "").strip()
        model = os.getenv("FREEMODEL_MODEL", "").strip()

        faltantes = []
        if not base_url:
            faltantes.append("FREEMODEL_BASE_URL")
        if not api_key:
            faltantes.append("FREEMODEL_API_KEY")
        if not model:
            faltantes.append("FREEMODEL_MODEL")

        if faltantes:
            raise ConfigError(
                "Faltan variables de entorno obligatorias: "
                + ", ".join(faltantes)
                + ".\nDefinelas en tu entorno o en un archivo .env "
                "(ver .env.example)."
            )

        return cls(base_url=base_url, api_key=api_key, model=model)
