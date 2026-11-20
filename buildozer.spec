[app]
title = JARVIS
package.name = jarvis
package.domain = org.faisal
source.dir = .
source.include_exts = py
version = 1.0
requirements = python3,kivy==2.3.0,requests,plyer,urllib3,certifi,idna,charset-normalizer
orientation = portrait
fullscreen = 0
android.permissions = INTERNET,RECORD_AUDIO
android.api = 33
android.minapi = 21
android.archs = arm64-v8a
android.accept_sdk_license = True

[buildozer]
log_level = 2
