"""Ventana circular animada de O.S.I.R.I.S. y sus trabajadores de fondo."""

import math
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QLabel, QFrame, QPushButton
from PySide6.QtCore import Qt, QThread, Signal, QTimer
from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor, QPen

from core.llm import pensar_respuesta
from core.system import ejecutar_comando_sistema

class WorkerOsiris(QThread):
    """Ejecuta la generación de una respuesta fuera del hilo de la interfaz.

    La respuesta y la finalización se notifican mediante señales Qt para que
    los receptores puedan actualizar la interfaz desde el hilo principal.
    """

    senal_respuesta = Signal(str)
    senal_fin = Signal()

    def __init__(self, texto):
        """Prepara el trabajador con el texto que procesará.

        Args:
            texto: Mensaje del usuario que se enviará al motor de lenguaje.

        Returns:
            None: Inicializa el hilo sin iniciarlo.
        """
        super().__init__()
        self.texto = texto

    def run(self):
        """Genera una respuesta y emite las señales de resultado y fin.

        No recibe parámetros adicionales. El texto se obtiene de ``self``.

        Returns:
            None: La respuesta se comunica mediante señales Qt.
        """
        # QThread ejecuta este método en el hilo de trabajo; las señales permiten
        # que la interfaz reciba el resultado sin bloquear su ciclo de eventos.
        respuesta = pensar_respuesta(self.texto)
        self.senal_respuesta.emit(respuesta)
        self.senal_fin.emit()

class InterfazCircular(QWidget):
    """Ventana sin marco con controles de texto y una animación circular.

    Proporciona una interfaz compacta para enviar comandos del sistema o
    solicitudes al motor de lenguaje, y puede moverse arrastrando su etiqueta.
    """

    def __init__(self):
        """Configura la ventana, sus controles y el temporizador de animación.

        No recibe parámetros. Construye la interfaz y conecta sus eventos.

        Returns:
            None: Inicializa la ventana.
        """
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(320, 320)

        self.angulo_rotacion = 0
        self.escala_pulso = 0.0
        
        self.timer_animacion = QTimer(self)
        self.timer_animacion.timeout.connect(self.actualizar_animacion)
        self.timer_animacion.start(16)

        self.contenedor = QFrame(self)
        self.contenedor.setFixedSize(320, 320)
        
        layout = QVBoxLayout(self.contenedor)
        layout.setAlignment(Qt.AlignCenter)

        self.lbl_estado = QLabel("O . S . I . R . I . S .")
        self.lbl_estado.setAlignment(Qt.AlignCenter)
        self.lbl_estado.setStyleSheet("color: #ffd700; font-weight: bold; font-family: 'Consolas', monospace; font-size: 18px; margin-top: 35px;")
        layout.addWidget(self.lbl_estado)

        self.lbl_respuesta = QLabel("Sistemas en línea.\nEsperando órdenes.")
        self.lbl_respuesta.setAlignment(Qt.AlignCenter)
        self.lbl_respuesta.setWordWrap(True)
        self.lbl_respuesta.setStyleSheet("color: #fcd12a; font-family: 'Consolas', monospace; font-size: 11px; margin: 5px 25px;")
        layout.addWidget(self.lbl_respuesta)

        self.input_texto = QLineEdit()
        self.input_texto.setPlaceholderText("Comando...")
        self.input_texto.setAlignment(Qt.AlignCenter)
        self.input_texto.setStyleSheet("""
            QLineEdit {
                background-color: rgba(10, 5, 0, 180); color: #ffbf00; border: 1.5px solid #d8a01b; 
                border-radius: 15px; padding: 5px 15px; margin-bottom: 5px; margin-left: 30px; margin-right: 30px;
                font-family: 'Consolas', monospace;
            }
            QLineEdit:focus { border: 1.5px solid #ffd700; background-color: rgba(20, 10, 0, 220); }
        """)
        self.input_texto.returnPressed.connect(self.procesar_comando)
        layout.addWidget(self.input_texto)

        self.btn_microfono = QPushButton("Microfono")
        self.btn_microfono.setFixedSize(40, 40)
        self.btn_microfono.setCursor(Qt.PointingHandCursor)
        self.btn_microfono.setStyleSheet("""
            QPushButton {
                background-color: rgba(10, 5, 0, 180);
                color: #ffd700;
                border: 1.5px solid #d8a01b;
                border-radius: 20px;
                font-size: 18px;
                margin-bottom: 25px;
            }
            QPushButton:hover {
                background-color: rgba(30, 15, 0, 220);
                border: 1.5px solid #ffd700;
            }
            QPushButton:pressed {
                background-color: #d8a01b;
                color: #000;
            }
        """)
        layout.addWidget(self.btn_microfono, alignment=Qt.AlignCenter)

        self.lbl_estado.mousePressEvent = self.iniciar_arrastre
        self.lbl_estado.mouseMoveEvent = self.arrastrar

    def paintEvent(self, event):
        """Dibuja el fondo, los anillos y las marcas radiales de la ventana.

        Args:
            event: Evento de pintura de Qt que solicita redibujar el widget.

        Returns:
            None: El dibujo se realiza directamente sobre el widget.
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QColor(15, 12, 5, 235))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(10, 10, 300, 300)

        pulso_anillo = 3 + (math.sin(self.escala_pulso) * 1.5)
        pen_exterior = QPen(QColor(216, 160, 27, 100))
        pen_exterior.setWidthF(pulso_anillo)
        painter.setPen(pen_exterior)
        painter.drawEllipse(15, 15, 290, 290)

        pen_interior = QPen(QColor(255, 215, 0, 200))
        pen_interior.setWidth(2)
        painter.setPen(pen_interior)
        
        for i in range(0, 360, 45):
            start_angle = (i + self.angulo_rotacion) * 16
            span_angle = 25 * 16
            painter.drawArc(25, 25, 270, 270, start_angle, span_angle)

        pen_ticks = QPen(QColor(255, 191, 0, 90))
        pen_ticks.setWidth(1)
        painter.setPen(pen_ticks)
        for i in range(0, 360, 15):
            angle_rad = math.radians(i - self.angulo_rotacion * 0.5)
            x1 = 160 + 125 * math.cos(angle_rad)
            y1 = 160 + 125 * math.sin(angle_rad)
            x2 = 160 + 132 * math.cos(angle_rad)
            y2 = 160 + 132 * math.sin(angle_rad)
            painter.drawLine(x1, y1, x2, y2)
        painter.end()

    def actualizar_animacion(self):
        """Avanza los parámetros de animación y solicita un nuevo dibujo.

        No recibe parámetros. Incrementa la rotación y la fase del pulso.

        Returns:
            None: Actualiza el estado visual del widget.
        """
        self.angulo_rotacion = (self.angulo_rotacion + 1) % 360
        self.escala_pulso += 0.05
        self.update()

    def procesar_comando(self):
        """Procesa el texto ingresado como acción del sistema o consulta.

        No recibe parámetros. Intenta ejecutar primero un comando local; si no
        corresponde a uno, inicia un ``WorkerOsiris`` para procesarlo en segundo
        plano.

        Returns:
            None: Actualiza la interfaz y, cuando corresponde, inicia un hilo.
        """
        texto = self.input_texto.text().strip()
        if not texto: return

        if texto.lower() == "ocultar":
            self.hide()
            self.input_texto.clear()
            return

        self.input_texto.clear()
        self.input_texto.setEnabled(False)

        respuesta_sistema = ejecutar_comando_sistema(texto)
        
        if respuesta_sistema:
            self.mostrar_respuesta(respuesta_sistema)
            self.restaurar_input()
            QTimer.singleShot(600, self.hide)
        else:
            self.lbl_respuesta.setText("Procesando...")
            self.lbl_respuesta.setStyleSheet("color: #ffa500; font-family: Consolas; font-size: 11px; margin: 5px 25px;")
            self.worker = WorkerOsiris(texto)
            self.worker.senal_respuesta.connect(self.mostrar_respuesta)
            self.worker.senal_fin.connect(self.restaurar_input)
            self.worker.start()

    def mostrar_respuesta(self, respuesta):
        """Presenta una respuesta en la etiqueta correspondiente.

        Args:
            respuesta: Texto que se mostrará en la ventana.

        Returns:
            None: Actualiza la etiqueta de respuesta.
        """
        self.lbl_respuesta.setText(respuesta)
        self.lbl_respuesta.setStyleSheet("color: #ffd700; font-family: Consolas; font-size: 11px; margin: 5px 25px;")

    def restaurar_input(self):
        """Habilita el campo de entrada y le devuelve el foco.

        No recibe parámetros.

        Returns:
            None: Restaura la disponibilidad del campo de texto.
        """
        self.input_texto.setEnabled(True)
        self.input_texto.setFocus()

    def iniciar_arrastre(self, event):
        """Registra la posición global inicial al pulsar la etiqueta.

        Args:
            event: Evento de ratón que contiene la posición global del cursor.

        Returns:
            None: Guarda la posición que servirá como origen del arrastre.
        """
        self.drag_pos = event.globalPosition().toPoint()

    def arrastrar(self, event):
        """Desplaza la ventana según el movimiento global del ratón.

        Args:
            event: Evento de movimiento que contiene la posición global actual.

        Returns:
            None: Mueve la ventana y actualiza la posición de referencia.
        """
        delta = event.globalPosition().toPoint() - self.drag_pos
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.drag_pos = event.globalPosition().toPoint()

def crear_icono_tray():
    """Crea un icono circular dorado para la bandeja del sistema.

    No recibe parámetros.

    Returns:
        QIcon: Icono generado a partir de un ``QPixmap`` transparente.
    """
    pixmap = QPixmap(64, 64)
    pixmap.fill(Qt.transparent)
    painter = QPainter(pixmap)
    painter.setBrush(QColor("#ffd700"))
    painter.setPen(Qt.NoPen)
    painter.drawEllipse(0, 0, 64, 64)
    painter.end()
    return QIcon(pixmap)