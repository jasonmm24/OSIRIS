from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input, RichLog
from textual import work

# Importamos nuestra lógica modular exacta
from core.system import ejecutar_comando_sistema
from core.llm import inicializar_motor, pensar_respuesta

class OsirisTUI(App):
    """Interfaz de Terminal (TUI) para O.S.I.R.I.S."""
    
    # Actualizamos el CSS para apuntar a RichLog
    CSS = """
    Screen {
        background: #050505;
    }
    RichLog {
        border: solid #d8a01b;
        background: #0a0802;
        color: #ffd700;
        padding: 1 2;
        height: 1fr;
    }
    Input {
        border: tall #d8a01b;
        background: #140a00;
        color: #ffbf00;
        dock: bottom;
        margin: 1 0;
    }
    Input:focus {
        border: tall #ffd700;
    }
    """

    BINDINGS = [
        ("q", "quit", "Salir de O.S.I.R.I.S."),
        ("ctrl+l", "limpiar", "Limpiar pantalla")
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        # Cambiamos Log por RichLog y activamos markup
        yield RichLog(id="consola_salida", highlight=True, markup=True)
        yield Input(placeholder="Ingresa un comando...", id="entrada_texto")
        yield Footer()

    def on_mount(self) -> None:
        self.title = "O.S.I.R.I.S. - MODO TERMINAL"
        consola = self.query_one(RichLog)
        
        # Usamos write en lugar de write_line
        consola.write("[bold #ffd700]Iniciando motor neuronal...[/]")
        inicializar_motor()
        consola.write("[bold green]Sistemas en línea. Interfaz de terminal lista.[/]")

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        texto = event.value.strip()
        if not texto: return

        input_box = self.query_one(Input)
        consola = self.query_one(RichLog)

        input_box.value = ""
        
        if texto.lower() in ["salir", "exit", "quit"]:
            self.exit()
            return

        consola.write(f"\n[bold white]Tú:[/] {texto}")

        respuesta_sistema = ejecutar_comando_sistema(texto)
        if respuesta_sistema:
            consola.write(f"[bold cyan]O.S.I.R.I.S.:[/] {respuesta_sistema}")
        else:
            consola.write("[italic #ffa500]Procesando datos...[/]")
            self.procesar_llm(texto)

    @work(thread=True)
    def procesar_llm(self, texto: str) -> None:
        respuesta = pensar_respuesta(texto)
        self.call_from_thread(self.mostrar_respuesta_llm, respuesta)

    def mostrar_respuesta_llm(self, respuesta: str) -> None:
        consola = self.query_one(RichLog)
        consola.write(f"[bold #ffd700]O.S.I.R.I.S.:[/] {respuesta}")

    def action_limpiar(self) -> None:
        consola = self.query_one(RichLog)
        consola.clear()
        consola.write("[bold green]Pantalla limpiada. Sistemas en línea.[/]")

def main():
    app = OsirisTUI()
    app.run()

if __name__ == "__main__":
    main()