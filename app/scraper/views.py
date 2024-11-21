from django.http import JsonResponse
from django.views import View
from .my_republica_scraper import MyRepublicaScraper


class ScrapeView(View):
    def get(self, request, *args, **kwargs):
        scraper = MyRepublicaScraper()
        scraper.scrap()  # Call the scraping method
        return JsonResponse({"message": "Scraping completed."})
