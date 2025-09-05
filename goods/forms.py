from django import forms
from goods.models import Categories, Size


# class FilterForm(forms.Form):
#     price_choice = (('default', 'по умолчанию',), ('price', 'по возрастанию'), ('-price', 'по убыванию',),)
#     price = forms.ChoiceField(label='Цена', choices=price_choice, initial=price_choice)
#     discount = forms.BooleanField(label='Товары по акции', required=False)
#     category = forms.ModelChoiceField(Categories.objects.all(), label='Выберите категорию', empty_label='все', required=False)
#     size = forms.ModelChoiceField(Size.objects.all().exclude(name='Б\р'), label='Выберите размер', empty_label='все', required=False)


class FilterForm(forms.Form):
    # Существующие поля
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


    # Размеры
    size = forms.ModelMultipleChoiceField(
        queryset=Size.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False,
        label='Размеры'
    )

