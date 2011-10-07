from django import forms

class HackForm(forms.Form):
    q_id = forms.CharField(max_length=5)
    answer = forms.CharField(max_length=100)
