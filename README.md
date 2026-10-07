# Visión por Computador — Práctica 1

Herramienta de etiquetado de vídeo hecha con OpenCV. Permite recorrer un vídeo
frame a frame, marcar regiones rectangulares con el ratón y guardar un nuevo
vídeo con esas regiones dibujadas.

## Estado de la práctica

| Script | Apartado | Estado |
| --- | --- | --- |
| `1-base.py` | Funcionalidad básica: guardar el vídeo con las regiones dibujadas | Implementado |
| `2-region-extraction.py` | Extracción de regiones: un vídeo recortado por región | Pendiente |
| `3-hiding-regions.py` | Ocultación de regiones con un color sólido | Pendiente |
| `4-reduction-of-manual-labeling.py` | Reducción del etiquetado manual | Implementado |
| `5-extra-features.py` | Funcionalidades extra | Pendiente |

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

### Diferencia entre los dos scripts

- **`1-base.py`**: cada región solo se dibuja en el frame en el que se marcó.
- **`4-reduction-of-manual-labeling.py`**: las regiones de un frame etiquetado
  se reutilizan en los frames siguientes hasta el próximo frame etiquetado, así
  que solo hay que volver a etiquetar cuando la región deja de encajar. En la
  ventana, las regiones propias del frame se ven en verde y las heredadas en
  amarillo.

## Salida

Los vídeos se guardan en la carpeta `outputs/`, que se crea sola y está
excluida de git:

| Script | Fichero generado |
| --- | --- |
| `1-base.py` | `outputs/1-base.mp4` |
| `4-reduction-of-manual-labeling.py` | `outputs/4-reduction-of-manual-labeling.mp4` |

Cada ejecución sobrescribe el fichero anterior.

## Desarrollo

Si añades o actualizas una dependencia, regenera `requirements.txt`:

```
pip freeze > requirements.txt
```
