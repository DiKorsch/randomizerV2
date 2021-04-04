import datetime as dt
from django.utils import timezone as tz

from django.http import JsonResponse
from django.core import serializers
from django.views import View

from core.models import Player

def players(request):
	now = tz.now()
	diff = dt.timedelta(hours=1)

	data = {}
	players = Player.objects.filter(last_active__gte=now-diff)

	data["players"] = [p.to_json() for p in players]
	return JsonResponse(data)

class Randomize(View):

	def post(self, request):
		print(request.POST)
		return JsonResponse({"bar": 2})

