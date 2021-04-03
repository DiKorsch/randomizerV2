import datetime as dt

from django.http import JsonResponse
from django.core import serializers

from core.models import Player

def players(request):
	now = dt.datetime.now()
	diff = dt.timedelta(hours=1)

	data = {}
	players = Player.objects.filter(last_active__gte=now-diff)

	data["players"] = [p.to_json() for p in players]
	return JsonResponse(data)

