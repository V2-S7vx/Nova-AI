import math

from OpenGL.GL import *




class NovaHub:


    def __init__(self):

        self.time = 0
        self.pulse = 0



    def update(self, delta):

        self.time += delta

        self.pulse = (
            math.sin(self.time * 2.5) + 1
        ) / 2



    # ==========================================
    # PRIMITIVES
    # ==========================================

    def circle(self, radius, color, width=2, alpha=1):

        glLineWidth(width)

        glColor4f(
            color[0],
            color[1],
            color[2],
            alpha
        )

        glBegin(GL_LINE_LOOP)

        for i in range(240):

            a = math.pi * 2 * i / 240

            glVertex2f(
                math.cos(a) * radius,
                math.sin(a) * radius
            )

        glEnd()



    def arc(self, radius, start, end, color, width=3, alpha=1):

        glLineWidth(width)

        glColor4f(
            color[0],
            color[1],
            color[2],
            alpha
        )

        glBegin(GL_LINE_STRIP)

        for i in range(60):

            a = start + (end - start) * i / 60

            glVertex2f(
                math.cos(a) * radius,
                math.sin(a) * radius
            )

        glEnd()



    # ==========================================
    # COLOURS
    # ==========================================
    # Shifted from the earlier teal toward a deeper,
    # more restrained blue.

    RING_COLOR = (
        0.14,
        0.33,
        0.65
    )

    GLOW_COLOR = (
        0.05,
        0.14,
        0.35
    )

    ACCENT_COLOR = (
        0.55,
        0.69,
        0.92
    )

    DIM_COLOR = (
        0.10,
        0.24,
        0.47
    )



    # ==========================================
    # RING
    # ==========================================
    # Main ring + glow, then a handful of extra
    # detail layers around it: graduated tick marks,
    # a slow rotating dashed orbit ring, small node
    # markers at the cardinal points, and a couple of
    # quiet counter-rotating arcs just inside the ring.
    # Nothing here is filled, so the starfield behind
    # still shows straight through the middle.

    def draw_ring(self):

        radius = 0.5


        # soft outer glow

        for i in range(9, 0, -1):

            self.circle(
                radius + i * 0.005,
                self.GLOW_COLOR,
                width=i * 3,
                alpha=0.05
            )


        # gentle breathing thickness on the main ring

        pulse_width = 2.2 + self.pulse * 0.7


        # crisp main ring

        self.circle(
            radius,
            self.RING_COLOR,
            width=pulse_width,
            alpha=0.85
        )


        # faint inner ring for a touch of depth

        self.circle(
            radius - 0.017,
            self.RING_COLOR,
            width=1,
            alpha=0.2
        )


        self.draw_ticks(radius)
        self.draw_outer_orbit(radius)
        self.draw_inner_arcs(radius)
        self.draw_cardinal_nodes(radius)
        self.draw_brackets(radius)



    # ==========================================
    # TICK MARKS (major / medium / minor)
    # ==========================================
    # A dial-style graduation ring just outside the
    # main ring, three tiers deep so it reads as
    # detailed without turning into visual noise.

    def draw_ticks(self, radius):

        count = 72

        glBegin(GL_LINES)

        for i in range(count):

            a = math.pi * 2 * i / count

            if i % 6 == 0:
                outer_r, alpha, width = radius + 0.031, 0.55, 2
            elif i % 2 == 0:
                outer_r, alpha, width = radius + 0.019, 0.28, 1
            else:
                outer_r, alpha, width = radius + 0.012, 0.15, 1

            inner_r = radius + 0.010

            glColor4f(
                self.RING_COLOR[0],
                self.RING_COLOR[1],
                self.RING_COLOR[2],
                alpha
            )

            glVertex2f(
                math.cos(a) * inner_r,
                math.sin(a) * inner_r
            )

            glVertex2f(
                math.cos(a) * outer_r,
                math.sin(a) * outer_r
            )

        glEnd()



    # ==========================================
    # OUTER ORBIT RING
    # ==========================================
    # A slow rotating ring of short dashes further
    # out - reads like a satellite/orbit trace.

    def draw_outer_orbit(self, radius):

        orbit_r = radius + 0.065

        dash_count = 40

        dash_len = 0.07

        rotation = self.time * 0.22

        for i in range(dash_count):

            start = (
                (math.pi * 2 / dash_count) * i
                + rotation
            )

            self.arc(
                orbit_r,
                start,
                start + dash_len,
                self.DIM_COLOR,
                width=2,
                alpha=0.4
            )



    # ==========================================
    # INNER ARCS
    # ==========================================
    # Two quiet counter-rotating arcs just inside
    # the ring - subtle motion, no fill.

    def draw_inner_arcs(self, radius):

        inner_r = radius - 0.046

        rotation = -self.time * 0.5

        self.arc(
            inner_r,
            rotation,
            rotation + 1.2,
            self.RING_COLOR,
            width=2,
            alpha=0.35
        )

        self.arc(
            inner_r,
            rotation + 2.6,
            rotation + 3.3,
            self.RING_COLOR,
            width=2,
            alpha=0.22
        )



    # ==========================================
    # CARDINAL NODE MARKERS
    # ==========================================
    # Small diamond markers sitting right on the
    # ring at 12/3/6/9 o'clock.

    def draw_cardinal_nodes(self, radius):

        size = 0.010

        glColor4f(
            self.ACCENT_COLOR[0],
            self.ACCENT_COLOR[1],
            self.ACCENT_COLOR[2],
            0.9
        )

        glBegin(GL_QUADS)

        for i in range(4):

            a = i * (math.pi / 2)

            cx = math.cos(a) * (radius + 0.006)
            cy = math.sin(a) * (radius + 0.006)

            glVertex2f(cx, cy + size)
            glVertex2f(cx + size, cy)
            glVertex2f(cx, cy - size)
            glVertex2f(cx - size, cy)

        glEnd()



    # ==========================================
    # CARDINAL BRACKETS
    # ==========================================
    # Four short brighter arcs at 12/3/6/9 o'clock,
    # like a reticle - subtle, not shouting.

    def draw_brackets(self, radius):

        spread = 0.14

        for i in range(4):

            centre = i * (math.pi / 2)

            self.arc(
                radius + 0.006,
                centre - spread,
                centre + spread,
                self.ACCENT_COLOR,
                width=3,
                alpha=0.8
            )



    # ==========================================
    # DRAW
    # ==========================================

    def draw(self):

        glDisable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)

        glBlendFunc(
            GL_SRC_ALPHA,
            GL_ONE_MINUS_SRC_ALPHA
        )


        # ring only - no background fill, so the
        # starfield stays visible in the middle. The
        # N.O.V.A label is handled by the PyQt overlay
        # (hud/overlay.py), not here.

        self.draw_ring()


        glDisable(GL_BLEND)
        glEnable(GL_DEPTH_TEST)

