from django.views import View
from django.http import JsonResponse
from travel.models import City


class LoadCitiesView(View):
    def get(self, request, *args, **kwargs):
        country_id = request.GET.get("country_id")

        if not country_id:
            return JsonResponse({"error": "Missing country_id"}, status=400)

        try:
            country_id = int(country_id)
        except ValueError:
            return JsonResponse({"error": "Invalid country_id"}, status=400)

        cities = City.objects.filter(country_id=country_id).only("id", "name").order_by("name")
        return JsonResponse(list(cities.values("id", "name")), safe=False)