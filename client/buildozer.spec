[app]

title = TournamentApp

package.name = tournamentapp
package.domain = org.example

version = 1.0.0

source.dir = src

icon.filename = data/app_icon.png

source.include_exts = py, png
source.include_patterns = images/*

requirements = kivy, requests
android.permissions = INTERNET

orientation = portrait
fullscreen = 1

[buildozer]
requirements.source.virtualenv = .venv

log_level = 2

