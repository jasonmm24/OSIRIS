"""Inicialización y conversación con el motor de lenguaje Ollama."""

import ollama
import datetime

fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

historial = [
    {
        'role': 'system', 
        'content': f'Eres O.S.I.R.I.S. (Open Source Intelligent Reactive Information System), un sistema de inteligencia artificial avanzada, eficiente y concisa de código abierto. Tu creador es Jason. Responde siempre en español, ve directo al grano sin saludos. Hoy es {fecha_actual}.'
    }
]

def inicializar_motor():
    """Precalienta el modelo configurado mediante una solicitud breve.

    No recibe parámetros. Informa del inicio y de la carga del modelo en la
    consola; los errores de inicialización se consumen según el comportamiento
    actual del módulo.

    Returns:
        None: El resultado de la solicitud de precalentamiento no se devuelve.
    """
    print("[Viernes] Pre-calentando motor neuronal...")
    try:
        ollama.chat(model='qwen3.5:2b', messages=[{'role': 'user', 'content': 'iniciando'}], keep_alive='2h')
        print("[Viernes] Motor neuronal cargado y listo.")
    except Exception:
        pass 

def pensar_respuesta(texto_usuario: str) -> str:
    """Envía un mensaje al modelo y devuelve la respuesta completa generada.

    Args:
        texto_usuario: Mensaje que se añade al historial de conversación.

    Returns:
        str: Respuesta acumulada del modelo, o una cadena vacía si falla
        la solicitud.
    """
    historial.append({'role': 'user', 'content': texto_usuario})
    
    try:
        stream = ollama.chat(
            model='qwen3.5:2b', 
            messages=historial, 
            stream=True, 
            keep_alive='2h',
            options={'num_ctx': 1024}
        )
        
        respuesta_completa = ""
        for chunk in stream:
            palabra = chunk['message']['content']
            print(palabra, end='', flush=True)
            respuesta_completa += palabra
            
        print()
        
        historial.append({'role': 'assistant', 'content': respuesta_completa})
        return respuesta_completa
        
    except Exception as e:
        print(f"\n[Error neuronal]: {e}")
        historial.pop() 
        return ""