from django.http import HttpRequest
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView, ListView
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator

from .forms import UserRegister
from .models import Buyer, Game


class MainPage(TemplateView):
    template_name = 'task1/main_page.html'
    extra_context = {
        'title': 'Главная страница магазина',
    }

# Используем класс ListView для разделения списка объектов на страницы
class ShopPage(ListView):
    template_name = 'task1/shop.html'
    # Связываем используемую модель и шаблон
    model = Game
    # Количество элементов на странице
    paginate_by = 1

    def get_context_data(self, **kwargs):
        # Создаем контекст для шаблона
        context = super().get_context_data(**kwargs)

        games = self.model.objects.all()
        if not games:
            context['error'] = 'Игры не найдены'
        else:
            paginator = Paginator(games, self.paginate_by)
            page_number = self.request.GET.get('page')
            games = paginator.get_page(page_number)
            context['games'] = games
            context['title'] = 'Игры'
        return context


class CartPage(TemplateView):
    template_name = 'task1/cart.html'
    extra_context = {
        'title': 'Ваша корзина',
    }


# Регистрация через класс и форму
class SignUpPage(View):

    def get(self, request: HttpRequest):
        info = {}
        info['form'] = UserRegister()
        return render(request, 'task1/registration_page.html', context=info)

    def post(self, request: HttpRequest):
        info = {}

        form = UserRegister(request.POST)
        info['form'] = form

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            password2 = form.cleaned_data['password2']
            age = form.cleaned_data['age']
            # Проверяем совпадение паролей
            if password != password2:
                info['error'] = 'Пароли не совпадают'
                return render(request, 'task1/registration_page.html', context=info)
            # Проверяем наличие пользователя в базе данных
            try:
                user = Buyer.objects.filter(name=username).first()
            except ObjectDoesNotExist:
                try:
                    Buyer.objects.create(name=username, age=age)
                except Exception as e:
                    info['error'] = f'Ошибка при создании пользователя: {e}'
                else:
                    info['message'] = f'Приветствуем, {username}!'
            else:
                info['error'] = 'Пользователь с таким именем уже существует'
                return render(request, 'task1/registration_page.html', context=info)
        else:
            info['error'] = 'Ошибка в валидации формы'
        return render(request, 'task1/registration_page.html', context=info)
