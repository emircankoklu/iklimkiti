from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import redirect, render

from accounts.models import UserProfile


@login_required
def profile_view(request):
    progress_count = request.user.gameprogress_set.count()
    profile = UserProfile.objects.filter(user=request.user).first()
    return render(request, 'accounts/profile.html', {'profile': profile, 'progress_count': progress_count})


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.get_or_create(user=user, defaults={'display_name': user.username})
            login(request, user)
            messages.success(request, 'Hesabınız oluşturuldu. Hoş geldiniz!')
            return redirect('profile')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'Giriş yapıldı.')
                return redirect('profile')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'Çıkış yapıldı.')
    return redirect('home')
