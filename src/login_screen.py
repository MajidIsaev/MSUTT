from imports import *


class LoginScreen(MDScreen):
    def on_enter(self):
        self.app = MDApp.get_running_app()
        self.login_value = ""
        self.password_value = ""

    def login_button(self):
        self.login_value = self.ids.login_field.text
        self.password_value = self.ids.password_field.text

        self.app.loading_dialog.open()
        self.button_is_pressed = True
        Clock.schedule_once(lambda dt: self.login(), 0)

    def login(self):
        result = self.app.login(self.login_value, self.password_value)

        if result == 1:
            with open(self.app.config, "r+", encoding="utf-8") as file:
                config = json.load(file)
                config.update(
                    {"login": self.login_value, "password": self.password_value}
                )
                file.seek(0)
                json.dump(config, file, ensure_ascii=False, indent=4)
                file.truncate()
            self.app.change_screen("faculty_screen")
        elif result == -1:
            self.dialog = self.app.get_dialog("message", "Ошибка соединения!")
            self.dialog.open()
        else:
            self.dialog = self.app.get_dialog("message", "Неверный логин или пароль!")
            self.dialog.open()
            
        self.app.loading_dialog.dismiss()
