"""Punto de entrada de la interfaz gráfica y el icono de bandeja del sistema."""

import sys
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PySide6.QtWidgets import QSystemTrayIcon

from core.llm import inicializar_motor
from gui.arc_reactor import InterfazCircular, crear_icono_tray

def main():
    """Crea la aplicación Qt, la ventana circular y el menú de bandeja.

    No recibe parámetros. Inicia el ciclo de eventos de Qt y finaliza el
    proceso cuando se solicita salir desde la interfaz.

    Returns:
        None: El ciclo de eventos termina mediante ``sys.exit``.
    """
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    
    print("Iniciando motor de O.S.I.R.I.S. ...")
    inicializar_motor()

    ventana = InterfazCircular()
    
    tray = QSystemTrayIcon()
    tray.setIcon(crear_icono_tray())
    tray.setVisible(True)

    menu = QMenu()
    accion_mostrar = menu.addAction("Mostrar O.S.I.R.I.S.")
    accion_ocultar = menu.addAction("Ocultar")
    menu.addSeparator()
    accion_salir = menu.addAction("Apagar Sistema")

    accion_mostrar.triggered.connect(ventana.show)
    accion_ocultar.triggered.connect(ventana.hide)
    accion_salir.triggered.connect(app.quit)

    tray.setContextMenu(menu)

    def alternar_ventana(reason):
        """Muestra u oculta la ventana al pulsar el icono de bandeja.

        Args:
            reason: Motivo de activación emitido por ``QSystemTrayIcon``.

        Returns:
            None: La función solo modifica la visibilidad y el foco.
        """
        if reason == QSystemTrayIcon.Trigger:
            if ventana.isVisible():
                ventana.hide()
            else:
                ventana.show()
                ventana.activateWindow()

    tray.activated.connect(alternar_ventana)
    
    ventana.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()