# ==========================================================
# NOVA CINEMATIC HUD OVERLAY
# JARVIS STYLE INTERFACE LAYER
# ==========================================================


from PySide6.QtWidgets import QWidget

from PySide6.QtCore import (
    Qt,
    QTimer
)

from PySide6.QtGui import (
    QPainter,
    QColor,
    QFont,
    QPainterPath,
    QPen,
    QBrush
)


import psutil
import math


from engine import config

from hud import config as hud_config






class NovaHUD(QWidget):


    def __init__(
            self,
            parent=None
    ):

        super().__init__(
            parent
        )


        self.setAttribute(
            Qt.WA_TransparentForMouseEvents
        )


        self.setAttribute(
            Qt.WA_TranslucentBackground
        )




        # ==========================================
        # TITLE ANIMATION
        # ==========================================

        self.title_time = 0




        # ==========================================
        # TELEMETRY
        # ==========================================

        self.cpu = 0

        self.memory = 0

        self.gpu = 0




        self.time = 0




        self.timer = QTimer(
            self
        )


        self.timer.timeout.connect(
            self.animate
        )


        self.timer.start(
            16
        )









    # ==========================================
    # UPDATE
    # ==========================================

    def animate(
            self
    ):


        self.title_time += 1

        self.time += 1


        self.cpu = psutil.cpu_percent()


        self.memory = (

            psutil.virtual_memory()
            .percent
        )


        self.update()









    # ==========================================
    # TITLE BRIGHTNESS
    # ==========================================

    def get_title_brightness(
            self
    ):


        t = self.title_time




        fade_in = hud_config.TITLE_FADE_IN_FRAMES


        hold = hud_config.TITLE_WHITE_HOLD_FRAMES


        fade_out = hud_config.TITLE_FADE_OUT_FRAMES




        # Fade from black to white

        if t < fade_in:


            return int(

                255 *
                (
                    t /
                    fade_in
                )
            )




        # Stay white

        elif t < (
            fade_in +
            hold
        ):


            return 255






        # Fade white back to black

        elif t < (
            fade_in +
            hold +
            fade_out
        ):


            progress = (
                t -
                fade_in -
                hold
            ) / fade_out




            return int(
                255 *
                (
                    1 -
                    progress
                )
            )




        else:


            self.title_time = 0


            return 0











    # ==========================================
    # DRAW
    # ==========================================

    def paintEvent(
            self,
            event
    ):


        painter = QPainter(
            self
        )


        painter.setRenderHint(
            QPainter.Antialiasing
        )


        width = self.width()
        height = self.height()





        # ==========================================
        # V2 DEVELOPMENT
        # ==========================================


        brightness = self.get_title_brightness()





        painter.setFont(
            QFont(
                hud_config.TITLE_FONT,
                hud_config.TITLE_FONT_SIZE
            )
        )


        painter.setPen(
            QColor(
                brightness,
                brightness,
                brightness
            )
        )


        title = "V2 DEVELOPMENT"




        text_width = (
            painter.fontMetrics()
            .horizontalAdvance(
                title
            )
        )


        painter.drawText(
            (
                width -
                text_width
            )
            //
            2,
            hud_config.TITLE_Y,
            title
        )





        # ==========================================
        # NOVA CORE LABEL
        # ==========================================
        # Sits centred inside the reactor ring drawn
        # by hud/nova_hud.py. Plain Qt text (not the
        # pixel-point font used for the boot sequence)
        # so it stays crisp at any size - but built as
        # a QPainterPath so it can glow the same way
        # the ring does: a few soft, wide, low-alpha
        # strokes behind a crisp fill on top.

        core_font = QFont(
            hud_config.CORE_LABEL_FONT,
            hud_config.CORE_LABEL_FONT_SIZE
        )
        core_font.setBold(True)
        core_font.setLetterSpacing(
            QFont.AbsoluteSpacing,
            hud_config.CORE_LABEL_LETTER_SPACING
        )
        painter.setFont(
            core_font
        )
        core_label = "N.O.V.A"
        core_metrics = painter.fontMetrics()
        core_label_width = (
            core_metrics.horizontalAdvance(
                core_label
            )
        )
        core_x = (
            (
                width -
                core_label_width
            )
            //
            2
        )
        core_y = (
            (
                height //
                2
            )
            +
            hud_config.CORE_LABEL_Y_OFFSET
        )
        core_path = QPainterPath()
        core_path.addText(
            core_x,
            core_y,
            core_font,
            core_label
        )
        glow_colour = QColor(
            hud_config.CORE_LABEL_GLOW_RED,
            hud_config.CORE_LABEL_GLOW_GREEN,
            hud_config.CORE_LABEL_GLOW_BLUE
        )
        painter.setBrush(Qt.NoBrush)
        # soft halo - several wide, faint strokes,
        # narrowing and brightening each pass
        for glow_width, glow_alpha in (
            (14, 20),
            (10, 35),
            (6, 60),
            (3, 100)
        ):
            glow_colour.setAlpha(
                glow_alpha
            )
            glow_pen = QPen(
                glow_colour
            )
            glow_pen.setWidthF(
                glow_width
            )
            glow_pen.setJoinStyle(
                Qt.RoundJoin
            )
            glow_pen.setCapStyle(
                Qt.RoundCap
            )
            painter.setPen(
                glow_pen
            )
            painter.drawPath(
                core_path
            )
        # crisp fill on top of the glow
        painter.setPen(Qt.NoPen)
        painter.setBrush(
            QBrush(
                QColor(
                    hud_config.CORE_LABEL_RED,
                    hud_config.CORE_LABEL_GREEN,
                    hud_config.CORE_LABEL_BLUE
                )
            )
        )
        painter.drawPath(
            core_path
        )
        painter.setBrush(Qt.NoBrush)




        # ==========================================
        # LEFT STATUS
        # ==========================================


        painter.setFont(
            QFont(
                hud_config.HUD_FONT,
                hud_config.HUD_FONT_SIZE
            )
        )




        systems = [
            "NOVA GPU PIPELINE // ONLINE",
            "GPU RENDERER // ONLINE",
            "HOLOGRAM HUD // ONLINE",
            "NOVA AI SYSTEM // ONLINE"
        ]





        for i,text in enumerate(
            systems
        ):


            painter.setPen(
                QColor(
                    hud_config.HUD_RED,
                    hud_config.HUD_GREEN,
                    hud_config.HUD_BLUE
                )
            )


            painter.drawText(
                hud_config.LEFT_HUD_X,
                (
                    height //
                    2
                    +
                    hud_config.LEFT_HUD_Y_OFFSET
                    +
                    i *
                    hud_config.LEFT_HUD_SPACING
                ),
                text
            )








        # ==========================================
        # TELEMETRY
        # ==========================================


        telemetry = [
            f"MEMORY USAGE // {self.memory:.1f}%",
            f"CPU LOAD // {self.cpu:.1f}%",
            f"GPU POWER // {self.gpu:.1f}%"
        ]





        for i,text in enumerate(
            telemetry
        ):


            painter.drawText(
                width -
                hud_config.RIGHT_HUD_OFFSET_X,
                height -
                hud_config.RIGHT_HUD_OFFSET_Y
                +
                (
                    i *
                    hud_config.RIGHT_HUD_SPACING
                ),
                text
            )





        painter.end()