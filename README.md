# Visión por Computador — Práctica 1

Herramienta de etiquetado de vídeo hecha con OpenCV. Permite recorrer un vídeo
frame a frame, marcar regiones rectangulares con el ratón y guardar un nuevo
vídeo con esas regiones dibujadas.

## Estado de la práctica

| Script | Apartado | Estado |
| --- | --- | --- |
| `1-base.py` | Funcionalidad básica: guardar el vídeo con las regiones dibujadas | Implementado |
| `2-region-extraction.py` | Extracción de regiones: un vídeo recortado por región | Implementado |
| `3-hiding-regions.py` | Ocultación de regiones con un color sólido | Implementado |
| `4-reduction-of-manual-labeling.py` | Reducción del etiquetado manual | Implementado |
| `5-extra-features.py` | Funcionalidades extra | Implementado |

`practica1.py` es el ejemplo de partida de la asignatura. Espera un vídeo
`MyInputVid.avi` que no está en el repositorio.

## Requisitos

- Python 3 (probado con Python 3.14)
- Dependencias de `requirements.txt`: `numpy` y `opencv-python`

## Instalación

1. Crear el entorno virtual:

   ```
   python -m venv .venv
   ```

2. Activarlo.

   Windows (PowerShell):

   ```
   .venv\Scripts\Activate.ps1
   ```

   Linux / macOS:

   ```
   source .venv/bin/activate
   ```

3. Instalar las dependencias:

   ```
   pip install -r requirements.txt
   ```

## Cómo se ejecuta

Los scripts abren `dog.mp4` con una ruta relativa, así que hay que lanzarlos
desde la raíz del repositorio, con el entorno virtual activado:

```
python 1-base.py
```

```
python 4-reduction-of-manual-labeling.py
```

Se abre una ventana con el vídeo **en pausa** en el primer frame. Al pulsar
`Q` se cierra la ventana y se guarda el resultado.

### Controles

| Tecla | Acción |
| --- | --- |
| `Espacio` | Pausar / reproducir |
| `←` / `→` | Frame anterior / siguiente (pausa el vídeo) |
| Click izquierdo | Marcar una esquina de la región |
| `Z` | Deshacer la última región del frame actual |
| `Q` | Guardar y salir |

### Etiquetar una región

1. Pausa el vídeo en el frame que quieras etiquetar.
2. Haz click en una esquina de la región y después en la esquina opuesta.
   Con el segundo click se crea el rectángulo.
3. Repite para añadir más regiones al mismo frame.

Los clicks sueltos se descartan al cambiar de frame, por lo que los dos clicks
de una región tienen que hacerse sobre el mismo frame.

### Extracción de regiones (`2-region-extraction.py`)

Genera un vídeo independiente por cada región seleccionada. Cada vídeo contiene únicamente
el recorte del vídeo original correspondiente al rectángulo marcado por el
usuario, con fondo negro en los frames donde esa región no fue etiquetada.

Los vídeos de región se guardan como `outputs/2-region-1.mp4`,
`outputs/2-region-2.mp4`, etc., uno por cada región marcada.

<img width="1300" height="752" alt="2-region-extraction" src="https://github.com/user-attachments/assets/cf3bec6c-1e66-426b-9eef-644f2925dfdf" />

### Ocultar regiones (`3-hiding-regions`)

Genera un vídeo en el que las regiones marcadas se ocultan mediante un color sólido negro por defecto.


![Demo de 3-hiding-regions](./documentation/3-hiding-regions.gif)

### Reducción del etiquetado manual (`4-reduction-of-manual-labeling.py`)

En `1-base.py` cada región solo se dibuja en el frame en el que se marcó. Aquí,
en cambio, basta con etiquetar el frame en el que aparece o cambia una región:
las regiones se reutilizan en los frames siguientes hasta el próximo frame
etiquetado, así que solo hay que volver a etiquetar cuando la región deja de
encajar. En la ventana, las regiones propias del frame se ven en verde y las
heredadas en amarillo.

![Demo de 4-reduction-of-manual-labeling.py](./documentation/4-reduction-of-manual-labeling.gif)

### Funcionalidades extra (`5-extra-features.py`)

Además de permitir regiones de forma libre (no solo rectángulos), por cada
región etiquetada se guarda un vídeo independiente solo con su contenido
(recortado a su bounding box, con el resto en negro). Un vídeo nuevo se genera
cada vez que aparece un frame con regiones nuevas, hasta el siguiente frame
etiquetado.

![Demo de 5-extra-features.py](./documentation/5%20-%20extra%20features%20documented.gif)

## Salida

Los vídeos se guardan en la carpeta `outputs/`, que se crea sola y está
excluida de git:

| Script | Fichero generado |
| --- | --- |
| `1-base.py` | `outputs/1-base.mp4` |
| `3-hiding-regions.py` | `outputs/3-hiding-regions.mp4` |
| `4-reduction-of-manual-labeling.py` | `outputs/4-reduction-of-manual-labeling.mp4` |
| `5-extra-features.py` | `outputs/5-extra-features.mp4` y, por cada región etiquetada, un vídeo en `outputs/regions-5-extra-features/` |

Cada ejecución sobrescribe el fichero anterior.

## Desarrollo

Si añades o actualizas una dependencia, regenera `requirements.txt`:

```
pip freeze > requirements.txt
```
