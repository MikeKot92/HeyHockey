from django import forms

from goods.models import Categories, Size


class FilterForm(forms.Form):
    SORT_CHOICES = (
        ('default', 'по умолчанию'),
        ('price', 'по возрастанию'),
        ('-price', 'по убыванию'),
    )
    price = forms.ChoiceField(
        label='Цена',
        choices=SORT_CHOICES,
        initial='default',
        widget=forms.Select(attrs={'class': 'form-select form-select-sm'})
    )

    discount = forms.BooleanField(
        label='Товары по акции',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    category = forms.ModelMultipleChoiceField(
        queryset=Categories.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False,
        label='Категории'
    )

    size = forms.ModelMultipleChoiceField(
        queryset=Size.objects.all().exclude(name='Б/р'),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False,
        label='Размеры'
    )
