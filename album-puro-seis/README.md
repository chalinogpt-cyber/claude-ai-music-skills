# Puro Seis

Álbum de 14 tracks en corrido tumbado / rap mexicano, escrito para generarse en Suno.
Un solo personaje, una sola voz: el morro al que le dijeron que no iba a llegar, contando
lo que aprendió llegando.

## Concepto

Todo el disco lo canta la misma persona, en el mismo tono: sarcasmo frío, cero víctima,
cero fanfarronería vacía. No hay lujo presumido — hay cuentas pagadas. No hay venganza —
hay memoria. Cada track es un dicho de barrio llevado a canción.

**Arco del álbum**: de dónde vine (01–03) → quién me estorbó (04–06) → cómo trabajo
(07–08) → cómo me cuido (09–11) → lo que perdí (12) → a quién le debo (13) → gracias
por todo (14).

## Tracklist

| # | Título | Tema | BPM |
|---|--------|------|-----|
| 01 | [Me Graduaron de Burro (Puro 6)](songs/01-me-graduaron-de-burro.md) | La escuela vs. la banqueta | 101 |
| 02 | [Los Profetas del Fracaso (Bien Callados)](songs/02-los-profetas-del-fracaso.md) | Los que predijeron mi fracaso | 102 |
| 03 | [Perro Que Ladra No Muerde](songs/03-perro-que-ladra-no-muerde.md) | Amigos falsos, hocicones | 102 |
| 04 | [Se Te Enfría el Caldo (La Envidia No Paga Renta)](songs/04-se-te-enfria-el-caldo.md) | La envidia como tiempo perdido | 100 |
| 05 | [La Renta No Se Paga con Aplausos](songs/05-la-renta-no-se-paga-con-aplausos.md) | Aparentar vs. tener | 103 |
| 06 | [Pierdes el Dinero y el Amigo](songs/06-pierdes-el-dinero-y-el-amigo.md) | Prestar y quedarte sin las dos cosas | 99 |
| 07 | [El Que Regatea Nunca Cargó la Caja](songs/07-el-que-regatea-nunca-cargo-la-caja.md) | El oficio y su precio | 104 |
| 08 | [La Suerte Llega Cansada](songs/08-la-suerte-llega-cansada.md) | "Tuviste suerte" | 100 |
| 09 | [Boca Cerrada (No Cuento lo Que Traigo)](songs/09-boca-cerrada.md) | Discreción como defensa | 98 |
| 10 | [Aprendí a Decir No (y Se Ofendieron)](songs/10-aprendi-a-decir-no.md) | Poner límites | 101 |
| 11 | [Llegaste con el Carro (No Conmigo)](songs/11-llegaste-con-el-carro.md) | El cariño de temporada | 97 |
| 12 | [El Camino Corto](songs/12-el-camino-corto.md) | El compa que no volvió | 96 |
| 13 | [Mi Jefa No Sabe de Marcas](songs/13-mi-jefa-no-sabe-de-marcas.md) | La madre | 95 |
| 14 | [Gracias por el No](songs/14-gracias-por-el-no.md) | Cierre: gratitud, no revancha | 102 |

## Reglas de escritura del álbum

Para que cualquier track nuevo suene del mismo disco:

- **Métrica**: cuartetas de ~14–16 sílabas, cantadas atrás del beat.
- **Rima**: asonante, pares AABB (o las cuatro líneas con la misma asonancia en los coros).
- **Voz**: primera persona, presente y pretérito. Nunca lastimero, nunca fanfarrón.
- **Cierre**: outro cantado con un dicho de un familiar (jefa, apá, abuelo) + spoken outro
  frío de dos o tres líneas.
- **Vocabulario**: mexicano de calle — feria, lana, chido, morro, jefa, troca, endrogado,
  hocicón, banqueta, quincena. Groserías solo donde el personaje de verdad las diría.
- **Prohibido**: metáforas de poeta, inglés, moralina explicada, presumir cifras.

## Estructura de cada archivo

Cada `.md` trae lo que Suno pide, en orden:

1. `## Style of Music` — el prompt de estilo (bloque `text`)
2. `## Exclude Styles` — lo que no queremos
3. `## Lyrics` — letra con etiquetas de sección y de interpretación
4. `## Configuración sugerida` — Style Influence, Weirdness, duración

## Cómo generarlo en Suno

1. Modo **Custom**.
2. Pegar el bloque de `Style of Music` en el campo de estilo.
3. Pegar `Exclude Styles` en exclusiones.
4. Pegar el bloque de `Lyrics` completo, con los corchetes.
5. Ajustar Style Influence y Weirdness según cada archivo.
6. Generar 3–4 versiones por track; las voces con quiebre natural suelen salir en la 2ª o 3ª.

**Nota de pronunciación**: las letras están escritas para leerse en español mexicano.
Si Suno canta mal alguna palabra, corregir con escritura fonética **solo en Suno**,
no en el archivo.
