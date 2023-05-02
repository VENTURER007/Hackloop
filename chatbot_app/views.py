from django.shortcuts import render

# Create your views here.
from http.client import HTTPResponse
from django.shortcuts import render
import os
from dotenv import load_dotenv
import openai

# Create your views here.

load_dotenv()

api_key = os.getenv('OPENAI_KEY',None)
# api_key = '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'
def ai(request):
    response = None
    
    if(api_key is not None and request.method == 'POST'):
        openai.api_key = api_key
        user_input = request.POST.get('user_input')
        prompt = user_input
        response = openai.ChatCompletion.create(model="ada", messages=[{"role": "user", "content": prompt}])
        print(response.choices[0].message.content)
        resp = response.choices[0].message.content
       
        return render(request,'chatbot.html',{'response':resp})
    else:
        print('working')
        return render(request,'chatbot.html')
