from imports import *

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
        content += f'[size={size-2}sp]\n—\n[/size]'
        content += f'[size={size}sp]' + time.rsplit('|', 1)[-1] + '\n[/size]'
        
        size = 11 if len(audience) < 9 else 9
        
        content += f'[size={size}sp]' + audience + '[/size]'
        
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