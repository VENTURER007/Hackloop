from django.shortcuts import render

# Create your views here.
def signs(request):
    return render(request,'hostels.html')