from imports import *

class TimeTable(MDApp):
    def build(self):
        self.work = Session()
        self.config = 'config.json'
        
        with open(self.config, 'r', encoding='utf-8') as file:
                config = json.load(file)
                self.login_value = config['login']
                self.password_value = config['password']
                self.faculty_name = config['faculty_name']
                self.faculty_iD = config['faculty_iD']
                self.course = config['course']
                self.first_launch = config['first_launch']
                self.auto_connect = config['auto_connect']
                self.theme_cls.theme_style = config['style']
                self.theme_cls.primary_palette = config['palette']
                
        self.screen = Builder.load_file('gui.kv')    
        return self.screen

    def on_start(self):        
        if not self.auto_connect: return
            
        elif self.login(self.login_value, self.password_value) == 1:
            self.change_screen('faculty_screen')

    def login(self, username, password):
        data = {'username': username, 'password': password, 'submit': 'Войти'}

        try:
            self.work.get('http://timetable.msu.az/', headers=HEADERS)
            result = self.work.post('http://timetable.msu.az/index.php', headers=HEADERS, data=data, allow_redirects=True)
        except:
            return -1
            
        soup = BeautifulSoup(result.text, PARSER)

        check = soup.find('div', class_='loginDiv')

        if check == None:
            self.auto_connect = True
            
            with open(self.config, 'r', encoding='utf-8') as file:
                config = json.load(file)
                config['first_launch'] = False
                config['auto_connect'] = self.auto_connect
                
            with open(self.config, 'w', encoding='utf-8') as file:
                json.dump(config, file, ensure_ascii=False, indent=4)
            return 1
            
        else:
            return 0

    
    def change_screen(self, screen_name):
        self.root.current = screen_name

    def get_dialog(self, dialog_type, message = ''):
        app = MDApp.get_running_app()
        
        if dialog_type == 'message':
            self.dialog = MDDialog(
                text = message,
                buttons = [
                    MDFlatButton(
                        text = 'ЗАКРЫТЬ',
                        theme_text_color = 'Custom',
                        text_color = app.theme_cls.primary_color,
                        on_release = self.dialog_close
                    ),
                ],
            )

            return self.dialog
        
        elif dialog_type == 'info':
            self.dialog = MDDialog( #Требутся заменить!
                text = message
            )
            return self.dialog

    def dialog_close(self, instance):
        self.dialog.dismiss()