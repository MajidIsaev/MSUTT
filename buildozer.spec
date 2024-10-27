[app]

title = MSUTT

version = 1.0

package.name = msutt

package.domain = app.majid


source.dir = ./src

source.include_exts = py,webp,kv,json

source.exclude_exts = spec, md, log

source.exclude_dirs = tests, bin, venv

requirements = python3,kivy,kivymd==1.2.0,datetime,beautifulSoup4,requests,pillow


fullscreen = 0

orientation = portrait

icon.filename = ./logo.png

presplash.filename = ./logo.png

android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE

android.minapi = 27

android.archs = armeabi-v7a

android.allow_backup = False

android.release_artifact = apk


[buildozer]

log_level = 2

warn_on_root = 1

