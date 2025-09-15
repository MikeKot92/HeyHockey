from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Prefetch
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from common.mixins import CacheMixin, TitleMixin
from orders.models import Order, OrderItem
from users.forms import UserLoginForm, UserProfileForm, UserRegistrationForm

User = get_user_model()


class UserLoginView(TitleMixin, SuccessMessageMixin, LoginView):
    title = 'Login'
    form_class = UserLoginForm
    template_name = 'users/login.html'
    success_message = 'Вы вошли в аккаунт!'

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')
        if not remember_me:
            self.request.session.set_expiry(0)
        return super().form_valid(form)


class UserRegistrationView(TitleMixin, SuccessMessageMixin, CreateView):
    title = 'Registration'
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('main:home')
    success_message = 'Вы успешно зарегестрировались!'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, self.success_message)
        return HttpResponseRedirect(self.success_url)


class UserProfileView(TitleMixin, CacheMixin, LoginRequiredMixin, UpdateView):
    title = 'Profile'
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('user:profile')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Данные успешно обновлены!")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orders = Order.objects.filter(user=self.request.user).prefetch_related(Prefetch(
            'items', queryset=OrderItem.objects.select_related('product'))).order_by('-id')
        context['orders'] = self.set_get_cache(orders, f'orders_for_user{self.request.user.id}', 60)
        return context


class UserLogoutView(LogoutView):
    success_message = 'Вы вышли из аккаунта!'

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, self.success_message)
        return super().dispatch(request, *args, **kwargs)
