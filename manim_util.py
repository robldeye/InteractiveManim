from manim import *
from sympy import sin

class Integral(Scene):
    # allows Integral to be called with a specified parameters f(x) and a
    # def __init__(self, func, a, **kwargs):
    #     self.func = func
    #     self.a = a
    #     super().__init__(**kwargs)

    def construct(self):
        def f(x):
            return sin(x)
    
        self.a = 5
        # Axes
        axes = Axes(
            x_range=[0, 8, 1],
            y_range=[-2, 2, 1],
            x_length=10,
            y_length=5,
            axis_config={"include_numbers": True},
        ).to_edge(RIGHT)
        
        f_graph = axes.plot(
            f, 
            x_range=[*axes.x_range[:2], 0.05],
            color=DARK_BLUE, 
            stroke_width=2, 
            use_smoothing=True
        )

        # ValueTrackers
        a_value = ValueTracker(0.5)
        dx_value = ValueTracker(0.5)

        # Mobjects
        f_riemann = always_redraw(
            lambda: axes.get_riemann_rectangles(
                f_graph,
                x_range=[0, a_value.get_value()-dx_value.get_value()], # so you don't get an extra rectangle
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
        a_lbl = always_redraw(
            lambda: MathTex(r"a").next_to(axes.c2p(a_value.get_value(), 0), DOWN, buff=1)
        )

        #self.play(
            #Write(title)
        #)

        self.add(axes, f_graph, f_riemann)
        self.wait(2)

        self.play(
            a_value.animate.set_value(2*np.pi),
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


