import pygame as pg

class BaseState:
    """
    Zustand, in dem sich das Spiel befinden kann.

    Attribute:
    - `is_done` (bool)          - Ob der Zustand abgeschlossen ist.
    - `quit` (bool)             - Ob der Nutzer das Spiel verlassen möchte.
    - `next_state` (str)        - Name des darauffolgenden Zustands.
    - `persistent_data` (dict)  - Über alle Zustände anhaltende Daten.
    """

    def __init__(self) -> None:
        """
        Konstruktor.
        """

        self.is_done: bool = False
        self.quit: bool = False
        self.next_state: str = None
        self.persistent_data: dict = {}

    def init(self, persistent_data: dict) -> None:
        """
        Initialisiert anhaltende Daten beim Eintreten eines neuen Zustandes.

        Parameter:
        - `persistent_data` (dict) - Über Zustände anhaltende Daten.
        """

        self.persistent_data = persistent_data

    def update(self, tick: int) -> None:
        """
        Aktualisiert den Zustand.
        Kann von von individuellen Unterklassen implementiert werden.

        Parameter:
        - `tick` (int) - Wie viele Millisekunden seit dem letzten Update vergangen sind. 
        """

        pass

    def handle_event(self, event: pg.event.Event) -> None:
        """
        Verarbeitet ein vom Spiel eingehendes Event.
        Muss von von individuellen Unterklassen implementiert werden.

        Parameter:
        - `event` (pg.event.Event) - Eingehendes Event.
        """

        raise Exception("handle_event() nicht implementiert")

    def render(self, screen: pg.Surface) -> None:
        """
        Elemente, die im Zustand gerendert werden.
        Muss von von individuellen Unterklassen implementiert werden.

        Parameter:
        - `screen` (pg.Surface) - Bildschirm, auf den gerendert wird.
        """

        raise Exception("render() nicht implementiert")