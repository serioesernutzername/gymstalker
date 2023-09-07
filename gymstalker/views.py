from django.shortcuts import render
import gymstalker.tools.webscraper
from django.http import HttpResponse


def startseite(request):
    besucherzahl = gymstalker.tools.webscraper.save_data()
    return render(request, "startseite.html", {"text": besucherzahl, "title": "Startseite"})
