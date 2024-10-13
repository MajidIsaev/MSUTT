from imports import *

class ThemeScreen(MDScreen):
    def on_enter(self):        
        self.app = MDApp.get_running_app()
    
    def select_theme(self, palette = 'Blue', style = 'Dark'):
        self.app.theme_cls.theme_style = style
        self.app.theme_cls.primary_palette = palette
        
        with open(self.app.config, 'r', encoding='utf-8') as file:
                config = json.load(file)
                config['style'] = style
                config['palette'] = palette
                
        with open(self.app.config, 'w', encoding='utf-8') as file:
                json.dump(config, file, ensure_ascii=False, indent=4)
                
        self.app.change_screen('menu_screen')