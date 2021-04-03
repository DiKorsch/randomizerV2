from django.conf import settings

from functools import wraps

def ensure_uuid(method):

	@wraps(method)
	def inner(self, request, *args, **kwargs):
		key = settings.ANONYMOUS_USER_COOKIE_ID
		cookies = request.COOKIES

		if key not in cookies:
			cookies[key] = request.session._get_new_session_key()

		uuid = cookies[key]

		resp = method(self, request, *args, **kwargs)
		resp.set_cookie(key, uuid)
		return resp

	return inner
