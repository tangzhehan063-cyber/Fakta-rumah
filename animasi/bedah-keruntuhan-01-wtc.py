"""Bedah Keruntuhan #01 · WTC 1 dan 2. Animasi Manim, 1080x1920, ±55 dtk, tanpa suara.

Naskah : naskah/bedah-keruntuhan-01-wtc.md
Riset  : riset/bedah-keruntuhan-01-wtc.md
Render : manim -r 540,960 --fps 30 animasi/bedah-keruntuhan-01-wtc.py BedahWTC  (pratinjau)
         manim -r 1080,1920 --fps 30 ...                                          (final)
Semua bentuk disederhanakan. Kurva kekuatan baja hanya ilustrasi (tanpa angka).
Zona aman Shorts: bagian bawah (y < -2.4) tertutup antarmuka, jadi isi utama di atasnya.
"""
import numpy as np
from manim import *

config.pixel_width = 1080
config.pixel_height = 1920
config.frame_height = 8
config.frame_width = 4.5

BG = "#0b1a2e"
CHALK = "#e8efe9"
HEAT = "#ff7a2f"
GOLD = "#ffd166"
RED = "#e5484d"
STEEL = "#6fa8dc"
GREY = "#8b95a1"
FONT = "Inter"

GROUND = -1.9      # dasar penampang
X_COL = 1.3        # posisi tiang tepi
FLOORS = [-1.4, -0.8, -0.2]
TOP_Y = 0.2        # batas bawah blok atas


def T(s, size=30, color=CHALK, bold=False, w=4.0, **kw):
    t = Text(s, font=FONT, font_size=size, color=color,
             weight=BOLD if bold else NORMAL, **kw)
    if t.width > w:
        t.scale_to_fit_width(w)
    return t


def flame(scale=1.0, at=ORIGIN):
    outer = Triangle(color=HEAT, fill_opacity=1, stroke_width=0).scale(0.28 * scale)
    inner = Triangle(color=GOLD, fill_opacity=1, stroke_width=0).scale(0.14 * scale)
    inner.move_to(outer.get_bottom() + UP * 0.1 * scale)
    return VGroup(outer, inner).move_to(at)


def floor_curve(y, depth):
    return ParametricFunction(
        lambda t: np.array([t, y - depth * np.sin(np.pi * (t + X_COL) / (2 * X_COL)), 0]),
        t_range=[-X_COL, X_COL], color=CHALK, stroke_width=3)


def column_curve(sign, bow, kink=0.0):
    """sign=-1 kolom kiri, +1 kolom kanan; bow = lengkung ke arah dalam."""
    span = TOP_Y - GROUND
    return ParametricFunction(
        lambda t: np.array([
            sign * X_COL - sign * (bow * np.sin(np.pi * (t - GROUND) / span)
                                   + kink * np.sin(3 * np.pi * (t - GROUND) / span)),
            t, 0]),
        t_range=[GROUND, TOP_Y], color=STEEL, stroke_width=6)


class BedahWTC(Scene):
    def hold(self, until):
        self.wait(max(0.01, until - self.renderer.time))

    def cap(self, text, size=30, color=CHALK):
        new = T(text, size, color, bold=True, w=4.0, line_spacing=0.9).move_to([0, 3.0, 0])
        if getattr(self, "_cap", None) is not None:
            self.play(FadeOut(self._cap, shift=UP * 0.1), FadeIn(new, shift=UP * 0.1), run_time=0.4)
        else:
            self.play(FadeIn(new), run_time=0.4)
        self._cap = new

    def clear_stage(self, keep=()):
        stuff = [m for m in self.mobjects if m not in keep]
        if stuff:
            self.play(*[FadeOut(m) for m in stuff], run_time=0.4)
        self._cap = None

    def construct(self):
        self.camera.background_color = BG
        self._cap = None
        foot = VGroup(
            T("Diagram disederhanakan, bukan skala asli", 13, GREY),
            T("Sumber: NIST NCSTAR 1", 13, GREY),
        ).arrange(DOWN, buff=0.05).move_to([0, -2.65, 0])
        self.add(foot)

        # ---------- 1 · HOOK (0-3 dtk)
        tower = Rectangle(width=1.0, height=3.6, color=CHALK, stroke_width=3).move_to([0, -0.1, 0])
        grid = VGroup(*[Line([-0.5, y, 0], [0.5, y, 0], color=CHALK, stroke_width=1, stroke_opacity=0.4)
                        for y in np.linspace(-1.7, 1.5, 17)])
        grid.add(*[Line([x, -1.9, 0], [x, 1.7, 0], color=CHALK, stroke_width=1, stroke_opacity=0.4)
                   for x in np.linspace(-0.4, 0.4, 5)])
        fl = flame(1.2, [0, 2.0, 0])
        title = T("Gedung baja runtuh\ncuma karena api?", 36, bold=True, line_spacing=0.9).move_to([0, 3.0, 0])
        self.play(Create(tower), Create(grid), run_time=1.0)
        self.play(FadeIn(fl, scale=0.5), Write(title), run_time=1.0)
        self.play(fl.animate.scale(1.15), rate_func=there_and_back, run_time=0.8)
        self.hold(3.0)

        # ---------- 2 · SUHU API vs LELEH BAJA (3-10)
        self.play(FadeOut(tower), FadeOut(grid), FadeOut(fl), FadeOut(title), run_time=0.4)
        base = -1.6
        unit = 1.8 / 1000.0  # tinggi per derajat (ilustrasi linear)
        bar_a = Rectangle(width=0.7, height=1000 * unit, color=HEAT, fill_opacity=0.9, stroke_width=0)
        bar_a.move_to([-1.35, base + 1000 * unit / 2, 0])
        bar_b = Rectangle(width=0.7, height=1500 * unit, color=STEEL, fill_opacity=0.9, stroke_width=0)
        bar_b.move_to([0.4, base + 1500 * unit / 2, 0])
        lab_a = VGroup(T("±1.000 °C", 26, HEAT, True, w=1.6),
                       T("suhu udara\nmaks (NIST)", 16, CHALK, w=1.6, line_spacing=0.9)).arrange(DOWN, buff=0.08)
        lab_a.next_to(bar_a, UP, buff=0.12)
        lab_b = VGroup(T("±1.500 °C", 26, STEEL, True, w=1.6),
                       T("baja meleleh\n(perkiraan)", 16, CHALK, w=1.6, line_spacing=0.9)).arrange(DOWN, buff=0.08)
        lab_b.next_to(bar_b, UP, buff=0.12)
        self.cap("Api ±1.000 °C.\nBaja meleleh jauh di atasnya.", 28)
        self.play(GrowFromEdge(bar_a, DOWN), GrowFromEdge(bar_b, DOWN), run_time=1.6)
        self.play(FadeIn(lab_a), FadeIn(lab_b), run_time=0.6)
        dash = DashedLine([-1.0, base + 1000 * unit, 0], [0.9, base + 1000 * unit, 0], color=CHALK, stroke_width=2)
        brace = Brace(Line([0.95, base + 1000 * unit, 0], [0.95, base + 1500 * unit, 0]), RIGHT, color=GOLD, buff=0.05)
        gap = T("masih\njauh", 16, GOLD, True, w=0.9, line_spacing=0.9).next_to(brace, RIGHT, buff=0.05)
        self.play(Create(dash), GrowFromCenter(brace), FadeIn(gap), run_time=1.0)
        self.hold(10.0)

        # ---------- 3 · LEMAS, BUKAN LELEH (10-18)
        self.clear_stage(keep=[foot])
        ax = Axes(x_range=[0, 1, 1], y_range=[0, 1, 1], x_length=3.0, y_length=2.4, tips=False,
                  axis_config={"color": CHALK, "stroke_width": 3, "include_ticks": False}).move_to([0, 0.0, 0])
        x_lab = T("suhu →", 18, GREY).next_to(ax, DOWN, buff=0.1)
        y_lab = T("kekuatan baja", 18, GREY).rotate(PI / 2).next_to(ax, LEFT, buff=0.1)
        self.cap("Baja nggak perlu meleleh.\nCukup jadi lemas.", 28)
        self.play(Create(ax), FadeIn(x_lab), FadeIn(y_lab), run_time=0.8)
        f = lambda x: 0.05 + 0.95 / (1 + np.exp(9 * (x - 0.6)))
        curve = ax.plot(f, x_range=[0.0, 1.0], color=STEEL, stroke_width=6)
        self.play(Create(curve), run_time=2.0)
        melt = DashedLine(ax.c2p(1.0, 0), ax.c2p(1.0, 1.0), color=RED)
        melt_t = T("meleleh", 16, RED, True, w=1.0).next_to(melt, UP, buff=0.05).shift(LEFT * 0.2)
        zone = Rectangle(width=ax.c2p(0.97, 0)[0] - ax.c2p(0.66, 0)[0], height=ax.y_length * 0.5,
                         color=HEAT, fill_opacity=0.25, stroke_width=0)
        zone.move_to([(ax.c2p(0.97, 0)[0] + ax.c2p(0.66, 0)[0]) / 2, ax.c2p(0, 0)[1] + ax.y_length * 0.25, 0])
        zone_t = T("lemas,\nbelum meleleh", 18, HEAT, True, w=1.5, line_spacing=0.9).move_to(ax.c2p(0.78, 0.74))
        dot = Dot(ax.c2p(0.0, f(0.0)), color=GOLD, radius=0.08)
        self.play(Create(melt), FadeIn(melt_t), FadeIn(zone), FadeIn(zone_t), FadeIn(dot), run_time=0.8)
        self.play(MoveAlongPath(dot, curve), run_time=2.0, rate_func=smooth)
        note = T("bentuk kurva ilustrasi", 14, GREY).next_to(x_lab, DOWN, buff=0.1)
        self.play(FadeIn(note), run_time=0.4)
        self.hold(18.0)

        # ---------- 4 · PELINDUNG API TERKELUPAS (18-26)
        self.clear_stage(keep=[foot])
        self.cap("Pelindung api\nterkelupas", 30)
        beam = Rectangle(width=3.2, height=0.3, color=STEEL, fill_opacity=1, stroke_width=0).move_to([0, 0.3, 0])
        coat = Rectangle(width=3.5, height=0.6, color=GREY, fill_opacity=0.85, stroke_width=0).move_to(beam)
        lab_c = T("lapisan pelindung api", 18, CHALK).next_to(coat, UP, buff=0.35)
        arr_c = Arrow(lab_c.get_bottom(), coat.get_top(), buff=0.05, color=CHALK, stroke_width=3,
                      max_tip_length_to_length_ratio=0.3)
        self.play(FadeIn(beam), FadeIn(coat), FadeIn(lab_c), GrowArrow(arr_c), run_time=1.2)
        self.wait(0.6)
        hit = Star(n=8, outer_radius=0.55, inner_radius=0.25, color=RED, fill_opacity=1, stroke_width=0)
        hit.move_to([-2.0, 0.3, 0])
        hit_t = T("tabrakan", 18, RED, True, w=1.0).next_to(hit, DOWN, buff=0.1)
        self.play(GrowFromCenter(hit), FadeIn(hit_t), run_time=0.4)
        rng = np.random.default_rng(7)
        chunks = VGroup(*[Square(0.18, color=GREY, fill_opacity=1, stroke_width=0)
                          .move_to([x, 0.3, 0]) for x in np.linspace(-1.4, 1.4, 8)])
        self.play(
            FadeOut(coat), FadeOut(lab_c), FadeOut(arr_c), FadeIn(chunks, run_time=0.1),
            *[c.animate.shift([rng.uniform(-0.6, 0.6), rng.uniform(0.6, 1.4), 0]).set_opacity(0)
              for c in chunks], run_time=1.0)
        self.play(FadeOut(hit), FadeOut(hit_t), run_time=0.3)
        flames = VGroup(*[flame(1.0, [x, -0.25, 0]) for x in (-1.1, -0.35, 0.4, 1.15)])
        self.play(beam.animate.set_color(HEAT), FadeIn(flames, lag_ratio=0.2), run_time=1.5)
        warn = T("baja langsung\nkena panas", 22, GOLD, True, line_spacing=0.9).move_to([0, 1.5, 0])
        self.play(FadeIn(warn), run_time=0.5)
        self.hold(26.0)

        # ---------- 5 · LANTAI MELOROT, TIANG DITARIK (26-36)
        self.clear_stage(keep=[foot])
        self.cap("Lantai melorot,\ntiang ditarik ke dalam", 28)
        col_l, col_r = column_curve(-1, 0), column_curve(1, 0)
        core = Rectangle(width=0.7, height=TOP_Y - GROUND, color=GREY, fill_opacity=0.5, stroke_width=0)
        core.move_to([0, (TOP_Y + GROUND) / 2, 0])
        floors = VGroup(*[floor_curve(y, 0) for y in FLOORS])
        glow = Rectangle(width=2.6, height=1.5, color=HEAT, fill_opacity=0.22, stroke_width=0).move_to([0, -0.8, 0])
        block = Rectangle(width=3.0, height=1.4, color=CHALK, fill_opacity=0.18, stroke_width=3).move_to([0, TOP_Y + 0.7, 0])
        block_t = T("bagian atas\n(beban)", 20, CHALK, line_spacing=0.9).move_to(block)
        ground = Line([-1.9, GROUND, 0], [1.9, GROUND, 0], color=CHALK, stroke_width=4)
        self.play(Create(ground), Create(core), Create(col_l), Create(col_r), Create(floors),
                  FadeIn(block), FadeIn(block_t), run_time=2.0)
        self.play(FadeIn(glow), run_time=0.6)
        fl5 = VGroup(*[flame(0.8, [x, -1.65, 0]) for x in (-0.9, 0.0, 0.9)])
        self.play(FadeIn(fl5), run_time=0.4)
        self.play(*[Transform(floors[i], floor_curve(FLOORS[i], 0.28)) for i in range(3)],
                  run_time=2.4, rate_func=smooth)
        arrows = VGroup(
            Arrow([-1.75, -0.8, 0], [-1.35, -0.8, 0], color=GOLD, buff=0, stroke_width=6),
            Arrow([1.75, -0.8, 0], [1.35, -0.8, 0], color=GOLD, buff=0, stroke_width=6),
        )
        pull = T("lantai menarik\ntiang ke dalam", 18, GOLD, True, line_spacing=0.9).move_to([0, 2.0, 0])
        self.play(GrowArrow(arrows[0]), GrowArrow(arrows[1]), FadeIn(pull), run_time=0.8)
        self.play(Transform(col_l, column_curve(-1, 0.22)), Transform(col_r, column_curve(1, 0.22)),
                  run_time=2.0)
        self.hold(36.0)

        # ---------- 6 · TIANG TEKUK, BAGIAN ATAS JATUH (36-45)
        self.play(FadeOut(arrows), FadeOut(pull), run_time=0.3)
        self.cap("Tiang tekuk,\nbagian atas jatuh", 30)
        self.play(Transform(col_l, column_curve(-1, 0.5, 0.12)), Transform(col_r, column_curve(1, 0.5, 0.12)),
                  run_time=1.6)
        lower = VGroup(core, col_l, col_r, floors, glow, fl5)
        self.play(
            block.animate.shift(DOWN * 1.36), block_t.animate.shift(DOWN * 1.36),
            lower.animate.stretch(0.35, 1, about_point=np.array([0, GROUND, 0])),
            run_time=1.4, rate_func=rush_into)
        self.wait(0.3)
        shock = T("bagian atas menimpa\nlantai di bawahnya", 20, GOLD, True, line_spacing=0.9).move_to([0, 1.3, 0])
        self.play(FadeIn(shock), run_time=0.5)
        self.hold(45.0)

        # ---------- 7 · BUKTI: TIANG MELENGKUNG 5 MENIT SEBELUM (45-50)
        self.clear_stage(keep=[foot])
        self.cap("Tiang melengkung ke dalam\nlima menit sebelum runtuh", 26)
        line = Line([-1.7, 0.2, 0], [1.7, 0.2, 0], color=CHALK, stroke_width=4)
        t1, t2 = Dot([-1.0, 0.2, 0], color=GOLD, radius=0.1), Dot([1.0, 0.2, 0], color=RED, radius=0.1)
        l1 = VGroup(T("10:23", 30, GOLD, True, w=1.4), T("tiang\nmelengkung", 16, CHALK, w=1.4, line_spacing=0.9)
                    ).arrange(DOWN, buff=0.08).next_to(t1, UP, buff=0.2)
        l2 = VGroup(T("10:28", 30, RED, True, w=1.4), T("runtuh\nmulai", 16, CHALK, w=1.4, line_spacing=0.9)
                    ).arrange(DOWN, buff=0.08).next_to(t2, UP, buff=0.2)
        br = Brace(Line([-1.0, 0.2, 0], [1.0, 0.2, 0]), DOWN, color=CHALK, buff=0.15)
        br_t = T("5 menit", 24, CHALK, True, w=1.6).next_to(br, DOWN, buff=0.1)
        src = T("Menara utara (WTC 1) · sisi selatan · NIST", 14, GREY, w=3.8).next_to(br_t, DOWN, buff=0.5)
        self.play(Create(line), FadeIn(t1), FadeIn(l1), run_time=0.9)
        self.play(FadeIn(t2), FadeIn(l2), GrowFromCenter(br), FadeIn(br_t), FadeIn(src), run_time=1.2)
        self.hold(50.0)

        # ---------- 8 · PENUTUP (50-55)
        self.clear_stage(keep=[foot])
        big = T("LEMAS", 96, HEAT, True, w=4.0).move_to([0, 1.4, 0])
        self.play(GrowFromCenter(big), run_time=0.8)
        tip = T("Makanya lapisan pelindung api\ndi baja itu penting banget", 24, CHALK, line_spacing=0.95
                ).move_to([0, 0.3, 0])
        self.play(FadeIn(tip), run_time=0.6)
        ask = T("Gedung mana lagi\nyang mau dibedah?", 28, GOLD, True, line_spacing=0.95).move_to([0, -0.7, 0])
        self.play(FadeIn(ask, shift=UP * 0.1), run_time=0.6)
        follow = RoundedRectangle(corner_radius=0.15, width=3.8, height=0.55, color=HEAT, fill_opacity=1,
                                  stroke_width=0).move_to([0, -1.7, 0])
        follow_t = T("Follow buat fakta rumah berikutnya!", 18, BG, True, w=3.6).move_to(follow)
        self.play(FadeIn(follow), FadeIn(follow_t), run_time=0.5)
        self.hold(55.0)
