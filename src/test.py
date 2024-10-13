from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.app import MDApp

KV = '''
MDScreen:

    MDBoxLayout:
        orientation: 'horizontal'
        size_hint: 1, 0.5
        pos_hint: {'top': 1}
        md_bg_color: "white"
            
        MDFloatingActionButtonSpeedDial:
            pos: root.pos
            data: app.data
            root_button_anim: True
'''


class Example(MDApp):
    data = {
        '': 'language-python',
        ' ': 'language-php',
    }

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        return Builder.load_string(KV)


Example().run()