import pygame as pg
from states import BaseState, MenuState, AnteState
from constants import TITLE, SCREEN_WIDTH, SCREEN_HEIGHT, FPS, GameState

class Game:
    """
    Drei-Karten-Poker.

    Attribute:
    - `screen` (pg.Surface)             - Fläche, auf der das Spiel gerendert wird.
    - `is_running` (bool)               - Ob das Spiel am Laufen ist.
    - `states` (dict[str, BaseState])   - Zustände des Spiels.
    - `state_name` (str)                - Name des aktuellen Zustands.
    - `state` (BaseState)               - Aktueller Zustand.
    """

    def __init__(self) -> None:
        """
        Konstruktor.
        """

        pg.display.set_caption(TITLE)

        self.screen: pg.Surface = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock: pg.time.Clock = pg.time.Clock()

        self.fps: int = FPS
        self.is_running: bool = True

        self.states: dict[GameState, BaseState] = {
            GameState.MENU: MenuState(),
            GameState.ANTE: AnteState()
        }

        self.state_name: str = GameState.MENU
        self.state: BaseState = self.states[self.state_name]

    def event_loop(self) -> None:
        """
        Gibt alle eingehenden Events zum aktuellen Zustand zur Verarbeitung.
        """

        for event in pg.event.get():
            self.state.handle_event(event)

    def next_state(self) -> None:
        """
        Wechselt das Spiel in den nächsten Zustand.
        """

        next_state = self.state.next_state
        persistent_data = self.state.persistent_data

        self.state.is_done = False
        self.state_name = next_state

        self.state = self.states[self.state_name]
        self.state.init(persistent_data)

    def update_state(self, tick: int) -> None:
        """
        Aktualisiert den aktuellen Zustand.
        """

        if self.state.quit:
            self.is_running = False
            return

        if self.state.is_done:
            self.next_state()

        self.state.update(tick)

    def render(self) -> None:
        """
        Rendert die Elemente des aktuellen Zustandes.
        """

        self.state.render(self.screen)

    def run(self) -> None:
        """
        Führt das Spiel aus.
        """
        
        while self.is_running:
            tick = self.clock.tick(self.fps)
            self.event_loop()
            self.update_state(tick)
            self.render()
            pg.display.update()