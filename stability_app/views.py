from django.shortcuts import render
#import getpass
import io
import os
import warnings

# NB: host url is not prepended with \"https\" nor does it have a trailing slash.
os.environ['STABILITY_HOST'] = 'grpc.stability.ai:443'

# To get your API key, visit https://beta.dreamstudio.ai/membership
os.environ['STABILITY_KEY'] = 'sk-s9phuuOg65Tws5VMyGW11VvI4vtDnLLy0CleqCjoLhE2s2Xa'

#binary to image format
import base64
from io import BytesIO

from IPython.display import display
from PIL import Image
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation


# Create your views here.
def stable(request):
    response = None
    stability_api = client.StabilityInference(
    key=os.environ['STABILITY_KEY'], 
    verbose=True,
    )
    if(stability_api is not None and request.method == 'POST'):
        user_input = request.POST.get('user_input')
        answers = stability_api.generate(
        prompt=user_input,
        seed=34567, # if provided, specifying a random seed makes results deterministic
        steps=20, # defaults to 30 if not specified
        )
        for resp in answers:
            for artifact in resp.artifacts:
                if artifact.finish_reason == generation.FILTER:
                    warnings.warn(
                        "Your request activated the API's safety filters and could not be processed."
                        "Please modify the prompt and try again.")
                if artifact.type == generation.ARTIFACT_IMAGE:
                    img = Image.open(io.BytesIO(artifact.binary))
                    buffered = BytesIO()
                    img.save(buffered, format="PNG")
                    img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
                    data_url = f"data:image/png;base64,{img_base64}"    
        if data_url is not None:
            return render(request,'stability.html',{'img_src':data_url})
        else:
            return render(request,'stability.html')
    else:
        return render(request,'stability.html')

    