from manim import *
from sympy import symbols, latex, limit, S
import math

class Integral(Scene):
    # allows Integral to be called with a specified parameters f(x) and b
    def __init__(self, f, f_expr, b, **kwargs):
        self.f = f
        self.b = b
        self.f_expr = f_expr # needed for nice latex expressions
        super().__init__(**kwargs)

    def construct(self):
        x = symbols("x")
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[-5, 5, 1],
            x_length=8,
            y_length=8,
            axis_config={"include_numbers": False},
        ).to_edge(RIGHT)
        axes_labels = axes.get_axis_labels()
        
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
        
        # Animations
        self.play(
            Write(title, run_time=1)
        )
        self.play(
            title.animate.to_edge(LEFT),
        )
        self.wait()

        self.play(
            FadeIn(axes),
            FadeIn(f_graph),
            FadeIn(f_riemann)
        )
        self.wait()

        self.play(
            b_value.animate.set_value(self.b),
            run_time = 2
        )
        self.wait(2)

        self.play(
            dx_value.animate.set_value(0.01),
            run_time = 2
        )
        self.wait(3)
        # End Integral

class Limit(Scene):
    # allows Limit to be called with a specified parameters f(x) and b
    def __init__(self, f, f_expr, a, f_tex, **kwargs):
        self.f = f
        self.a = a
        self.f_expr = f_expr # usually expressed latex correctly
        self.f_tex = f_tex # rarely needed for nice latex expressions (think piecewise functions)
        super().__init__(**kwargs)

    def construct(self):
        x = symbols("x")
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            x_length=8,
            y_length=8,
            axis_config={"include_numbers": False},
        ).to_edge(RIGHT)
        axes_labels = axes.get_axis_labels()
        
        graph = axes.plot(
            self.f, 
            x_range=[*axes.x_range[:2], 0.01],
            color=BLUE, 
            use_smoothing=True
        )

        # Dots
        limit_dot = Dot(axes.input_to_graph_point(self.a, graph))

        left_dot = Dot().move_to(axes.c2p(self.a-1, self.f(self.a-1)))
        right_dot = Dot().move_to(axes.c2p(self.a+1, self.f(self.a+1)))
        leftx_dot = Dot().move_to(axes.c2p(self.a-1, 0)).set_opacity(0) # hacky way to draw lines later
        rightx_dot = Dot().move_to(axes.c2p(self.a+1, 0)).set_opacity(0)

        left_tracker = ValueTracker(1)
        right_tracker = ValueTracker(1)

        left_dot.add_updater(lambda d: d.move_to(axes.c2p(self.a - left_tracker.get_value(), self.f(self.a - left_tracker.get_value()))))
        right_dot.add_updater(lambda d: d.move_to(axes.c2p(self.a + right_tracker.get_value(), self.f(self.a + right_tracker.get_value()))))
        leftx_dot.add_updater(lambda d: d.move_to(axes.c2p(self.a - left_tracker.get_value(), 0)))
        rightx_dot.add_updater(lambda d: d.move_to(axes.c2p(self.a + right_tracker.get_value(), 0)))

        title = MathTex(rf"\text{{Calculating }} \lim_{{x \to {self.a}}} f(x)").scale(0.8)

        # Lines
        left_line = always_redraw(
            lambda: Arrow(
            start=axes.c2p(self.a - left_tracker.get_value(), 0),
            end=axes.c2p(self.a - left_tracker.get_value(), self.f(self.a - left_tracker.get_value())),
            max_tip_length_to_length_ratio=0.35
            )
        )

        right_line = always_redraw(
            lambda: Arrow(
            start=axes.c2p(self.a + right_tracker.get_value(), 0),
            end=axes.c2p(self.a + right_tracker.get_value(), self.f(self.a + right_tracker.get_value())),
            max_tip_length_to_length_ratio=0.35
            )
        )

        limit_dash = DashedLine(
            start = axes.c2p(0, self.f(self.a)),
            end = axes.c2p(self.a, self.f(self.a))
        )

        # Start
        self.play(
            Write(title, run_time=1)
        )
        self.wait()

        self.play(
            title.animate.to_corner(UL)
        )
        self.wait()
        
        func_label = MathTex(f"f(x) = {self.f_tex}").scale(0.8).next_to(title, DOWN).align_to(title, LEFT)
        self.play(
            Write(func_label, run_time=1)
        )
        self.wait()

        limit_l = MathTex(
            rf"\text{{L}}) \quad \lim_{{x \to {self.a}^{{-}}}} f(x) = {latex(limit(self.f_expr, x, self.a, dir='-'))}"
            ).scale(0.8)
        limit_r = MathTex(
            rf"\text{{R}}) \quad \lim_{{x \to {self.a}^{{+}}}} f(x) = {latex(limit(self.f_expr, x, self.a, dir='+'))}"
            ).scale(0.8)
        sided_limits = VGroup(limit_l, limit_r).arrange(DOWN).next_to(func_label, DOWN).align_to(title, LEFT)
        
        limit_def1 = MathTex(
            rf"""
                \begin{{array}}{{l}}
                \text{{Since}} \\
                \quad \displaystyle \lim_{{x \to {self.a}^{{-}}}} f(x) = \lim_{{x \to {self.a}^{{+}}}} f(x)... \\
                \end{{array}}
            """
            )
        limit_def2 = MathTex(
            rf"""    
                \begin{{array}}{{l}}
                \text{{We have}} \\
                \quad \displaystyle \lim_{{x \to {self.a}}} \,\, f(x) = {latex(self.f(self.a))}
                \end{{array}}
            """
            )
        limit_def = VGroup(
            limit_def1, 
            limit_def2
            ).scale(0.8).arrange(DOWN).next_to(sided_limits, 2*DOWN).align_to(sided_limits, LEFT)

        self.play(
            FadeIn(axes, axes_labels),
            *(Create(obj) for obj in [graph, leftx_dot, rightx_dot]),
            lag_ratio=0.5,
        )
        self.wait()

        self.play(
            FadeIn(left_line, right_line),
            FadeIn(left_dot, right_dot)
        )
        self.play(
            Indicate(left_dot),
            Indicate(right_dot),
            lag_ratio=0.5
        )
        self.wait()

        self.play(
            FocusOn(left_dot)
        )
        self.play(
            left_tracker.animate.set_value(0),
            run_time=2
        )
        self.play(FadeOut(left_line))
        self.play(
            Indicate(left_dot),
            Write(limit_l, run_time=1),
            lag_ratio=0.5
        )
        self.wait()

        self.play(
            FocusOn(right_dot)
        )
        self.play(
            right_tracker.animate.set_value(0),
            run_time=2
        )
        self.play(FadeOut(right_line))
        self.play(
            Indicate(right_dot),
            Write(limit_r, run_time=1),
            lag_ratio=0.5
        )
        self.wait()


        # Identify limit check
        if limit(self.f_expr, x, self.a, dir='-') == limit(self.f_expr, x, self.a, dir='+'):
            self.play(
                Circumscribe(limit_dot, color=YELLOW),
                Create(limit_dash),
                *(Write(label, run_time=1) for label in limit_def),
                lag_ratio = 0.5
            )
        else:
            lim_fail = MathTex(
                rf"\lim_{{x \to {self.a}^{{-}}}} {latex(self.f_expr)} \neq \lim_{{x \to {self.a}^{{-}}}} {latex(self.f_expr)}"
            )
        self.wait(3)