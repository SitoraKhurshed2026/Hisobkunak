import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle, Line, Ellipse, Rectangle
from kivy.metrics import dp
from kivy.core.window import Window
import math

# ==================== РАНГҲО ====================
BG_COLOR = (0.04, 0.06, 0.12, 1)
DISPLAY_BG = (0.06, 0.1, 0.2, 1)
NUM_BG = (0.1, 0.16, 0.28, 1)
OP_BG = (0.9, 0.5, 0.1, 1)
CLEAR_BG = (0.8, 0.2, 0.2, 1)
EQUAL_BG = (0.2, 0.7, 0.3, 1)
BLUE_FEATURE = (0.1, 0.4, 0.8, 1)
PURPLE_FEATURE = (0.4, 0.2, 0.6, 1)
TEAL_FEATURE = (0.1, 0.6, 0.5, 1)
ORANGE_FEATURE = (0.7, 0.4, 0.1, 1)
POPUP_BG = (0.08, 0.1, 0.2, 1)
ICON_COLOR = (0.9, 0.94, 1, 1)
SCI_BG = (0.15, 0.3, 0.55, 1)
GEO_BG = (0.5, 0.3, 0.1, 1)
TRIG_BG = (0.3, 0.15, 0.5, 1)
LOG_BG = (0.1, 0.5, 0.4, 1)
GEO2_BG = (0.3, 0.5, 0.2, 1)


# ==================== ФУНКСИЯҲОИ МАТЕМАТИКӢ ====================
def _fact(n):
    if n < 0 or n != int(n):
        raise ValueError("Факториал танҳо барои ададҳои бутуни ғайриманфӣ")
    return math.factorial(int(n))

def _cbrt(x):
    if x < 0:
        return -((-x) ** (1/3))
    return x ** (1/3)

MATH_NS = {
    'sqrt': math.sqrt,
    'cbrt': _cbrt,
    'sin': lambda x: math.sin(math.radians(x)),
    'cos': lambda x: math.cos(math.radians(x)),
    'tan': lambda x: math.tan(math.radians(x)),
    'asin': lambda x: math.degrees(math.asin(x)),
    'acos': lambda x: math.degrees(math.acos(x)),
    'atan': lambda x: math.degrees(math.atan(x)),
    'log': math.log10,
    'ln': math.log,
    'exp': math.exp,
    'abs': abs,
    'pi': math.pi,
    'e': math.e,
    'factorial': _fact,
    'pow': pow,
    'round': round,
}


# ==================== СУРАТИ КАЛКУЛЯТОР ====================
class CalculatorIcon(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(pos=self.draw, size=self.draw)

    def draw(self, *args):
        self.canvas.clear()
        cx, cy = self.center_x, self.center_y
        w, h = self.width, self.height
        bw, bh = w * 0.55, h * 0.8
        bx, by = cx - bw / 2, cy - bh / 2
        with self.canvas:
            Color(0.85, 0.92, 1, 1)
            Line(rounded_rectangle=(bx, by, bw, bh, dp(3)), width=dp(1.5))
            Color(0.4, 0.65, 0.95, 1)
            Rectangle(pos=(bx + bw * 0.12, by + bh * 0.7),
                      size=(bw * 0.76, bh * 0.2))
            Color(0.5, 0.7, 0.95, 1)
            btn_w, btn_h = bw * 0.18, bh * 0.12
            for row in range(3):
                for col in range(3):
                    bxx = bx + bw * 0.14 + col * (bw * 0.26)
                    byy = by + bh * 0.48 - row * (bh * 0.16)
                    Line(rounded_rectangle=(bxx, byy, btn_w, btn_h, dp(1)),
                         width=dp(0.8))


# ==================== ТУГМАИ ГРАФИКӢ ====================
class IconButton(Button):
    def __init__(self, icon_type, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (0, 0, 0, 0)
        self.icon_type = icon_type
        self.icon_color = ICON_COLOR
        self.bind(pos=self.draw_icon, size=self.draw_icon, state=self.on_state)

    def draw_icon(self, *args):
        self.canvas.after.clear()
        cx, cy = self.center_x, self.center_y
        w, h = self.width, self.height
        with self.canvas.after:
            Color(*self.icon_color)
            if self.icon_type == 'settings':
                line_w = w * 0.6
                x1, x2 = cx - line_w / 2, cx + line_w / 2
                r = dp(3)
                for i, off in enumerate([0.3, 0.7, 0.4]):
                    y = cy + (1 - i) * h * 0.22
                    Line(points=[x1, y, x2, y], width=dp(1.8), cap='round')
                    dot_x = x1 + line_w * off
                    Ellipse(pos=(dot_x - r, y - r), size=(r * 2, r * 2))
            elif self.icon_type == 'info':
                r = min(w, h) * 0.32
                Line(circle=(cx, cy, r), width=dp(1.8))
                Ellipse(pos=(cx - dp(1.2), cy + r * 0.3), size=(dp(2.4), dp(2.4)))
                Line(points=[cx, cy + r * 0.05, cx, cy - r * 0.45],
                     width=dp(1.8), cap='round')

    def on_state(self, instance, value):
        self.icon_color = (0.5, 0.65, 0.9, 1) if value == 'down' else ICON_COLOR
        self.draw_icon()


# ==================== ТУГМАИ ГИРД ====================
class RoundedButton(Button):
    def __init__(self, bg_color=(0.1, 0.1, 0.1, 1), **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (0, 0, 0, 0)
        self.bg_color = bg_color
        with self.canvas.before:
            Color(*self.bg_color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(12)])
        self.bind(pos=self.update_rect, size=self.update_rect)
        self.bind(state=self.on_state_change)

    def update_rect(self, instance, value):
        if self.state == 'normal':
            self.rect.pos = self.pos
            self.rect.size = self.size

    def on_state_change(self, instance, value):
        self.canvas.before.clear()
        with self.canvas.before:
            if value == 'down':
                r, g, b, a = self.bg_color
                Color(r * 0.6, g * 0.6, b * 0.6, a)
                self.rect = RoundedRectangle(pos=(self.x, self.y - dp(2)),
                                             size=self.size, radius=[dp(12)])
            else:
                Color(*self.bg_color)
                self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(12)])


# ==================== ЭЛЕМЕНТҲОИ КӮМАКӢ ====================
def make_info_label(text):
    lbl = Label(text=text, font_size=dp(13), halign="left", valign="top",
                color=(0.88, 0.92, 1, 1), markup=True,
                size_hint_y=None, padding=(dp(12), dp(10)))
    lbl.bind(width=lambda s, w: s.setter('text_size')(s, (w - dp(20), None)))
    lbl.bind(texture_size=lambda s, ts: s.setter('height')(s, ts[1] + dp(20)))
    return lbl


def make_field(label_text, hint_text="0"):
    box = BoxLayout(orientation='vertical', spacing=dp(3),
                    size_hint_y=None, height=dp(70))
    lbl = Label(text=label_text, font_size=dp(13), bold=True,
                size_hint_y=None, height=dp(20),
                color=(0.75, 0.88, 1, 1), halign="left")
    lbl.bind(size=lbl.setter('text_size'))
    inp = TextInput(hint_text=hint_text, multiline=False,
                    font_size=dp(16), input_filter='float',
                    size_hint_y=None, height=dp(44))
    box.add_widget(lbl)
    box.add_widget(inp)
    return box, inp


def make_result_label(text=""):
    lbl = Label(text=text, font_size=dp(14), halign="center", valign="middle",
                color=(0.85, 1, 0.85, 1), size_hint_y=None)
    lbl.bind(width=lambda s, w: s.setter('text_size')(s, (w - dp(20), None)))
    lbl.bind(texture_size=lambda s, ts: s.setter('height')(s, max(ts[1] + dp(20), dp(80))))
    return lbl


def make_solve_btn(callback, text="Ҳисоб кардан"):
    btn = Button(text=text, size_hint_y=None, height=dp(46),
                 background_normal='', background_color=BLUE_FEATURE,
                 font_size=dp(16), bold=True)
    btn.bind(on_press=callback)
    return btn


def make_close_btn(callback):
    btn = Button(text="Пӯшидан", size_hint_y=None, height=dp(46),
                 background_normal='', background_color=CLEAR_BG,
                 font_size=dp(16), bold=True)
    btn.bind(on_press=callback)
    return btn


def make_scroll():
    scroll = ScrollView(bar_width=dp(4))
    inner = BoxLayout(orientation='vertical', padding=dp(12), spacing=dp(10),
                      size_hint_y=None)
    inner.bind(minimum_height=inner.setter('height'))
    scroll.add_widget(inner)
    return scroll, inner


def make_section_title(text, color):
    """Сарлавҳаи бахш бо матн дар мобайн"""
    lbl = Label(text=text, font_size=dp(13), bold=True,
                size_hint_y=None, height=dp(36),
                color=(0.95, 0.97, 1, 1),
                halign="left", valign="middle",
                padding=(dp(14), 0))
    lbl.bind(size=lambda s, v: setattr(s, 'text_size', (s.width, s.height)))
    with lbl.canvas.before:
        Color(*color)
        lbl.rect = RoundedRectangle(pos=lbl.pos, size=lbl.size, radius=[dp(8)])
    lbl.bind(pos=lambda i, v: setattr(lbl.rect, 'pos', i.pos),
             size=lambda i, v: setattr(lbl.rect, 'size', i.size))
    return lbl


# ==================== РАВЗАНАИ ФУНКСИЯҲОИ МАТЕМАТИКӢ ====================
class SciencePopup(Popup):
    def __init__(self, app_ref, **kwargs):
        super().__init__(**kwargs)
        self.app_ref = app_ref
        self.title = "f(x)  Функсияҳои математикӣ"
        self.title_size = dp(16)
        self.size_hint = (0.97, 0.95)
        self.background_color = POPUP_BG
        self.separator_color = BLUE_FEATURE

        layout = BoxLayout(orientation='vertical')
        scroll, inner = make_scroll()

        inner.add_widget(Label(text="Интихоб кунед, ки чӣ илова кунед:",
                               font_size=dp(15), bold=True,
                               size_hint_y=None, height=dp(30),
                               color=(0.9, 0.95, 1, 1)))

        # 1. РЕША ВА ДАРАҶА
        inner.add_widget(make_section_title("Реша ва дараҷа", SCI_BG))
        row1 = GridLayout(cols=3, spacing=dp(6), size_hint_y=None, height=dp(55))
        for text, insert in [("√x", "sqrt("), ("3√x", "cbrt("), ("x²", "**2"),
                             ("x³", "**3"), ("x^y", "**"), ("1/x", "1/")]:
            btn = RoundedButton(text=text, bg_color=SCI_BG, font_size=dp(15), bold=True)
            btn.bind(on_press=lambda inst, t=insert: self.insert(t))
            row1.add_widget(btn)
        inner.add_widget(row1)

        # 2. ТРИГОНОМЕТРИЯ
        inner.add_widget(make_section_title("Тригонометрия (дараҷа)", TRIG_BG))
        row2 = GridLayout(cols=3, spacing=dp(6), size_hint_y=None, height=dp(55))
        for text, insert in [("sin", "sin("), ("cos", "cos("), ("tan", "tan("),
                             ("asin", "asin("), ("acos", "acos("), ("atan", "atan(")]:
            btn = RoundedButton(text=text, bg_color=TRIG_BG, font_size=dp(13), bold=True)
            btn.bind(on_press=lambda inst, t=insert: self.insert(t))
            row2.add_widget(btn)
        inner.add_widget(row2)

        # 3. ЛОГАРИФМ ВА АДАДҲО
        inner.add_widget(make_section_title("Логарифм ва ададҳои махсус", LOG_BG))
        row3 = GridLayout(cols=3, spacing=dp(6), size_hint_y=None, height=dp(55))
        for text, insert in [("log", "log("), ("ln", "ln("), ("exp", "exp("),
                             ("π", "pi"), ("e", "e"), ("x!", "factorial(")]:
            btn = RoundedButton(text=text, bg_color=LOG_BG, font_size=dp(14), bold=True)
            btn.bind(on_press=lambda inst, t=insert: self.insert(t))
            row3.add_widget(btn)
        inner.add_widget(row3)

        # 4. МОДУЛ ВА ДИГАР
        inner.add_widget(make_section_title("Модул ва дигар", GEO_BG))
        row4 = GridLayout(cols=3, spacing=dp(6), size_hint_y=None, height=dp(55))
        for text, insert in [("|x|", "abs("), ("( )", "("), (") ", ")"),
                             ("%", "/100"), (",", ","), ("mod", "%")]:
            btn = RoundedButton(text=text, bg_color=GEO_BG, font_size=dp(14), bold=True)
            btn.bind(on_press=lambda inst, t=insert: self.insert(t))
            row4.add_widget(btn)
        inner.add_widget(row4)

        # 5. ФОРМУЛАҲОИ ГЕОМЕТРӢ
        inner.add_widget(make_section_title("Формулаҳои геометрӣ", GEO2_BG))
        geo_info = (
            "[b]Масоҳати доира:[/b]  S = pi*r**2\n"
            "[b]Муҳити доира:[/b]  C = 2*pi*r\n"
            "[b]Ҳаҷми кура:[/b]  V = (4/3)*pi*r**3\n"
            "[b]Масоҳати росткунҷа:[/b]  S = a*b\n"
            "[b]Масоҳати секунҷа (Герон):[/b]\n"
            "S = sqrt(p*(p-a)*(p-b)*(p-c))\n"
            "[b]Ҳаҷми параллелепипед:[/b]  V = a*b*c\n"
            "[b]Теоремаи Пифагор:[/b]\n"
            "c = sqrt(a**2 + b**2)"
        )
        inner.add_widget(make_info_label(geo_info))

        # Ҳамаи 6 тугма дар як GridLayout
        geo_row = GridLayout(cols=2, spacing=dp(8),
                             size_hint_y=None, height=dp(180))
        for text, insert in [
            ("S доира", "pi*r**2"),
            ("C доира", "2*pi*r"),
            ("V кура", "(4/3)*pi*r**3"),
            ("S рост.", "a*b"),
            ("Герон", "sqrt(p*(p-a)*(p-b)*(p-c))"),
            ("Пифагор", "sqrt(a**2+b**2)")
        ]:
            btn = RoundedButton(text=text, bg_color=GEO2_BG,
                                font_size=dp(13), bold=True)
            btn.bind(on_press=lambda inst, t=insert: self.insert(t))
            geo_row.add_widget(btn)
        inner.add_widget(geo_row)

        inner.add_widget(make_info_label(
            "[b]Маслиҳат:[/b]\n"
            "• Тригонометрия бо [b]дараҷа[/b] кор мекунад (мисол: sin(30) = 0.5).\n"
            "• Мисол: sqrt(16) = 4, factorial(5) = 120, pi = 3.14159."
        ))

        inner.add_widget(make_close_btn(self.dismiss))

        layout.add_widget(scroll)
        self.content = layout

    def insert(self, text):
        self.app_ref.input_field.text += text

    def dismiss(self, *args):
        super().dismiss()


# ==================== 1. МУОДИЛАИ КВАДРАТӢ ====================
class QuadraticPopup(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "ax2 + bx - c = 0"
        self.title_size = dp(16)
        self.size_hint = (0.97, 0.95)
        self.background_color = POPUP_BG
        self.separator_color = BLUE_FEATURE

        info = (
            "[b]Муодилаи квадратӣ: ax2 + bx - c = 0[/b]\n\n"
            "[b]Қоида:[/b]\n"
            "- Агар a = 0 набошад, муодила квадратӣ аст.\n"
            "- Шакли умумӣ: ax2 + bx - c = 0\n"
            "- Ба шакли стандартӣ меорем: ax2 + bx + (-c) = 0\n"
            "- Дискриминант: D = b2 - 4a(-c) = b2 + 4ac\n\n"
            "[b]Ҳолатҳо:[/b]\n"
            "- D > 0  ->  ду решаи ҳақиқӣ\n"
            "- D = 0  ->  як реша (дукарата)\n"
            "- D < 0  ->  решаҳои ҳақиқӣ надорад\n\n"
            "[b]Формула:[/b] x = (-b +/- sqrt(D)) / (2a)\n\n"
            "[b]Мисол:[/b] x2 - 5x - 6 = 0\n"
            "D = 49, x1 = 6, x2 = -1"
        )

        layout = BoxLayout(orientation='vertical')
        scroll, inner = make_scroll()

        inner.add_widget(Label(text="ax2 + bx - c = 0", font_size=dp(22), bold=True,
                               size_hint_y=None, height=dp(40), color=(0.95, 0.97, 1, 1)))
        inner.add_widget(make_info_label(info))

        grid = GridLayout(cols=2, spacing=dp(10), size_hint_y=None, height=dp(120))
        box_a, self.a_input = make_field("a =", "1")
        box_b, self.b_input = make_field("b =", "-5")
        box_c, self.c_input = make_field("c =", "6")
        for b in [box_a, box_b, box_c]:
            grid.add_widget(b)
        inner.add_widget(grid)

        inner.add_widget(make_solve_btn(self.solve))
        self.result_label = make_result_label("Коэффитсиентҳоро ворид кунед.")
        inner.add_widget(self.result_label)
        inner.add_widget(make_close_btn(self.dismiss))

        layout.add_widget(scroll)
        self.content = layout

    def solve(self, instance):
        try:
            a = float((self.a_input.text.strip() or "0").replace(',', '.'))
            b = float((self.b_input.text.strip() or "0").replace(',', '.'))
            c = float((self.c_input.text.strip() or "0").replace(',', '.'))

            if a == 0:
                if b == 0:
                    self.result_label.text = "Ҳал надорад (a=0, b=0)"
                else:
                    x = c / b
                    self.result_label.text = f"Муодилаи хаттӣ (a=0):\nx = {x:.4f}"
                return

            # ax2 + bx - c = 0 → ax2 + bx + (-c) = 0
            D = b * b - 4 * a * (-c)
            if D > 0:
                sD = math.sqrt(D)
                x1 = (-b + sD) / (2 * a)
                x2 = (-b - sD) / (2 * a)
                self.result_label.text = (f"D = {D:.4f}  (D > 0)\n"
                                          f"Ду решаи ҳақиқӣ:\nx1 = {x1:.4f}\nx2 = {x2:.4f}")
            elif abs(D) < 1e-9:
                x = -b / (2 * a)
                self.result_label.text = f"D = 0\nЯк реша (дукарата):\nx = {x:.4f}"
            else:
                real = -b / (2 * a)
                imag = math.sqrt(-D) / (2 * a)
                self.result_label.text = (f"D = {D:.4f}  (D < 0)\n"
                                          f"Решаҳои ҳақиқӣ надорад.\n"
                                          f"x1 = {real:.3f} + {abs(imag):.3f}i\n"
                                          f"x2 = {real:.3f} - {abs(imag):.3f}i")
        except ValueError:
            self.result_label.text = "[X] Хато: Рақамҳоро дуруст ворид кунед!"


# ==================== 2. СИСТЕМАИ МУОДИЛАҲО ====================
class SystemPopup(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "x,y  Системаи муодилаҳо"
        self.title_size = dp(16)
        self.size_hint = (0.97, 0.95)
        self.background_color = POPUP_BG
        self.separator_color = BLUE_FEATURE

        info = (
            "[b]Системаи муодилаҳои хаттӣ:[/b]\n"
            "a1x + b1y = c1\n"
            "a2x + b2y = c2\n\n"
            "[b]Усули Крамер:[/b]\n"
            "- D  = a1*b2 - a2*b1\n"
            "- Dx = c1*b2 - c2*b1\n"
            "- Dy = a1*c2 - a2*c1\n\n"
            "[b]Ҳолатҳо:[/b]\n"
            "- D != 0  ->  x = Dx/D, y = Dy/D\n"
            "- D = Dx = Dy = 0  ->  бешумор\n"
            "- D = 0, Dx ё Dy != 0  ->  надорад\n\n"
            "[b]Мисол:[/b] 2x + 3y = 12; x - y = 1\n"
            "D = -5, x = 3, y = 2"
        )

        layout = BoxLayout(orientation='vertical')
        scroll, inner = make_scroll()

        inner.add_widget(Label(text="a1x + b1y = c1  /  a2x + b2y = c2",
                               font_size=dp(14), bold=True, size_hint_y=None,
                               height=dp(30), color=(0.95, 0.97, 1, 1)))
        inner.add_widget(make_info_label(info))

        inner.add_widget(Label(text="Муодилаи 1:", font_size=dp(14), bold=True,
                               size_hint_y=None, height=dp(24), color=(0.7, 0.9, 1, 1)))
        grid1 = GridLayout(cols=3, spacing=dp(8), size_hint_y=None, height=dp(80))
        b1a, self.a1 = make_field("a1", "2")
        b1b, self.b1 = make_field("b1", "3")
        b1c, self.c1 = make_field("c1", "12")
        grid1.add_widget(b1a); grid1.add_widget(b1b); grid1.add_widget(b1c)
        inner.add_widget(grid1)

        inner.add_widget(Label(text="Муодилаи 2:", font_size=dp(14), bold=True,
                               size_hint_y=None, height=dp(24), color=(0.7, 0.9, 1, 1)))
        grid2 = GridLayout(cols=3, spacing=dp(8), size_hint_y=None, height=dp(80))
        b2a, self.a2 = make_field("a2", "1")
        b2b, self.b2 = make_field("b2", "-1")
        b2c, self.c2 = make_field("c2", "1")
        grid2.add_widget(b2a); grid2.add_widget(b2b); grid2.add_widget(b2c)
        inner.add_widget(grid2)

        inner.add_widget(make_solve_btn(self.solve))
        self.result_label = make_result_label("Коэффитсиентҳоро ворид кунед.")
        inner.add_widget(self.result_label)
        inner.add_widget(make_close_btn(self.dismiss))

        layout.add_widget(scroll)
        self.content = layout

    def _get(self, field):
        return float((field.text.strip() or "0").replace(',', '.'))

    def solve(self, instance):
        try:
            a1 = self._get(self.a1); b1 = self._get(self.b1); c1 = self._get(self.c1)
            a2 = self._get(self.a2); b2 = self._get(self.b2); c2 = self._get(self.c2)

            D = a1 * b2 - a2 * b1
            Dx = c1 * b2 - c2 * b1
            Dy = a1 * c2 - a2 * c1

            if abs(D) > 1e-9:
                x = Dx / D; y = Dy / D
                self.result_label.text = (f"D = {D:.4f}\n"
                                          f"Dx = {Dx:.4f},  Dy = {Dy:.4f}\n"
                                          f"----------------\n"
                                          f"x = {x:.4f}\ny = {y:.4f}")
            else:
                if abs(Dx) < 1e-9 and abs(Dy) < 1e-9:
                    self.result_label.text = ("D = 0, Dx = 0, Dy = 0\n"
                                              "Система беоҳанг аст -\nҳалҳои бешумор дорад.")
                else:
                    self.result_label.text = ("D = 0, аммо Dx ё Dy != 0\n"
                                              "Система ҳал надорад.")
        except ValueError:
            self.result_label.text = "[X] Хато: Рақамҳоро дуруст ворид кунед!"


# ==================== 3. ЗАРБҲОИ МУХТАСАР ====================
class FormulaPopup(Popup):
    def __init__(self, formula_type, **kwargs):
        super().__init__(**kwargs)
        self.formula_type = formula_type
        self.title_size = dp(16)
        self.size_hint = (0.95, 0.9)
        self.background_color = POPUP_BG
        self.separator_color = BLUE_FEATURE

        if formula_type == 'plus':
            self.title = "(a + b)2  Моҳияти квадратӣ"
            formula_text = "(a + b)2 = a2 + 2ab + b2"
            info = ("[b]Квадрати сумма:[/b]\n\n"
                    "- квадрати якум - a2\n"
                    "- ду баробар зарби ҳарду - 2ab\n"
                    "- квадрати дуюм - b2\n\n"
                    "[b]Мисол:[/b] (3+5)2 = 9+30+25 = 64")
        elif formula_type == 'minus':
            self.title = "(a - b)2  Моҳияти квадратӣ"
            formula_text = "(a - b)2 = a2 - 2ab + b2"
            info = ("[b]Квадрати фарқ:[/b]\n\n"
                    "- квадрати якум - a2\n"
                    "- минус: 2 баробар зарб - (-2ab)\n"
                    "- квадрати дуюм - b2\n\n"
                    "[b]Мисол:[/b] (10-4)2 = 100-80+16 = 36")
        else:
            self.title = "a2 - b2  Фарқи квадратҳо"
            formula_text = "a2 - b2 = (a - b)(a + b)"
            info = ("[b]Фарқи квадратҳо:[/b]\n\n"
                    "- зарби фарқи онҳо (a - b)\n"
                    "- ба суммаи онҳо (a + b)\n\n"
                    "[b]Мисол:[/b] 49-9 = (7-3)(7+3) = 4*10 = 40")

        layout = BoxLayout(orientation='vertical')
        scroll, inner = make_scroll()

        inner.add_widget(Label(text=formula_text, font_size=dp(20), bold=True,
                               size_hint_y=None, height=dp(45),
                               color=(0.95, 0.97, 1, 1)))
        inner.add_widget(make_info_label(info))

        grid = GridLayout(cols=2, spacing=dp(10), size_hint_y=None, height=dp(85))
        box_a, self.a_input = make_field("a =", "3")
        box_b, self.b_input = make_field("b =", "5")
        grid.add_widget(box_a); grid.add_widget(box_b)
        inner.add_widget(grid)

        inner.add_widget(make_solve_btn(self.solve))
        self.result_label = make_result_label("Арзишҳои a ва b-ро ворид кунед.")
        inner.add_widget(self.result_label)
        inner.add_widget(make_close_btn(self.dismiss))

        layout.add_widget(scroll)
        self.content = layout

    def _fmt(self, num):
        if abs(num - round(num)) < 1e-9:
            return str(int(round(num)))
        return f"{num:.4f}"

    def solve(self, instance):
        try:
            a = float((self.a_input.text.strip() or "0").replace(',', '.'))
            b = float((self.b_input.text.strip() or "0").replace(',', '.'))

            if self.formula_type == 'plus':
                a2 = a*a; ab2 = 2*a*b; b2 = b*b; total = (a+b)**2
                self.result_label.text = (f"a2 = {self._fmt(a2)}\n"
                                          f"2ab = {self._fmt(ab2)}\n"
                                          f"b2 = {self._fmt(b2)}\n"
                                          f"----------------\n"
                                          f"(a+b)2 = {self._fmt(total)}")
            elif self.formula_type == 'minus':
                a2 = a*a; ab2 = -2*a*b; b2 = b*b; total = (a-b)**2
                self.result_label.text = (f"a2 = {self._fmt(a2)}\n"
                                          f"-2ab = {self._fmt(ab2)}\n"
                                          f"b2 = {self._fmt(b2)}\n"
                                          f"----------------\n"
                                          f"(a-b)2 = {self._fmt(total)}")
            else:
                a2 = a*a; b2 = b*b; total = a2 - b2
                self.result_label.text = (f"a2 = {self._fmt(a2)}\n"
                                          f"b2 = {self._fmt(b2)}\n"
                                          f"(a-b) = {self._fmt(a-b)}\n"
                                          f"(a+b) = {self._fmt(a+b)}\n"
                                          f"----------------\n"
                                          f"a2-b2 = {self._fmt(total)}")
        except ValueError:
            self.result_label.text = "[X] Хато: Рақамҳоро дуруст ворид кунед!"


# ==================== 4. ТАНЗИМОТ ====================
class SettingsPopup(Popup):
    def __init__(self, app_ref, **kwargs):
        super().__init__(**kwargs)
        self.app_ref = app_ref
        self.title = "Танзимот"
        self.title_size = dp(16)
        self.size_hint = (0.95, 0.8)
        self.background_color = POPUP_BG
        self.separator_color = BLUE_FEATURE

        layout = BoxLayout(orientation='vertical')
        scroll, inner = make_scroll()

        inner.add_widget(Label(text="Танзимоти барнома", font_size=dp(20), bold=True,
                               size_hint_y=None, height=dp(40), color=(0.95, 0.97, 1, 1)))
        inner.add_widget(make_info_label(
            "[b]Дақиқии рақамҳо[/b]\nИнтихоб кунед, ки натиҷа бо чанд рақами даҳӣ нишон дода шавад:"
        ))

        precision_row = GridLayout(cols=3, spacing=dp(8), size_hint_y=None, height=dp(50))
        btn_p2 = RoundedButton(text="2 рақам", bg_color=TEAL_FEATURE, font_size=dp(13))
        btn_p4 = RoundedButton(text="4 рақам", bg_color=BLUE_FEATURE, font_size=dp(13))
        btn_p6 = RoundedButton(text="6 рақам", bg_color=PURPLE_FEATURE, font_size=dp(13))
        btn_p2.bind(on_press=lambda x: self.set_precision(2))
        btn_p4.bind(on_press=lambda x: self.set_precision(4))
        btn_p6.bind(on_press=lambda x: self.set_precision(6))
        precision_row.add_widget(btn_p2)
        precision_row.add_widget(btn_p4)
        precision_row.add_widget(btn_p6)
        inner.add_widget(precision_row)

        self.status_label = Label(
            text=f"Ҳолати ҷорӣ: {self.app_ref.decimal_places} рақами даҳӣ",
            font_size=dp(13), color=(0.85, 1, 0.85, 1),
            size_hint_y=None, height=dp(30)
        )
        inner.add_widget(self.status_label)

        inner.add_widget(make_info_label(
            "[b]Тоза кардани ҳамаи маълумот[/b]"
        ))
        btn_clear = RoundedButton(text="Ҳамаро тоза кардан",
                                  bg_color=CLEAR_BG, font_size=dp(14), bold=True)
        btn_clear.bind(on_press=self.clear_all)
        inner.add_widget(btn_clear)

        inner.add_widget(make_info_label(
            "[b]Нусхаи барнома:[/b] 1.4\n"
            "[b]Забон:[/b] Python + Kivy\n"
            "[b]Функсияҳо:[/b] 20+\n"
            "[b]Тамос:[/b] 110804hh@gmail.com"
        ))
        inner.add_widget(make_close_btn(self.dismiss))

        layout.add_widget(scroll)
        self.content = layout

    def set_precision(self, n):
        self.app_ref.decimal_places = n
        self.status_label.text = f"Ҳолати ҷорӣ: {n} рақами даҳӣ"

    def clear_all(self):
        self.app_ref.input_field.text = ''
        self.app_ref.result_value.text = '0'
        self.app_ref.result_label.text = 'Натиҷа:'
        self.status_label.text = "Ҳамаи маълумот тоза шуд!"


# ==================== 5. МАЪЛУМОТ ====================
class InfoPopup(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Маълумот"
        self.title_size = dp(16)
        self.size_hint = (0.95, 0.9)
        self.background_color = POPUP_BG
        self.separator_color = BLUE_FEATURE

        layout = BoxLayout(orientation='vertical')
        scroll, inner = make_scroll()

        inner.add_widget(Label(text="Ҳисобкунаки оддӣ", font_size=dp(24), bold=True,
                               size_hint_y=None, height=dp(45), color=(0.95, 0.97, 1, 1)))
        inner.add_widget(Label(text="Нусхаи 1.4", font_size=dp(14),
                               size_hint_y=None, height=dp(25), color=(0.7, 0.85, 1, 1)))

        inner.add_widget(make_info_label(
            "[b]Ҳадафи барнома:[/b]\n\n"
            "Ин барнома барои [b]осон кардани ҳалли мисолу масъалаҳо[/b] "
            "пешбинӣ шудааст.\n\n"
            "- Муодилаи квадратӣ ax2 + bx - c = 0\n"
            "- Системаи муодилаҳо\n"
            "- Зарбҳои мухтасар\n"
            "- Функсияҳои математикӣ\n"
            "- Формулаҳои геометрӣ\n"
            "- Ҳисобкунаки оддӣ"
        ))
        inner.add_widget(make_info_label(
            "[b]Функсияҳои математикӣ:[/b]\n\n"
            "√, 3√, x², x³, x^y, 1/x\n"
            "sin, cos, tan, asin, acos, atan\n"
            "log, ln, exp, pi, e, factorial\n"
            "abs (модул), %, mod"
        ))
        inner.add_widget(make_info_label(
            "[b]Формулаҳои геометрӣ:[/b]\n\n"
            "- Масоҳати доира ва муҳит\n"
            "- Ҳаҷми кура\n"
            "- Масоҳати росткунҷа\n"
            "- Формулаи Герон\n"
            "- Теоремаи Пифагор"
        ))
        inner.add_widget(make_info_label(
            "[b]Тартибдиҳанда:[/b]\n\n"
            "Холов Хуршед\n"
            "Омӯзгори МТМУ №34, ноҳияи Данғара\n\n"
            "[b]Тамос:[/b]\n"
            "110804hh@gmail.com"
        ))
        inner.add_widget(make_info_label(
            "[b]Бунёд, ки ҳар як ҳисоб - қадами ба сӯи дониш аст![/b]"
        ))
        inner.add_widget(make_close_btn(self.dismiss))

        layout.add_widget(scroll)
        self.content = layout


# ==================== БАРНОМАИ АСОСӢ ====================
class CalculatorApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.decimal_places = 4

    def build(self):
        Window.clearcolor = BG_COLOR
        root = BoxLayout(orientation='vertical', padding=dp(8), spacing=dp(6))

        # 1. САРЛАВҲА
        header = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(8))
        calc_icon = CalculatorIcon(size_hint_x=None, width=dp(42))
        title = Label(text="Ҳисобкунаки оддӣ", font_size=dp(21), bold=True,
                      halign="left", valign="middle")
        title.bind(size=title.setter('text_size'))
        btn_settings = IconButton('settings', size_hint_x=None, width=dp(42))
        btn_info = IconButton('info', size_hint_x=None, width=dp(42))
        btn_settings.bind(on_press=self.open_settings)
        btn_info.bind(on_press=self.open_info)
        header.add_widget(calc_icon)
        header.add_widget(title)
        header.add_widget(btn_settings)
        header.add_widget(btn_info)
        root.add_widget(header)

        # 2. ТАБЛОИ НАТИҶА
        display = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(95), padding=dp(8))
        with display.canvas.before:
            Color(*DISPLAY_BG)
            self.display_rect = RoundedRectangle(pos=display.pos, size=display.size, radius=[dp(15)])
            Color(0.2, 0.4, 0.8, 1)
            self.display_line = Line(rounded_rectangle=(display.x, display.y,
                                    display.width, display.height, dp(15)), width=1.5)
        display.bind(pos=self.update_display, size=self.update_display)

        self.result_label = Label(text="Натиҷа:", font_size=dp(13), halign="right",
                                  valign="top", color=(0.6, 0.7, 0.8, 1))
        self.result_label.bind(size=self.result_label.setter('text_size'))
        self.result_value = Label(text="0", font_size=dp(40), bold=True,
                                  halign="center", valign="middle")
        self.result_value.bind(size=self.result_value.setter('text_size'))
        display.add_widget(self.result_label)
        display.add_widget(self.result_value)
        root.add_widget(display)

        # 3. ТУГМАҲОИ МАХСУС
        row1 = BoxLayout(size_hint_y=None, height=dp(52), spacing=dp(6))
        btn_sq = RoundedButton(text="ax2+bx-c=0", bg_color=BLUE_FEATURE,
                               font_size=dp(11), bold=True)
        btn_sys = RoundedButton(text="x,y Система", bg_color=NUM_BG, font_size=dp(12))
        btn_sci = RoundedButton(text="f(x) Иловагӣ", bg_color=PURPLE_FEATURE,
                                font_size=dp(12), bold=True)
        btn_sq.bind(on_press=self.open_quadratic)
        btn_sys.bind(on_press=self.open_system)
        btn_sci.bind(on_press=self.open_science)
        row1.add_widget(btn_sq)
        row1.add_widget(btn_sys)
        row1.add_widget(btn_sci)
        root.add_widget(row1)

        # 4. ЗАРБҲОИ МУХТАСАР
        row2 = GridLayout(cols=3, size_hint_y=None, height=dp(64), spacing=dp(8))
        btn_a_b = RoundedButton(text="(a+b)2", bg_color=TEAL_FEATURE, font_size=dp(13), bold=True)
        btn_a_b2 = RoundedButton(text="(a-b)2", bg_color=PURPLE_FEATURE, font_size=dp(13), bold=True)
        btn_a2_b2 = RoundedButton(text="a2-b2", bg_color=ORANGE_FEATURE, font_size=dp(13), bold=True)
        btn_a_b.bind(on_press=self.open_plus_formula)
        btn_a_b2.bind(on_press=self.open_minus_formula)
        btn_a2_b2.bind(on_press=self.open_diff_formula)
        row2.add_widget(btn_a_b)
        row2.add_widget(btn_a_b2)
        row2.add_widget(btn_a2_b2)
        root.add_widget(row2)

        # 5. ВОРИДИ АРЗИШҲО
        input_layout = BoxLayout(size_hint_y=None, height=dp(48), spacing=dp(8))
        self.input_field = TextInput(
            hint_text="Арзишҳоро ворид кунед...",
            multiline=False, font_size=dp(15),
            background_color=(0.08, 0.12, 0.22, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(1, 1, 1, 1),
            padding=[dp(10), dp(10), dp(10), dp(10)]
        )
        btn_calc = RoundedButton(text="Ҳисоб", bg_color=BLUE_FEATURE, font_size=dp(15),
                                 bold=True, size_hint_x=None, width=dp(85))
        btn_calc.bind(on_press=self.calculate_result)
        input_layout.add_widget(self.input_field)
        input_layout.add_widget(btn_calc)
        root.add_widget(input_layout)

        # 6. КЛАВИАТУРА
        keypad = GridLayout(cols=4, spacing=dp(5), size_hint_y=1)
        buttons = [
            ('7', NUM_BG), ('8', NUM_BG), ('9', NUM_BG), ('/', OP_BG),
            ('4', NUM_BG), ('5', NUM_BG), ('6', NUM_BG), ('*', OP_BG),
            ('1', NUM_BG), ('2', NUM_BG), ('3', NUM_BG), ('-', OP_BG),
            ('C', CLEAR_BG), ('0', NUM_BG), ('.', NUM_BG), (',', NUM_BG)
        ]
        for text, color in buttons:
            btn = RoundedButton(text=text, bg_color=color, font_size=dp(22), bold=True)
            btn.bind(on_press=self.on_keypad_press)
            keypad.add_widget(btn)
        root.add_widget(keypad)

        # 7. = ва +
        bottom_row = BoxLayout(size_hint_y=None, height=dp(52), spacing=dp(6))
        btn_equal = RoundedButton(text="=", bg_color=EQUAL_BG, font_size=dp(26), bold=True)
        btn_plus = RoundedButton(text="+", bg_color=OP_BG, font_size=dp(26), bold=True)
        btn_equal.bind(on_press=self.on_keypad_press)
        btn_plus.bind(on_press=self.on_keypad_press)
        bottom_row.add_widget(btn_equal); bottom_row.add_widget(btn_plus)
        root.add_widget(bottom_row)

        # 8. ПОВОН
        footer = BoxLayout(size_hint_y=None, height=dp(26))
        footer_label = Label(text="Бунёд, ки ҳар як ҳисоб - қадами ба сӯи дониш аст!",
                             font_size=dp(11), color=(0.5, 0.6, 0.7, 1), halign="center")
        footer_label.bind(size=footer_label.setter('text_size'))
        footer.add_widget(footer_label)
        root.add_widget(footer)

        return root

    def update_display(self, instance, value):
        self.display_rect.pos = instance.pos
        self.display_rect.size = instance.size
        self.display_line.rounded_rectangle = (instance.x, instance.y, instance.width, instance.height, dp(15))

    def open_quadratic(self, instance): QuadraticPopup().open()
    def open_system(self, instance): SystemPopup().open()
    def open_plus_formula(self, instance): FormulaPopup('plus').open()
    def open_minus_formula(self, instance): FormulaPopup('minus').open()
    def open_diff_formula(self, instance): FormulaPopup('diff').open()
    def open_settings(self, instance): SettingsPopup(self).open()
    def open_info(self, instance): InfoPopup().open()
    def open_science(self, instance): SciencePopup(self).open()

    def on_keypad_press(self, instance):
        text = instance.text
        if text == 'C':
            self.input_field.text = ''
            self.result_value.text = '0'
            self.result_label.text = 'Натиҷа:'
        elif text == '=':
            self.calculate_result(None)
        else:
            self.input_field.text += text

    def calculate_result(self, instance):
        expression = self.input_field.text
        if not expression:
            return
        try:
            expression = expression.replace(',', '.')
            result = eval(expression, {"__builtins__": {}}, MATH_NS)
            if isinstance(result, float):
                if result.is_integer():
                    result = int(result)
                else:
                    result = round(result, self.decimal_places)
            self.result_value.text = str(result)
            self.input_field.text = str(result)
            self.result_label.text = 'Натиҷа:'
        except ZeroDivisionError:
            self.result_value.text = "Хато: Ба сифр тақсим кардан мумкин нест"
        except Exception as e:
            self.result_value.text = "Хато дар ифода"
            print(f"Error: {e}")


if __name__ == '__main__':
    CalculatorApp().run()