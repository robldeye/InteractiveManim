from manim import *
from sympy import symbols, sin, Interval, S, latex
from sympy.calculus.util import maximum
import math

class Integral(Scene):
    # allows Integral to be called with a specified parameters f(x) and b
    def __init__(self, f, f_expr, b, **kwargs):
        self.f = f
        self.b = b
        self.f_expr = f_expr
        super().__init__(**kwargs)

    def construct(self):
        # Bound y-values
        x = symbols("x")
        # Axes
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[-5, 5, 1],
            x_length=8,
            y_length=8,
            axis_config={"include_numbers": True},
        ).to_edge(RIGHT)
        
        f_graph = axes.plot(
            self.f, 
            x_range=[*axes.x_range[:2], 0.01],
            color=DARK_BLUE, 
            stroke_width=2, 
            use_smoothing=True
        )

        # ValueTrackers
        b_value = ValueTracker(0.5)
        dx_value = ValueTracker(0.5)

        # Mobjects
        f_riemann = always_redraw(
            lambda: axes.get_riemann_rectangles(
                f_graph,
                x_range=[0, b_value.get_value()],
                dx=dx_value.get_value(),
                input_sample_type="center",
                stroke_width=5*dx_value.get_value(),
                fill_opacity=0.5,
                show_signed_area=True, # False for |f(x)| integrand
                color=GREEN
            )
        )

        # Labels
        title = MathTex(rf"\text{{Visualizing}} \, \int_0^{{{self.b:.1f}}} {latex(self.f_expr)} \, dx")
        self.play(
            Write(title)
        )
        self.play(
            title.animate.to_edge(LEFT),
        )
        self.wait()

        self.add(axes, f_graph, f_riemann)
        self.wait()

        # dx_prefix = MathTex(r"dx =")
        # dx_decimal = DecimalNumber(
        #     dx_value.get_value(),
        #     num_decimal_places=2,
        # ).next_to(dx_prefix, RIGHT)
        # dx_decimal.add_updater(lambda m: m.set_value(dx_value.get_value()))
        # dx_label = VGroup(dx_prefix, dx_decimal).arrange(RIGHT)
        # dx_label.next_to(title, DOWN).align_to(title, LEFT)

        self.play(
            b_value.animate.set_value(self.b),
            run_time = 3
        )
        self.wait(2)

        self.play(
            dx_value.animate.set_value(0.01),
            run_time = 4
        )

        # self.play(
        #     FadeOut(f_riemann)
        # )

        # f_area = axes.get_area(
        #     f_graph,
        #     x_range=[0, a_value.get_value()],
        #     color=BLUE,
        #     opacity=0.5
        # )

        # self.play(
        #     FadeIn(f_area)
        # )
        self.wait(3)


