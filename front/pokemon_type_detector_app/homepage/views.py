
from os import path
from io import BytesIO
from PIL import Image
from  base64 import b64encode, b64decode
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .model.pokemon_detector_type import predict_type
PATH = path.dirname(path.abspath(__file__))
def decode_img(msg):
    # msg = msg[msg.find(b"<plain_txt_msg:img>")+len(b"<plain_txt_msg:img>"):
    #           msg.find(b"<!plain_txt_msg>")]
    msg = b64decode(msg)
    buf = BytesIO(msg)
    img = Image.open(buf)
    return img
def encode_base64(img):
    output_buffer = BytesIO()
    img.save(output_buffer, format='JPEG')
    byte_data = output_buffer.getvalue()
    base64_str = b64encode(byte_data)
    return base64_str

# Create your views here.
def homepage(request):
    print("homepage loaded")
   
    print(request.FILES)
    # pokemon = request.GET.get('pokemon',"Default")
    # print(pokemon)
    print(request.method, "myfile" in request.FILES.keys())
    if "myfile" in request.FILES.keys():
        pokemon = "Bulbasaur"
        if request.method == 'POST':
            print(request.POST)
            # if "pokemon" in request.POST.keys(): 
            pokemon = request.POST.get("pokemon")
            
            myfile = request.FILES['myfile']
            encode_image = b64encode(myfile.read())
            img = decode_img(encode_image)
            result = predict_type(img , pokemon)
            encode_image = encode_base64(result)
    else:
        image_path = path.join(PATH, "model/pokemon.png")
        with open(image_path,"rb") as f:
            encode_image = b64encode(f.read())
        # img.save("a.png",format="png")
    # encode_image = "iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg=="
    # base_64_image = f'"data:image/png;base64, {encode_image}"'
    return render(request,"homepage/homepage.html", {"image_base_64":encode_image.decode()})