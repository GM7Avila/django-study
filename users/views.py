from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from . forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from . forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save() # hash automático da senha

            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        user_update_form = UserUpdateForm(request.POST, instance=request.user)
        profile_update_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user.profile
        )
        
        if user_update_form.is_valid() and profile_update_form.is_valid():
            if user_update_form.has_changed() or profile_update_form.has_changed():
                user_update_form.save()
                profile_update_form.save()
                messages.success(request, f'Your account has been updated!')
            else:
                messages.info(request, 'No changes detected.')
            
            return redirect('profile')
    
    else:
        user_update_form = UserUpdateForm(instance=request.user)
        profile_update_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_update_form': user_update_form,
        'profile_update_form': profile_update_form
    }

    return render(request, 'users/profile.html', context)