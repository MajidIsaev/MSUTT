[app]

title = MSUTT

version = 0.4

package.name = msutt

package.domain = app.msutt


source.dir = ./src

source.include_exts = py,webp,kv,json

source.exclude_exts = spec, md, log

source.exclude_dirs = tests, bin, venv

requirements = kivy,kivymd==1.2.0,datetime,beautifulSoup4,requests,pillow


fullscreen = 0

orientation = portrait

icon.filename = ./logo.png

#presplash.filename = %(source.dir)s/logo.webp


android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE

android.sqlite3 = False

android.compress_level = 9

android.strip_mode = everything

android.keep_screensize_restrictions = False

android.proguard = True

android.minapi = 27

android.archs = armeabi-v7a

android.allow_backup = False

android.release_artifact = apk


p4a.bootstrap = sdl2

p4a.opt = --without-java-doc

#p4a.extra_args = --blacklist-requirements=sqlite3,libffi,openssl


[buildozer]

log_level = 2

warn_on_root = 1

