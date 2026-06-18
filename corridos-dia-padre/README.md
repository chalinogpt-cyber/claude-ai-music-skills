# corridos-dia-padre

Automatiza la creacion de **20 corridos virales para el Dia del Padre** usando
una API **compatible con OpenAI**. Para cada tema el sistema genera un titulo
con alto CTR, un gancho emocional para miniatura, una letra de corrido norteno
clasico estilo anos 90 (original, sin copiar artistas reales) y prompts listos
para Suno e imagen 16:9.

## Caracteristicas

- Lee los temas desde `temas.csv`.
- Genera por cada tema:
  - Titulo con alto CTR.
  - Gancho emocional para la miniatura.
  - Frase corta para sobreponer en la miniatura.
  - Letra de corrido norteno clasico estilo anos 90, **100% original**.
  - Prompt para **Suno**.
  - Prompt para **imagen 16:9**.
- Estructura del corrido:
  - **6 sextillas** (estrofas).
  - **6 versos** por sextilla.
  - Versos octosilabos cantables (objetivo).
  - Rima por sextilla **ABCBDB**.
- Guarda cada corrido en su propio archivo `.md`.
- Crea un archivo `RESUMEN.md` con titulo, gancho, tema, frase de miniatura,
  prompt para Suno y prompt para imagen 16:9.
- **Manejo de errores, reintentos con backoff y guardado automatico** (el
  resumen se actualiza tras cada corrido para no perder progreso).
- La **API key nunca se escribe en el codigo**: se lee de variables de entorno.

## Requisitos

- Python 3.10 o superior.
- Una API compatible con OpenAI (endpoint `/chat/completions`).

## Instalacion

```bash
# 1. (Opcional pero recomendado) crear un entorno virtual
python -m venv .venv
source .venv/bin/activate        # En Windows: .venv\Scripts\activate

# 2. Instalar dependencias
pip install -r requirements.txt
```

## Configuracion

La configuracion se toma de **variables de entorno**. Copia el ejemplo y
rellena tus valores:

```bash
cp .env.example .env
```

Edita `.env` (no se sube al repositorio):

| Variable              | Descripcion                                              | Ejemplo                     |
|-----------------------|----------------------------------------------------------|-----------------------------|
| `FREEMODEL_BASE_URL`  | URL base del endpoint compatible con OpenAI (con `/v1`). | `https://api.openai.com/v1` |
| `FREEMODEL_API_KEY`   | Tu clave de API (secreta).                               | `sk-...`                    |
| `FREEMODEL_MODEL`     | Identificador del modelo a usar.                         | `gpt-4o-mini`               |

Tambien puedes exportarlas directamente en tu shell:

```bash
export FREEMODEL_BASE_URL="https://api.openai.com/v1"
export FREEMODEL_API_KEY="tu-api-key"
export FREEMODEL_MODEL="gpt-4o-mini"
```

> El archivo `.env` esta incluido en `.gitignore`. **Nunca** subas tu API key.

## Uso

```bash
# Genera hasta 20 corridos a partir de temas.csv en ./salida
python main.py
```

Opciones:

```bash
python main.py --temas temas.csv --salida salida --limite 20
```

| Opcion      | Por defecto | Descripcion                                  |
|-------------|-------------|----------------------------------------------|
| `--temas`   | `temas.csv` | Ruta al CSV con los temas.                   |
| `--salida`  | `salida`    | Carpeta donde se guardan los `.md`.          |
| `--limite`  | `20`        | Numero maximo de corridos a generar.         |

## Formato de `temas.csv`

Archivo CSV con cabecera. La columna `tema` es obligatoria; `enfoque` es
opcional y ayuda a guiar el contenido:

```csv
tema,enfoque
El padre que trabajaba en el campo,Homenaje al padre campesino
El papa que cruzo la frontera por la familia,Sacrificio del migrante
```

## Salida

En la carpeta de salida (`salida/` por defecto) se crean:

```
salida/
├── 01-<titulo>.md      # un archivo por corrido
├── 02-<titulo>.md
├── ...
└── RESUMEN.md          # resumen con prompts de Suno e imagen
```

Cada archivo de corrido contiene el titulo, tema, enfoque, gancho, frase de
miniatura, la letra completa y los prompts de Suno e imagen 16:9.

## Estructura del proyecto

```
corridos-dia-padre/
├── main.py                  # CLI principal
├── temas.csv                # 20 temas de ejemplo
├── requirements.txt
├── .env.example             # plantilla de variables de entorno
├── .gitignore
├── README.md
└── corridos/
    ├── __init__.py
    ├── config.py            # carga/validacion de variables de entorno
    ├── cliente.py           # cliente OpenAI-compatible con reintentos
    ├── generador.py         # prompts, parseo y validacion del corrido
    └── almacenamiento.py    # lectura de CSV y guardado de .md / resumen
```

## Robustez

- **Reintentos**: cada llamada a la API se reintenta hasta 5 veces con backoff
  exponencial ante errores transitorios (limites de tasa, timeouts, 5xx).
- **Tolerancia a errores por tema**: si un tema falla, se registra y el proceso
  continua con los demas.
- **Validacion de estructura**: se verifica el numero de sextillas y versos; las
  desviaciones se anotan como avisos en el archivo del corrido.
- **Guardado automatico**: el `RESUMEN.md` se actualiza tras cada corrido.

## Notas

- Las letras se generan de forma **original**. El sistema instruye al modelo para
  no copiar, imitar ni mencionar artistas reales ni letras existentes.
- La metrica octosilaba y la rima ABCBDB son objetivos guiados por el prompt; la
  validacion automatica confirma la cantidad de estrofas y versos.
