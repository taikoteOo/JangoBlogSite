from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

from users.forms import RegistrationForm, NewRegistrationForm


def register(request):
    # Когда отправляем форму на сервер
    if request.method == 'POST':
        # создаём объект формы с данными из запроса
        form = NewRegistrationForm(request.POST)
        # если форма валидна
        if form.is_valid():
            # создаём объект пользователя без записи в ДБ
            new_user = form.save(commit=False)
            # хешируем пароль
            new_user.set_password(form.cleaned_data['password'])
            # сохраняем пользователя в ДБ
            new_user.save()
            context = {'title':'Регистрация завершена', 'new_user': new_user}
            return render(request, template_name='users/registration_done.html', context=context)
    # Если метод GET (страница с пустой формой регистрации)
    form = NewRegistrationForm()
    context = {'title':'Регистрация пользователя', 'register_form': form}
    return render(request, template_name='users/registration.html', context=context)

def log_in(request):
    pass

def log_out(request):
    pass

def user_profile(request, pk):
    pass
