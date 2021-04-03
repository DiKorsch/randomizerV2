from django.forms import ModelForm
from core.models import Player

class NewPlayerForm(ModelForm):
	class Meta:
		model = Player
		fields = ["username"]
