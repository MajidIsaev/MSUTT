# MSUTT Project

![smartmockups_m297wz3d](https://github.com/user-attachments/assets/49c4ce31-e979-463b-aa82-00dbd08f4fa1)

## About the Project
MSUTT is a test project created to explore mobile development possibilities using Python, with Kivy and KivyMD frameworks. The project is built via Buildozer, and its main function is to display the current class schedule for the Baku branch of Moscow State University.

## Features
- Real-time class schedule display.
- Notifications for upcoming exams during the current week.
- Option to customize the app's appearance (currently only a dark theme is available).

## Structure
This application contains the following screens and classes:

1. **LoginScreen (in `login_screen.py`)**: Represents the login interface.
2. **FacultyScreen (in `faculty_screen`)**: Allows selection of a major and course.
3. **ThemeScreen (in `theme_screen`)**: Provides options for changing the app's appearance.
4. **MenuScreen (in `menu_screen`)**: The main screen with three primary sections:
   - **Schedule**: Displays the current schedule and allows viewing other days.
   - **Profile**: Shows student information (specialty, course) and allows design or specialty updates.
   - **Exit**: Closes the application.

5. **TimeTable (in `time_table`)**: Core class managing screen transitions, loading/saving variables, and handling the dialog system.

## Dependencies
The project uses the following dependencies:
- `buildozer`
- `requests`
- `datetime`
- `beautifulsoup4`
- `kivy==2.2.0`
- `kivymd==1.2.0`
- `pillow`

If using the `lxml` parser, also include:
- `lxml==5.1.0`

## Supported Platforms
MSUTT runs on computers and smartphones.

- **Smartphones**: Android and iOS devices are supported (iOS requires additional setup).
- **Computers**: Windows, Linux, and macOS are supported.

Buildozer is used to build the project for smartphones. By default, the `buildozer.spec` file is configured for Android 8.1+ devices. iOS support requires additional steps, like setting up the environment on macOS with Xcode.

### Note:
The final app size may vary depending on the operating system used for building. Avoid building on a virtual machine, as this may double the app size.

## Feedback
If you have questions or suggestions, please create an [issue](https://github.com/MajidIsaev/MSUTT/issues) on GitHub or contact me via email at isaevmajidelman@gmail.com.

## License
This project is licensed under the MIT License. For details, see the [LICENSE](LICENSE) file.

## Useful Links
- [Kivy Documentation](https://kivy.org/doc/stable/)
- [KivyMD Documentation](https://kivymd.readthedocs.io/en/1.1.1/)
- [Buildozer Guide](https://buildozer.readthedocs.io/en/stable/)