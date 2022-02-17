from django import forms
from .models import Mechanic, Request, Customer
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox


class Account(forms.Form):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)


class AdminUpdateMechanic(forms.ModelForm):
    class Meta:
        model = Mechanic
        fields = [
            'skill',
            'salary',
            'hired',
        ]


class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = [
            'category',
            'vehicle_no',
            'vehicle_name',
            'vehicle_model',
            'vehicle_brand',
            'problem_description',
            'customer',
            'mechanic',
            'cost',
            'status',
        ]


class CustomerUpdateForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'


class MechanicUpdateStatus(forms.ModelForm):
    class Meta:
        model = Mechanic
        fields = [
            'username',
            'email',
            'phone',
            'location',
            'image',
            'skill'
        ]


class MechanicUpdateForm(forms.ModelForm):
    class Meta:
        model = Mechanic
        fields = '__all__'