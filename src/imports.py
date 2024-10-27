from kivymd.app import MDApp

from kivymd.uix.screen import MDScreen
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import OneLineListItem
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog

from kivy.metrics import dp
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.properties import StringProperty
from kivy.uix.behaviors import ButtonBehavior

from kivymd.uix.behaviors import (
    RectangularRippleBehavior,
    BackgroundColorBehavior,
    CommonElevationBehavior,
)

from bs4 import BeautifulSoup
from requests import Session
from datetime import datetime, timedelta
import json
import time


HEADERS = {"User-Agent": "CroockedHands/2.0 (EVM x8), CurlyFingers20/1;p"}

WEEK = ["ПН", "ВТ", "СР", "ЧТ", "ПТ", "СБ", "ВС"]

PARSER = "html"  #'lxml'

CONFIG = "config.json"

INTRO = "intro.json"

MAX_OF_DIALOGS = 10
 