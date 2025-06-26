from django.shortcuts import render
from django.conf import settings

from pathlib import Path
import os
import requests
from django.http import HttpResponse
from django.shortcuts import redirect

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


def download_images(request):
    if request.method == "POST":
        image_urls = request.POST.getlist("selected_images")

        # Get system Downloads folder path
        downloads_path = Path.home() / "Downloads"
        os.makedirs(downloads_path, exist_ok=True)

        for url in image_urls:
            try:
                image_name = url.split("/")[-1].split("?")[0]  # clean file name
                response = requests.get(url)
                if response.status_code == 200:
                    with open(os.path.join(downloads_path, image_name), "wb") as f:
                        f.write(response.content)
            except Exception as e:
                print(f"Error downloading {url}: {e}")

        return HttpResponse(
            f"{len(image_urls)} image(s) downloaded successfully to your Downloads folder!"
        )

    return redirect("home")
