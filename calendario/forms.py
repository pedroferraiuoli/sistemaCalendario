from .models import CalendarioEvento
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class UserModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
         return obj.username

class EventoForm(forms.ModelForm):
    class Meta:
        model = CalendarioEvento
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        users = User.objects.all()
        opcoes = (
    ('Nenhuma', 'Nenhuma'),
    ('Mensal', 'Mensal'),
    ('15° dia útil', '15° dia útil'),
    ('7° dia útil', '7° dia útil')
)
        self.fields['descricao'].widget = forms.widgets.Textarea(
            attrs={
                'type': 'text', 'class': 'form-control'
                }
        )

        self.fields['data_limite'].widget = forms.widgets.DateInput(format='%Y-%m-%d',
            attrs={
                'type': 'date', 'class': 'form-control',
                }
            )

        self.fields['titulo'].widget = forms.widgets.TextInput(attrs={
                'type': 'text', 'class': 'form-control'
                })
        
        self.fields['concluido'].widget = forms.CheckboxInput(attrs={'style':'width:20px;height:26px;'})

        self.fields['dataConclusao'].widget = forms.widgets.DateInput(format='%Y-%m-%d',
            attrs={
                'type': 'date', 'class': 'form-control',
                }
            )
        
        self.fields['observacao'].widget = forms.widgets.TextInput(attrs={
                'type': 'text', 'class': 'form-control'
                })
        
        self.fields['recorrencia'] = forms.ChoiceField(choices=opcoes, widget=forms.Select(attrs={'class':"form-control"}), label="Recorrência")

        self.fields['responsavelEvento'] = UserModelChoiceField(queryset=users, widget=forms.Select(attrs={'class':"form-control"}), label='Responsável')
