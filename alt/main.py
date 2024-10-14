from kivymd.app import MDApp

from kivymd.uix.screen import MDScreen
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import OneLineListItem
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog

from kivy.metrics import dp
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.properties import StringProperty
from kivy.uix.behaviors import ButtonBehavior

from kivymd.uix.behaviors import (
    RectangularRippleBehavior,
    BackgroundColorBehavior,
    CommonElevationBehavior
)

from bs4 import BeautifulSoup
from requests import Session
from datetime import datetime, timedelta
import json

HEADERS = {'User-Agent': 'CroockedHands/2.0 (EVM x8), CurlyFingers20/1;p'}

PARSER = 'html' #'lxml'

WEEK = ['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ', 'ВС']

MESSAGE = '''Примечание к выпуску:

Приложение находится в альфа-версии и может содержать множество ошибок. Пожалуйста, примите это к сведению!

1. При нажатии на предмет отображаются имя преподавателя и примечание к предмету.
   
2. При повторном нажатии содержимое возвращается к исходному виду.
   
3. Предметы с зачетами выделены особым цветом.

4. При входе в приложение оно уведомит о наличии зачетов на текущей неделе.

5. В профиле можно изменить специальность.'''

class Day:
    def __init__(self, date, lessons):
        self.date = date
        self.lessons = lessons

class Lesson:
    def __init__(self, number, time, audience, subject, teacher, note):
        self.number = number
        self.time = time
        self.audience = audience
        self.subject = subject
        self.teacher = teacher
        self.note = note

class LessonButton(
    RectangularRippleBehavior,
    BackgroundColorBehavior,
    CommonElevationBehavior,
    ButtonBehavior
):
    iD = StringProperty('')
    time = StringProperty('')
    audience = StringProperty('')
    
    mini_card = StringProperty('')
    big_card = StringProperty('')
    
    subject = StringProperty('')
    teacher = StringProperty('')
    note = StringProperty('')

    def __init__(
        self,
        iD='',
        time='',
        audience='',
        subject='',
        teacher='',
        note='',
        **kwargs  # Используем **kwargs для передачи других параметров
    ):
        super().__init__(**kwargs)  # Инициализируем родительский класс

        # Устанавливаем значения свойств
        self.iD = iD
        self.time = time
        self.audience = audience
        self.subject = subject
        self.teacher = teacher
        self.note = note

        self.released = False
        
        self.toggle_content()
    
    def get_mini_card(self, time, audience):
        if time == '': return ''
        else: time = time.replace(' - ', '|')
        
        size = 12 if len(audience) < 9 else 11
        
        content = f'[size={size}sp]' + time.split('|', 1)[0] + '[/size]'
        content = content + f'[size={size-2}sp]\n—\n[/size]'
        content = content + f'[size={size}sp]' + time.rsplit('|', 1)[-1] + '\n[/size]'
        
        size = 11 if len(audience) < 9 else 9
        
        content = content + f'[size={size}sp]' + audience + '[/size]'
        
        return content
        
    def toggle_content(self):
        if self.released:
            self.big_card = self.teacher
            note = '[size=11sp]' + self.note + '[/size]'
            self.mini_card = note
            
        else:
            self.big_card = self.subject
            self.mini_card = self.get_mini_card(self.time, self.audience)
            
        self.released = not self.released

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

class FacultyScreen(MDScreen):
    def on_pre_enter(self):        
        self.app = MDApp.get_running_app()

        if self.open_profile(
            self.app.faculty_name,
            self.app.faculty_iD,
            self.app.course
            ) == True: return
        
        self.change_faculty()

    def change_faculty(self):
        self.faculties = self.get_faculties()
        
        if -1 in self.faculties:
            self.app.root.current = 'login_screen'
            
        else:
            for index, (key, value) in enumerate(self.faculties.items()):
                self.ids.container.add_widget(
                    OneLineListItem(
                        text=f'{key}',
                        on_release=lambda instance: self.select_course(instance)
                        )
                    )
        
    def get_faculties(self):
        data = {'pagenum': 'tdeduGraph_common'}
        
        try:
            result = self.app.work.post('http://timetable.msu.az/edu_graph_common.php', headers=HEADERS, data=data, allow_redirects=True)
        except:
            return [-1]
            
        result.encoding = 'utf-8'

        soup = BeautifulSoup(result.text, PARSER)

        option_elements = soup.find('select', id='repProfId')
        
        options_spec = {}

        for option in option_elements:
            option_text = option.get_text()
            option_value = option['value']
            options_spec[option_text] = option_value

        del options_spec['- - -']        
        return options_spec

    def select_course(self, instance):
        self.clear_container('Курс')

        name = instance.text
        iD = self.faculties[name]

        if 'М.' in instance.text: courses = 2
        else: courses = 4
        
        for i in range(1, courses+1):
            self.ids.container.add_widget(
                OneLineListItem(
                    text=f'{i}',
                    on_release=lambda instance:
                    self.open_profile(name,iD,instance.text)
                )
            )
        
    def open_profile(self, name, iD, course):
        self.clear_container()

        if name != '':
            self.app.faculty_name = name
            self.app.faculty_iD = iD
            self.app.course = course
            
            with open(self.app.config, 'r', encoding='utf-8') as file:
                config = json.load(file)
                config['faculty_name'] = name
                config['faculty_iD'] = iD
                config['course'] = course
            with open(self.app.config, 'w', encoding='utf-8') as file:
                json.dump(config, file, ensure_ascii=False, indent=4)

            self.app.change_screen('menu_screen')
            
            return True
        else:
            return False

    def clear_container(self, label_text = 'Специальность'):
        container = self.ids.container
        container.clear_widgets()
        self.ids.select_subject.text = label_text
        
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

class MenuScreen(MDScreen):
    current_week = StringProperty()
    current_course = StringProperty()
    current_faculty = StringProperty()
    current_day = StringProperty()
    
    def on_pre_enter(self):
        self.app = MDApp.get_running_app()
        self.weekid, self.weeks = self.get_week_id()

        data = {'profid': self.app.faculty_iD, 'courseid': self.app.course, 'weekid': self.weekid, 'inf': '0'}
        
        if self.weekid != '-1':
            table = self.fetch_table(data)
        else:
            table = [-1]
            
        self.show_messages = True
        
        if -1 in table:
            self.days = []
            self.show_messages = False
            self.dialog = self.app.get_dialog('message', 'Ошибка соединения!')
            self.dialog.open()
        else:
            self.days = self.table_to_days(table)
            
        self.day_of_week = datetime.now().weekday()
        self.update_day_schedule(self.day_of_week)
        
        self.current_day = WEEK[self.day_of_week]
        self.current_faculty = self.app.faculty_name
        self.current_course = f'[size=36sp][b]{self.app.course} Курс[/size][/b]'
        self.current_week = datetime.now().strftime('%d.%m.%Y')
        
        menu_items = [
            {
                'viewclass': 'OneLineListItem',
                'text': week,
                'height': dp(56),
                'on_release': lambda x=week: self.set_week(x),
            } for week in self.weeks
        ]
        
        self.week_button = MDDropdownMenu(
            caller = self.ids.week_item,
            items = menu_items,
            pos_hint = {'center_x': 0.5, 'center_y': 0.5},
            width_mult = 4,
        )
        
        menu_items = [
            {
                'viewclass': 'OneLineListItem',
                'text': day,
                'height': dp(56),
                'on_release': lambda i=day: self.set_day(i),
            } for day in WEEK[:-1]
        ]
        
        self.day_button = MDDropdownMenu(
            caller = self.ids.day_item,
            items = menu_items,
            #size_hint = (0.8, 0.8),
            pos_hint = {'center_x': 0.5, 'center_y': 0.5},
            width_mult = 4,
        )
        
        menu_items = [
            {
                'viewclass': 'OneLineListItem',
                'text': 'Сменить тему',
                'height': dp(56),
                'on_release': lambda i='theme': self.button_action(i),
            },
            {
                'viewclass': 'OneLineListItem',
                'text': 'Сменить специальность',
                'height': dp(56),
                'on_release': lambda i='reset': self.button_action(i),
            }
        ]
        
        self.settings_button = MDDropdownMenu(
            caller = self.ids.settings_button,
            items = menu_items,
            pos_hint = {'center_x': 0.5, 'center_y': 0.5},
            width_mult = 4,
        )
        
        self.day_button.bind()
        self.week_button.bind()
        self.settings_button.bind()
        
        if self.show_messages:
            if self.app.first_launch:
                # message надо поменять
                self.app.get_dialog('info', MESSAGE).open()
                self.app.first_launch = False
                
            self.find_exams()
        else:
            self.show_messages = True

    def fetch_table(self, data):
        try:
            result = self.app.work.post('http://timetable.msu.az/process.php', headers = HEADERS, data=data, allow_redirects=True)
        except:
            return [-1]
        
        result.encoding = 'utf-8'
        soup = BeautifulSoup(result.text, PARSER)
        elements_with_c_top = soup.find_all(class_='c_top')
        
        return [element.get_text(strip=True) for element in elements_with_c_top]

    def get_week_id(self, week = ''):
        weeks = []
        data = {'prof_id': self.app.faculty_iD, 'course_id': self.app.course, 'inf': '0'}
        
        try:
            result = self.app.work.post('http://timetable.msu.az/process.php', headers = HEADERS, data=data, allow_redirects=True)
        except:
            return '-1', weeks 
            
        result.encoding = 'utf-8'
        soup = BeautifulSoup(result.text, PARSER)

        option_elements = soup.find('select', id='repWeekId')
        options_date = {option.get_text().replace(' ', ''): option['value'] for option in option_elements if option['value'] != '0'}
        
        now = datetime.now()

        if week != '':
            return options_date[week], weeks
            
        for key, value in options_date.items():
            weeks.append(key)
            date_min, date_max = [datetime.strptime(date, '%d.%m.%Y') + timedelta(days=offset) for date, offset in zip(key.split('-'), [-1, 1])]
            if date_min <= now <= date_max:
                return value, weeks
        return '', weeks

    def table_to_days(self, table): # Заменить!
        days = []
        
        if table != ['']:
            for i in range(0,6):
                tmp = table[i*38:(i+1)*38]
                if tmp != []:
                    days.append(Day('', list()))
                    days[i].date = tmp[1]
                    tmp = tmp[2:]

                    for j in range(0,6):
                        lesson = Lesson(
                            number = tmp[0+j*6],
                            time = tmp[1+j*6],
                            audience = tmp[2+j*6],
                            subject = tmp[3+j*6],
                            teacher = tmp[4+j*6],
                            note = tmp[5+j*6]
                        )
                        
                        days[i].lessons.append(lesson)

        return days
        
    def update_day_schedule(self, day_of_week = 0):
        self.clear_schedule()
        
        if self.days != [] and day_of_week < 6:
            for lesson in self.days[day_of_week].lessons:
                if lesson.time == '': continue
                self.ids.time_table.add_widget(
                    LessonButton(
                        iD = lesson.number,
                        time = lesson.time,
                        audience = lesson.audience,
                        subject = lesson.subject,
                        teacher = lesson.teacher,
                        note = lesson.note
                    )
                )

    def clear_schedule(self):
        self.ids.time_table.clear_widgets()

    def set_week(self, week):
        self.week_button.dismiss()
        self.weekid, _ = self.get_week_id(week)
        
        data = {'profid': self.app.faculty_iD, 'courseid': self.app.course, 'weekid': self.weekid, 'inf': '0'}
        
        if self.weekid != '-1':
            table = self.fetch_table(data)
        else:
            table = [-1]
            
        if -1 in table:
            self.days = []
            self.show_messages = False
            self.dialog = self.app.get_dialog('message', 'Ошибка соединения!')
            self.dialog.open()
        else:
            self.days = self.table_to_days(table)
            
        self.update_day_schedule()
        self.current_day = WEEK[0]
        self.current_week = week.split('-')[0]
        
    def set_day(self, day):
        self.day_button.dismiss()
        self.update_day_schedule(WEEK.index(day))
        
        current_week = datetime.strptime(self.current_week, '%d.%m.%Y')
        current_week = current_week - timedelta(days=WEEK.index(self.current_day))
        current_day = current_week + timedelta(days=WEEK.index(day))
        
        self.current_day = day
        self.current_week = current_day.strftime('%d.%m.%Y')

    def find_exams(self):
        if self.current_day == 'ВС': return
            
        message = ''
        
        names = [
            'понедельник',
            'вторник',
            'среду',
            'четверг',
            'пятницу',
            'субботу',
            'воскресенье'
        ]
        
        for day in self.days:
            for lesson in day.lessons:
                if 'Зачёт' in lesson.note:
                    day_of_week = WEEK[self.days.index(day)]
                    name = names[WEEK.index(day_of_week)]
                    if day_of_week == 'ВТ':
                        message = message + f'Зачёт во {name}!\n'
                    else:
                        message = message + f'Зачёт в {name}!\n'
                    break
        
        if message != '':
            self.app.get_dialog('message', message).open()
        
    def button_action(self, action):
        self.settings_button.dismiss()
        
        if action == 'theme':
            self.app.change_screen('theme_screen')
        else:
            self.reset_profile()
            
    def reset_profile(self):
        self.app.faculty_name = ''
        self.app.faculty_iD = ''
        self.app.course = ''
        self.app.root.current = 'faculty_screen'

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
        
if __name__ == '__main__':
    TimeTable().run()
