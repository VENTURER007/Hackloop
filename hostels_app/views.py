from django.shortcuts import render

# Create your views here.
def hostels(request):
    return render(request,'hostels.html')