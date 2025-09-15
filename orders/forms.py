from django import forms
from django.core.validators import RegexValidator


class FormOrder(forms.Form):
    first_name = forms.CharField(
        label='Имя',
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'required': True
        })
    )

    last_name = forms.CharField(
        label='Фамилия',
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'required': True
        })
    )

    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'required': True
        })
    )

    phone = forms.CharField(
        label='Телефон',
        max_length=50,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{11}$',
                message="Введите корректный номер телефона (например, +79991234567).",
            )
        ],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'required': True
        })
    )

    DELIVERY_CHOICES = [
        ('pickup', 'Самовывоз'),
        ('courier', 'Курьерская доставка'),
    ]

    delivery_method = forms.ChoiceField(
        label='Способ доставки',
        choices=DELIVERY_CHOICES,
        initial='pickup',
        widget=forms.RadioSelect
    )

    city = forms.CharField(
        label='Город',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        })
    )

    street = forms.CharField(
        label='Улица',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        })
    )

    house = forms.CharField(
        label='Дом',
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        })
    )

    apartment = forms.CharField(
        label='Квартира',
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        })
    )

    PAYMENT_CHOICES = [
        ('online', 'Онлайн оплата'),
        ('cash_on_delivery', 'Оплата при получении'),
    ]

    payment_method = forms.ChoiceField(
        label='Способ оплаты',
        choices=PAYMENT_CHOICES,
        initial='online',
        widget=forms.RadioSelect
    )

    comment = forms.CharField(
        label='Комментарий к заказу',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ['delivery_method', 'payment_method']:
            if field_name in self.fields:
                self.fields[field_name].widget.attrs.update({
                    'class': 'form-check-input',
                    'id': f'id_{field_name}'
                })

    def clean(self):
        cleaned_data = super().clean()
        delivery_method = cleaned_data.get('delivery_method')
        if delivery_method in ['courier']:

            city = cleaned_data.get('city')
            street = cleaned_data.get('street')
            house = cleaned_data.get('house')

            if not city:
                self.add_error('city', 'Город обязателен при курьерской доставке.')
            if not street:
                self.add_error('street', 'Улица обязательна при курьерской доставке.')
            if not house:
                self.add_error('house', 'Номер дома обязателен при курьерской доставке.')

        return cleaned_data
