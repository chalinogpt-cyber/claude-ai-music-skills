"""CLI principal: genera corridos virales para el Dia del Padre.

Uso basico:
    python main.py

Opciones:
    python main.py --temas temas.csv --salida salida --limite 20
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from corridos.almacenamiento import (
    guardar_corrido,
    guardar_resumen,
    leer_temas,
)
from corridos.cliente import ClienteCorridos, ErrorAPI
from corridos.config import Config, ConfigError
from corridos.generador import GeneradorCorridos

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("corridos")

RAIZ = Path(__file__).resolve().parent


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Genera corridos virales para el Dia del Padre "
        "usando una API compatible con OpenAI.",
    )
    parser.add_argument(
        "--temas",
        type=Path,
        default=RAIZ / "temas.csv",
        help="Ruta al CSV de temas (por defecto: temas.csv).",
    )
    parser.add_argument(
        "--salida",
        type=Path,
        default=RAIZ / "salida",
        help="Directorio de salida (por defecto: ./salida).",
    )
    parser.add_argument(
        "--limite",
        type=int,
        default=20,
        help="Maximo de corridos a generar (por defecto: 20).",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    try:
        config = Config.desde_entorno()
    except ConfigError as exc:
        logger.error("%s", exc)
        return 2

    try:
        temas = leer_temas(args.temas)
    except (FileNotFoundError, ValueError) as exc:
        logger.error("%s", exc)
        return 2

    if args.limite > 0:
        temas = temas[: args.limite]

    logger.info(
        "Modelo: %s | Endpoint: %s | Temas a procesar: %d",
        config.model,
        config.base_url,
        len(temas),
    )

    cliente = ClienteCorridos(config)
    generador = GeneradorCorridos(cliente)

    generados: list[tuple[int, object, Path]] = []
    fallidos: list[tuple[str, str]] = []

    for indice, tema in enumerate(temas, start=1):
        logger.info("[%d/%d] Generando: %s", indice, len(temas), tema.tema)
        try:
            corrido = generador.generar(tema.tema, tema.enfoque)
            ruta = guardar_corrido(corrido, indice, args.salida)
            generados.append((indice, corrido, ruta))
            logger.info("    Guardado en %s", ruta.name)

            # Guardado automatico e incremental del resumen tras cada exito,
            # para no perder progreso si algo falla mas adelante.
            guardar_resumen(generados, args.salida)

        except (ErrorAPI, ValueError) as exc:
            logger.error("    Fallo el tema '%s': %s", tema.tema, exc)
            fallidos.append((tema.tema, str(exc)))
            continue
        except KeyboardInterrupt:
            logger.warning("Interrumpido por el usuario. Guardando progreso...")
            break

    if generados:
        ruta_resumen = guardar_resumen(generados, args.salida)
        logger.info("Resumen actualizado: %s", ruta_resumen)

    logger.info(
        "Listo. Generados: %d | Fallidos: %d | Salida: %s",
        len(generados),
        len(fallidos),
        args.salida,
    )

    if fallidos:
        logger.warning("Temas con errores:")
        for tema, motivo in fallidos:
            logger.warning("  - %s -> %s", tema, motivo)

    # Codigo de salida: 0 si se genero al menos uno; 1 si todo fallo.
    return 0 if generados else 1


if __name__ == "__main__":
    sys.exit(main())
