from pathlib import Path
import pygame as pg
from states import BaseState
from constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    BG_COLOR,
    TEXT_LIGHT_COLOR,
    START_BALANCE,
    GameState
)

OPTIONS_OFFSET = 100
OPTIONS_SPACE_BETWEEN = 50

class GameOverState(BaseState):
    """
    Game-Over-Zustand.
    Der Spieler ist bankrottgegangen.
    """

    def __init__(self) -> None:
        """
        Konstruktor.
        """

        super().__init__()

        self.font = pg.font.Font(None, 36)

        logo_path = Path("assets/png/logo_black.png")
        click_sound_path = Path("assets/ogg/click.ogg")

        # Logo laden und positionieren
        self.logo = pg.transform.scale(pg.image.load(logo_path), (440, 260))
        self.logo_rect = self.logo.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 130))

        # Game-Over-Text
        self.game_over_text = self.font.render("Game Over!", True, TEXT_LIGHT_COLOR)
        self.game_over_text_rect = self.game_over_text.get_rect(center=((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 35)))

        # Sounds laden
        self.click_sound = pg.mixer.Sound(click_sound_path)

        self.options = [
            "Neues Spiel",
            "Zurück zum Hauptmenü"
        ]

        self.options_choice = 0

    def init(self, _: dict) -> None:
        """
        Initialisiert anhaltende Daten beim Eintreten eines neuen Zustandes.
        """

        self.persistent_data = { "balance": START_BALANCE }

    def handle_enter(self) -> None:
        """
        Wird aufgerufen, sobald der Spieler die Enter-Taste drückt, und somit eine
        Option aus dem Menü auswählt.
        """

        if self.options_choice == 0:
            self.next_state = GameState.ANTE
        else:
            self.next_state = GameState.MENU

        self.is_done = True

    def handle_event(self, event: pg.event.Event) -> None:
        """
        Verarbeitet ein vom Spiel eingehendes Event.

        Parameter:
        - `event` (pg.event.Event) - Eingehendes Event.
        """

        if event.type == pg.QUIT:
            self.quit = True
            return

        if event.type == pg.KEYUP:
            # Pfeiltaste nach oben
            if event.key == pg.K_UP and self.options_choice - 1 >= 0:
                self.options_choice -= 1
                pg.mixer.Sound.play(self.click_sound)

            # Pfeiltaste nach unten
            elif event.key == pg.K_DOWN and self.options_choice + 1 < len(self.options):
                self.options_choice += 1
                pg.mixer.Sound.play(self.click_sound)
            
            # Enter
            elif event.key == pg.K_RETURN:
                self.handle_enter()

    def get_option_text_rect(self, option_text: pg.Surface, index: int) -> pg.Rect:
        """
        Platziert die jeweilige Option mittig und leicht nach unten verschoben.

        Parameter:
        - `option_text` (pg.Surface) - Gerenderter Text.
        - `index` (int)              - Index der jeweiligen Option (aus der `self.options`-Liste)
        """

        pos = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + (OPTIONS_SPACE_BETWEEN * index) + OPTIONS_OFFSET)
        return option_text.get_rect(center=pos)

    def render_option_text(self, index: int) -> pg.Surface:
        """
        Rendert die verfügbaren Optionen.

        Parameter:
        - `index` (int) - Index der jeweiligen rOption (aus der `self.options`-Liste)
        """

        option_content = self.options[index]    
        use_underline = self.options_choice == index

        self.font.set_underline(use_underline)

        return self.font.render(option_content, True, TEXT_LIGHT_COLOR)

    def render(self, screen: pg.Surface) -> None:
        """
        Elemente, die im Zustand gerendert werden.

        Parameter:
        - `screen` (pg.Surface) - Bildschirm, auf den gerendert wird.
        """

        screen.fill(BG_COLOR)

        screen.blit(self.logo, self.logo_rect)
        screen.blit(self.game_over_text, self.game_over_text_rect)
        
        for i, _ in enumerate(self.options):
            option_text = self.render_option_text(i)
            option_text_rect = self.get_option_text_rect(option_text, i)
            screen.blit(option_text, option_text_rect)