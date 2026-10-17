<div align="center">

# O.S.I.R.I.S.

### Open Source Intelligent Reactive Information System

Asistente virtual nativo para Linux con IA local, interfaz de escritorio y
control de aplicaciones del sistema.

**Linux** · **Python 3.13+** · **Ollama** · **PySide6** · **Textual** · **uv**

</div>

O.S.I.R.I.S. es un proyecto modular y de código abierto que combina una interfaz
holográfica para el escritorio con una experiencia cyberpunk en terminal. Usa
Ollama para procesar conversaciones en el equipo local, sin depender de
servicios de IA en la nube.

## Contenido

- [Características](#características)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Uso](#uso)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Privacidad](#privacidad)

## Características

| Componente | Descripción |
| --- | --- |
| **GUI de escritorio** | Ventana circular animada con estética holográfica inspirada en un reactor Arc e icono en la bandeja del sistema. |
| **TUI de terminal** | Interfaz interactiva desarrollada con Textual, con procesamiento de respuestas fuera del hilo principal. |
| **Motor local** | Conversación mediante Ollama y el modelo `qwen3.5:2b`. |
| **Control del sistema** | Busca lanzadores `.desktop` del sistema, del usuario y de las exportaciones de Flatpak para iniciar aplicaciones. |
| **Búsqueda alternativa** | Si una aplicación solicitada no se encuentra localmente, abre una dirección de búsqueda en el navegador predeterminado. |
| **Diseño modular** | Separa las interfaces, la integración con el modelo y las operaciones del sistema. |

## Requisitos

- Linux con entorno de escritorio para utilizar la GUI. Nobara y Fedora son las
  plataformas recomendadas.
- Python **3.13 o posterior**.
- [`uv`](https://docs.astral.sh/uv/) para administrar el entorno y las
  dependencias.
- [Ollama](https://ollama.com/) instalado y en ejecución.
- Modelo `qwen3.5:2b` disponible en Ollama.

La TUI puede ejecutarse desde una terminal. La búsqueda alternativa del
navegador requiere conexión a Internet.

## Instalación

### Configurar este repositorio

Desde la raíz del proyecto, sincroniza las dependencias y descarga el modelo:

```bash
uv sync
ollama pull qwen3.5:2b
```

`uv sync` crea o actualiza el entorno virtual de acuerdo con
[`pyproject.toml`](pyproject.toml) y [`uv.lock`](uv.lock). Asegúrate de que el
servicio de Ollama esté activo antes de iniciar la aplicación.

### Crear un proyecto equivalente desde cero

Como referencia, estos comandos inicializan un proyecto nuevo. No los ejecutes
dentro de este repositorio, que ya incluye su propio manifiesto y archivo de
bloqueo:

```bash
uv init --package osiris
cd osiris
uv add ollama pyside6 textual
```

## Uso

Inicia cualquiera de las interfaces desde la raíz del repositorio.

### GUI · Escritorio

```bash
uv run python src/osiris/main_gui.py
```

La ventana puede mostrarse u ocultarse desde el icono de la bandeja del sistema.
Al procesar una orden para abrir una aplicación, la GUI se oculta
automáticamente.

### TUI · Terminal

```bash
uv run python src/osiris/main_cli.py
```

Escribe una instrucción en el campo de entrada. Pulsa `q` para salir o `Ctrl+L`
para limpiar la pantalla. También puedes escribir `salir`, `exit` o `quit`.

## Estructura del proyecto

```text
.
├── pyproject.toml             # Metadatos y dependencias del proyecto
├── uv.lock                    # Versiones fijadas de las dependencias
└── src/
    └── osiris/
        ├── __init__.py
        ├── main_gui.py        # Punto de entrada de la GUI
        ├── main_cli.py        # Punto de entrada de la TUI
        ├── core/
        │   ├── llm.py         # Integración con Ollama e historial
        │   ├── system.py      # Búsqueda y ejecución de aplicaciones
        │   └── audio.py       # Captura y transcripción de voz
        └── gui/
            └── arc_reactor.py # Ventana animada de PySide6
```

El módulo de audio está presente en el código, pero sus dependencias específicas
no están declaradas actualmente en `pyproject.toml`.

## Privacidad

La generación de respuestas se realiza localmente mediante Ollama; O.S.I.R.I.S.
no necesita un proveedor de IA en la nube ni una clave de API. La descarga
inicial del modelo requiere Internet. Además, la función de búsqueda alternativa
puede abrir páginas externas en el navegador.
