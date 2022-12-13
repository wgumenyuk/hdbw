import os.path as path
import pygame as pg
from states import BaseState
from constants import BG_COLOR, TEXT_LIGHT_COLOR, SCREEN_WIDTH, SCREEN_HEIGHT, GameState

OPTIONS_OFFSET = 100
OPTIONS_SPACE_BETWEEN = 50

class MenuState(BaseState):
    """
    Menü-Zustand.
    Das Spiel startet in diesem Zustand, und ermöglicht dem Spieler, ein neues Spiel zu
    starten oder es zu beenden.
    """

    def __init__(self) -> None:
        """
        Konstruktor.
        """

        super().__init__()

        self.next_state = GameState.ANTE
        self.persistent_data = { "balance": 0 }
        self.font = pg.font.Font(None, 36)

        base_path = path.join(path.dirname(path.abspath(__file__)), "../../assets/")
        logo_path = path.join(base_path, "png/logo_black.png")
        click_sound_path = path.join(base_path, "ogg/click.ogg")

        # Logo laden und positionieren
        self.logo = pg.transform.scale(pg.image.load(logo_path), (440, 260))
        self.logo_rect = self.logo.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 130))

        # Sounds laden
        self.click_sound = pg.mixer.Sound(click_sound_path)

        self.options = [
            "Neues Spiel",
            "Spiel beenden"
        ]

        self.options_choice = 0

    def handle_enter(self) -> None:
        """
        Wird aufgerufen, sobald der Spieler die Enter-Taste drückt, und somit eine
        Option im Menü auswählt.
        """

        if self.options_choice == 0:
            self.is_done = True
        else:
            self.quit = True

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

    def get_option_text_pos(self, option_text: pg.Surface, index: int) -> pg.Rect:
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
        - `index` (int) - Index der jeweiligen Option (aus der `self.options`-Liste)
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
        
        for i, _ in enumerate(self.options):
            option_text = self.render_option_text(i)
            option_text_rect = self.get_option_text_pos(option_text, i)
            screen.blit(option_text, option_text_rect)