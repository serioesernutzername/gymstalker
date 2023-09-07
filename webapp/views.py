from django.shortcuts import render
import webscraper.main
from django.http import HttpResponse

def index(request):
    with open('data.csv', "r", encoding="utf-8", errors="ignore") as csvfile:
        final_line = csvfile.readlines()[-1]
    return render(request, "index.html", {"text": final_line, "title": "Sportfabrik Besucherzahlen"})
