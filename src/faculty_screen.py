from imports import *

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