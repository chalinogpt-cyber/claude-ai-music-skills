"""Cliente para la API compatible con OpenAI, con reintentos y backoff."""

from __future__ import annotations

import logging
import time

from openai import OpenAI

from .config import Config

logger = logging.getLogger(__name__)


class ErrorAPI(RuntimeError):
    """Error al comunicarse con la API tras agotar los reintentos."""


class ClienteCorridos:
    """Envoltorio del SDK de OpenAI apuntando a un endpoint configurable.

    Implementa reintentos con backoff exponencial para errores transitorios
    (limites de tasa, timeouts, errores 5xx, problemas de red).
    """

    def __init__(self, config: Config) -> None:
        self.config = config
        self._client = OpenAI(
            base_url=config.base_url,
            api_key=config.api_key,
            timeout=config.timeout,
        )

    def completar(self, system_prompt: str, user_prompt: str) -> str:
        """Envia un chat completion y devuelve el texto de la respuesta.

        Reintenta automaticamente ante fallos transitorios.
        """
        ultimo_error: Exception | None = None

        for intento in range(1, self.config.max_reintentos + 1):
            try:
                respuesta = self._client.chat.completions.create(
                    model=self.config.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    temperature=self.config.temperature,
                    max_tokens=self.config.max_tokens,
                )
                contenido = respuesta.choices[0].message.content
                if not contenido or not contenido.strip():
                    raise ErrorAPI("La API devolvio una respuesta vacia.")
                return contenido.strip()

            except Exception as exc:  # noqa: BLE001 - reintentamos cualquier fallo de red/API
                ultimo_error = exc
                if intento >= self.config.max_reintentos:
                    break
                espera = self.config.espera_base * (2 ** (intento - 1))
                logger.warning(
                    "Intento %d/%d fallo (%s). Reintentando en %.1fs...",
                    intento,
                    self.config.max_reintentos,
                    exc.__class__.__name__,
                    espera,
                )
                time.sleep(espera)

        raise ErrorAPI(
            f"Fallo la llamada a la API tras {self.config.max_reintentos} "
            f"intentos: {ultimo_error}"
        ) from ultimo_error
