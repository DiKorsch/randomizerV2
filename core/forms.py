from django import forms
from core.models import Player

class NewPlayerForm(forms.ModelForm):
	class Meta:
		model = Player
		fields = ["username"]

		widgets = {
			'username': forms.TextInput(attrs=dict(placeholder="Dein Name")),
		}
