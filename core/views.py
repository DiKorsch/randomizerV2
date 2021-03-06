from django.conf import settings
from django.shortcuts import redirect
from django.utils import timezone as tz
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from core.decorators import context_render
from core.decorators import ensure_uuid
from core.forms import NewPlayerForm
from core.models import Player


class IndexView(TemplateView):
	template_name = "index.html"

	def get_context_data(self, *args, **kwargs):
		context = super(IndexView, self).get_context_data(*args, **kwargs)
		uuid = self.request.COOKIES[settings.ANONYMOUS_USER_COOKIE_ID]
		context["uuid"] = uuid
		return context

	@method_decorator(ensure_uuid)
	@context_render
	def get(self, request, context, *args, **kwargs):

		uuid = context["uuid"]
		now = tz.now()

		try:
			player = Player.objects.get(uuid=uuid)
			context["player"] = player
			player.last_active = now
			player.save()

		except Player.DoesNotExist:
			new_player = Player(uuid=uuid, last_active=now)
			context["form"] = NewPlayerForm(instance=new_player)

		return context

	@context_render
	def post(self, request, context, *args, **kwargs):

		uuid = context["uuid"]

		player = Player(uuid=uuid, last_active=tz.now())
		form = NewPlayerForm(request.POST, instance=player)

		player = form.save()
		context["player"] = player
		return context

	@classmethod
	def clear_cookie(cls, request):
		uuid = request.COOKIES[settings.ANONYMOUS_USER_COOKIE_ID]
		Player.objects.filter(uuid=uuid).delete()

		resp = redirect("index")
		resp.delete_cookie(settings.ANONYMOUS_USER_COOKIE_ID)

		return resp
