"""Descubrimiento y ejecución de aplicaciones de escritorio en Linux."""

import os
import glob
import subprocess
import webbrowser

# Sus valores son nombres de ejecutables que el sistema resuelve al iniciarlos.
ALIAS_PRIORIDAD = {
    "lutris": "lutris",
    "prism launcher": "prismlauncher",
    "minecraft": "prismlauncher",
    "archivos": "nautilus",
    "terminal": "gnome-terminal",
    "navegador": "firefox",
    "código": "code",
    "calculadora": "gnome-calculator"
}

def escanear_aplicaciones():
    """Busca aplicaciones en archivos ``.desktop`` de rutas habituales.

    No recibe parámetros. Lee el nombre y el comando de ejecución de cada
    archivo encontrado y omite las entradas sin ambos valores o cuyo comando
    contiene la opción de instalación ``--install``.

    Returns:
        dict[str, str]: Mapa de nombres de aplicación en minúsculas a comandos
        de ejecución.
    """
    # Se examinan aplicaciones del sistema, del usuario y exportadas por Flatpak.
    rutas_desktop = [
        "/usr/share/applications/**/*.desktop",
        os.path.expanduser("~/.local/share/applications/**/*.desktop"),
        "/var/lib/flatpak/exports/share/applications/**/*.desktop"
    ]
    
    aplicaciones = {}
    for ruta in rutas_desktop:
        # El patrón recursivo permite localizar lanzadores en subdirectorios.
        for archivo in glob.glob(ruta, recursive=True):
            try:
                with open(archivo, 'r', encoding='utf-8') as f:
                    nombre = None
                    comando_exec = None
                    
                    for linea in f:
                        # Las acciones secundarias del lanzador tienen campos
                        # propios; se detiene aquí el análisis de la entrada base.
                        if linea.startswith("[Desktop Action"):
                            break
                            
                        if linea.startswith("Name=") and not nombre:
                            nombre = linea.split("=")[1].strip().lower()
                        elif linea.startswith("Exec=") and not comando_exec:
                            # Se descarta el primer grupo de argumentos opcionales
                            # de escritorio y se eliminan comillas del ejecutable.
                            exec_raw = linea.split("=")[1].strip()
                            comando_exec = exec_raw.split(" %")[0].replace('"', '')
                            
                    if nombre and comando_exec:
                        if "--install" not in comando_exec:
                            aplicaciones[nombre] = comando_exec
            except Exception:
                pass
    return aplicaciones

def ejecutar_comando_sistema(texto: str) -> str | None:
    """Interpreta una orden de apertura e inicia una aplicación o una web.

    Args:
        texto: Orden en lenguaje natural que puede solicitar abrir una app.

    Returns:
        str | None: Mensaje que describe la acción iniciada, o ``None`` si el
        texto no coincide con una orden de apertura.
    """
    texto_lower = texto.lower()
    
    if "abre " in texto_lower or "inicia " in texto_lower:
        objetivo = texto_lower.replace("abre ", "").replace("inicia ", "").strip()
        
        # Los alias explícitos se prueban primero para evitar depender del
        # formato o de la presencia de un lanzador .desktop.
        for alias, comando_exacto in ALIAS_PRIORIDAD.items():
            if objetivo in alias or alias in objetivo:
                subprocess.Popen(comando_exacto.split(), start_new_session=True)
                return f"Iniciando {alias.title()} (Prioridad)..."
        
        # Se ejecuta el comando extraído de la entrada .desktop cuyo nombre
        # contiene el objetivo solicitado.
        apps_instaladas = escanear_aplicaciones()
        for nombre_app, comando_exec in apps_instaladas.items():
            if objetivo in nombre_app:
                subprocess.Popen(comando_exec.split(), start_new_session=True)
                return f"Iniciando {nombre_app.title()}..."
        
        # Si no hay coincidencia local, se construye y abre una URL de búsqueda.
        url = f"https://www.{objetivo.replace(' ', '')}.com"
        webbrowser.open(url)
        return f"Buscando '{objetivo.title()}' en la red..."
        
    return None