from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render

from .forms import LoginForm, PerfilForm, RegistroForm, UserEditForm
from .models import Perfil


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True


def registro(request):
    if request.user.is_authenticated:
        return redirect('posts:list')
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Cuenta creada. ¡Bienvenido!')
            return redirect('posts:list')
    else:
        form = RegistroForm()
    return render(request, 'accounts/registro.html', {'form': form})


@login_required
def perfil(request):
    Perfil.objects.get_or_create(user=request.user)
    return render(request, 'accounts/perfil.html', {'posts': request.user.posts.all()})


@login_required
def editar_perfil(request):
    perfil_obj, _ = Perfil.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        perfil_form = PerfilForm(request.POST, request.FILES, instance=perfil_obj)
        if user_form.is_valid() and perfil_form.is_valid():
            user_form.save()
            perfil_form.save()
            messages.success(request, 'Perfil actualizado.')
            return redirect('accounts:perfil')
    else:
        user_form = UserEditForm(instance=request.user)
        perfil_form = PerfilForm(instance=perfil_obj)
    return render(request, 'accounts/editar_perfil.html', {'user_form': user_form, 'perfil_form': perfil_form})
