# MSUTT Project

![smartmockups_m297wz3d](https://github.com/user-attachments/assets/49c4ce31-e979-463b-aa82-00dbd08f4fa1)

## О проекте
MSUTT — это тестовый проект, созданный для изучения возможностей мобильной разработки на Python с использованием фреймворков Kivy и KivyMD. Сборка проекта выполняется через Buildozer. Основная функция приложения — отображение актуального расписания занятий Бакинского филиала МГУ. 

## Функциональность
- Отображение расписания занятий в реальном времени.
- Уведомления о предстоящих экзаменах на текущей неделе.
- Возможность кастомизации внешнего вида приложения (в настоящее время доступна только темная тема).

## Структура приложения
This application contains the following screens and classes:

1. **LoginScreen (in `login_screen.py`)**: Represents the login interface.
2. **FacultyScreen (in `faculty_screen`)**: Allows selection of a major and course.
3. **ThemeScreen (in `theme_screen`)**: Provides options for changing the app's appearance.
4. **MenuScreen (in `menu_screen`)**: The main screen with three primary sections:
   - **Schedule**: Displays the current schedule and allows viewing other days.
   - **Profile**: Shows student information (specialty, course) and allows design or specialty updates.
   - **Exit**: Closes the application.

5. **TimeTable (in `time_table`)**: Core class managing screen transitions, loading/saving variables, and handling the dialog system.


## Зависимости
Проект использует следующие зависимости:
- `buildozer`
- `requests`
- `datetime`
- `beautifulsoup4`
- `kivy==2.2.0`
- `kivymd==1.2.0`
- `pillow`

Если вы используете парсер `lxml`, добавьте также:
- `lxml==5.1.0`

## Поддерживаемые платформы
MSUTT работает на компьютерах и смартфонах.

- **Смартфоны**: поддерживаются устройства на базе Android и iOS (для iOS требуется дополнительная настройка сборки).
- **Компьютеры**: поддерживаются платформы Windows, Linux и macOS.

Для сборки проекта под смартфоны используется Buildozer. По умолчанию, файл `buildozer.spec` настроен для устройств с Android 8.1 и выше. Поддержка iOS требует дополнительных шагов, таких как настройка окружения на macOS с установленным Xcode. Если при сборке возникают ошибки или приложение не запускается после установки, можно попробовать использовать альтернативный код. Для этого удалите все файлы `.py` из папки `src` и скопируйте файл `main.py` из деректории `alt` обратно в `src`. После этого пересоберите приложение заново.

### Примечание:
Размер готового приложения может зависеть от операционной системы, на которой производится сборка. Рекомендуется избегать сборки на виртуальной машине, так как есть вероятность, что размер приложения увеличится вдвое.

## Обратная связь
Если у вас возникли вопросы или предложения, пожалуйста, создайте [issue](https://github.com/MajidIsaev/MSUTT/issues) на GitHub или свяжитесь со мной по email: isaevmajidelman@gmail.com.

## Лицензия
Этот проект распространяется под лицензией MIT. Подробнее смотрите в файле [LICENSE](LICENSE).

## Полезные ссылки
- [Документация Kivy](https://kivy.org/doc/stable/)
- [Документация KivyMD](https://kivymd.readthedocs.io/en/1.1.1/)
- [Руководство по Buildozer](https://buildozer.readthedocs.io/en/latest/)
