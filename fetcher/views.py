from django.shortcuts import render
from django.conf import settings


# Create your views here.
import requests
from django.shortcuts import render

PEXELS_API_KEY = settings.PEXELS_API_KEY


def home(request):
    return render(request, "fetcher/home.html")


def search_images(request):
    query = request.GET.get("query")
    images = []

    if query:
        headers = {"Authorization": PEXELS_API_KEY}
        url = f"https://api.pexels.com/v1/search?query={query}&per_page=12"
        response = requests.get(url, headers=headers)

        print("STATUS:", response.status_code)
        print("JSON:", response.json())  # 👈 This prints to terminal

        if response.status_code == 200:
            data = response.json()
            images = [photo["src"]["medium"] for photo in data["photos"]]

    return render(request, "fetcher/home.html", {"images": images})
