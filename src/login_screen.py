from imports import *

class LoginScreen(MDScreen):
    def on_enter(self):
        self.app = MDApp.get_running_app()
        
    def login_button(self):
        login_value = self.ids.login_field.text
        password_value = self.ids.password_field.text

        result = self.app.login(login_value, password_value)
        
        if result == 1:
            with open(self.app.config, 'r+', encoding='utf-8') as file:
                config = json.load(file)
                config.update({'login': login_value, 'password': password_value})
                file.seek(0)
                json.dump(config, file, ensure_ascii=False, indent=4)
                file.truncate()

            self.app.change_screen('faculty_screen')
        elif result == -1:
            self.dialog = self.app.get_dialog('message', 'Ошибка соединения!')
            self.dialog.open()
        else:
            self.dialog = self.app.get_dialog('message', 'Неверный логин или пароль!')
            self.dialog.open()