from imports import *

MESSAGE = '''Примечание к выпуску:

Приложение находится в альфа-версии и может содержать множество ошибок. Пожалуйста, примите это к сведению!

1. При нажатии на предмет отображаются имя преподавателя и примечание к предмету.
   
2. При повторном нажатии содержимое возвращается к исходному виду.
   
3. Предметы с зачетами выделены особым цветом.

4. При входе в приложение оно уведомит о наличии зачетов на текущей неделе.

5. В профиле можно изменить специальность.'''
        
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