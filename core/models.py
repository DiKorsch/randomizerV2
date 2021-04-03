from django.db import models
from django.contrib import admin


class Player(models.Model):

	uuid = models.CharField(max_length=127,
		verbose_name="UUID")

	username = models.CharField(max_length=127)

	last_active = models.DateTimeField(
		verbose_name="Zuletzt Aktiv")


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
	list_display = (
		"username",
		"last_active",
		# "uuid",
	)

	list_filter = [
		"last_active"
	]


