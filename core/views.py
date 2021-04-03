from django.conf import settings
from django.shortcuts import redirect
from django.views.generic import TemplateView

from core.decorators import ensure_uuid


class IndexView(TemplateView):
	template_name = "index.html"

	@ensure_uuid
	def get(self, request, *args, **kwargs):
		context = self.get_context_data(**kwargs)
		context["session"] = request.COOKIES[settings.ANONYMOUS_USER_COOKIE_ID]
		return self.render_to_response(context)

	@classmethod
	def clear_cookie(cls, request):
		resp = redirect("index")
		resp.delete_cookie(settings.ANONYMOUS_USER_COOKIE_ID)
		return resp
