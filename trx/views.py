import profile
from django.shortcuts import render
from home.models import Profile

def main_view(request,*args,**kwargs):
    code = str(kwargs.get('ref_code'))
    try:
        profile = Profile.objects.get(code = code)
        request.session['ref-profile']
        print('id',profile.id)
    except:
        pass
    print(request.session.get_expiry_date())
    return render(request,"home/main.html")


