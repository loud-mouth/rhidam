from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from login_module.models import Profile

from .forms import SongUploadForm, ProfileChangeForm, UserChangeForm
from .models import Song

@login_required
def user_profile(request):
    user = request.user
    profile = request.user.profile
    form1 = ProfileChangeForm(instance=profile)
    form2 = UserChangeForm(instance=user)
    context = {
        'form1' : form1,
        'form2' : form2,
        'logged_in_user_username' : request.user,
    }
    
    if request.method == 'POST':
        form1 = ProfileChangeForm(request.POST, request.FILES, instance=profile)
        form2 = UserChangeForm(request.POST, request.FILES, instance=user)
        if( form1.is_valid() and form2.is_valid() ):
            profile = form1.save()
            user = form2.save()
            if(profile.profile_pic == ''):
                profile.profile_pic = 'noimage.jpg'


    return render(request, 'core_app/user_profile.html', context=context)

def HomepageView(request):
    return render(request, 'core_app/Homepage.html')
    pass

@login_required
def dashboard(request):
    form = SongUploadForm()
    a = User.objects.filter(username=request.user)[0]
    user = Profile.objects.filter(user=a)[0]
    songs_list = Song.objects.filter(owner=user)
    
    context = {
        'form' : form,
        'songs_list' : songs_list,
        'my_user' : user.user,
    }

    if request.method == 'POST':
        try:
            songUploaded = request.POST['songup']
            if songUploaded == '1':
                form = SongUploadForm(request.POST)
                if form.is_valid():
                    a = User.objects.filter(username=request.user)[0]
                    user = Profile.objects.filter(user=a)[0]
                    new_song = Song(owner=user, songLink=request.POST['songLink'], songName=request.POST['songName'])
                    new_song.save()
                    messages.success(request, "Song successfully uploaded")
                return redirect('core_app:dashboard')
        except:
            pass
    return render(request, 'core_app/dashboard.html', context=context)
            
