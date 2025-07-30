from manim import *
from sympy import symbols, sin, Interval, S
from sympy.calculus.util import maximum
import math

class Integral(Scene):
    # allows Integral to be called with a specified parameters f(x) and b
    def __init__(self, f, b_max, b, **kwargs):
        self.f = f
        self.b_max = b_max
        self.b = b
        super().__init__(**kwargs)

    def construct(self):
        # Bound y-values
        x = symbols("x")
        x_bound = math.ceil(self.b_max)+1
        y_bound = 10   
        # Axes
        axes = Axes(
            x_range=[0, x_bound, 1],
            y_range=[-5, 5, 1],
            x_length=x_bound,
            y_length=y_bound,
            axis_config={"include_numbers": True},
        ).to_edge(RIGHT)
        
        f_graph = axes.plot(
            self.f, 
            x_range=[*axes.x_range[:2], 0.05],
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
                x_range=[0, b_value.get_value()-dx_value.get_value()], # so you don't get an extra rectangle
                dx=dx_value.get_value(),
                input_sample_type="center",
                stroke_width=5*dx_value.get_value(),
                fill_opacity=0.5,
                show_signed_area=True, # False for |f(x)| integrand
                color=GREEN
            )
        )

        # Labels
        title = MathTex(r"\text{Visualizing} \, \int_0^a f(x) dx")
        b_lbl = MathTex("b =")
        b_value_lbl = DecimalNumber().add_updater(
            lambda n: n.set_value(b_value.get_value())
        )
        b_lbl_grp = VGroup(b_lbl, b_value_lbl).arrange(RIGHT).add_updater(
            lambda g: g.next_to(axes.c2p(b_value.get_value(), 0), DOWN, buff=1)
        )

        #self.play(
            #Write(title)
        #)

        self.add(axes, b_lbl_grp, f_graph, f_riemann)
        self.wait(2)

        self.play(
            b_value.animate.set_value(2*np.pi),
            run_time = 2
        )
        self.wait()

        self.play(
            dx_value.animate.set_value(0.1),
            run_time = 2
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


