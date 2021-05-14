import io
import os
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# from IPython.display import display
from PIL import Image,ImageDraw,ImageFont 
from glob import glob
from tensorflow.keras.applications.vgg16 import  preprocess_input
from tensorflow.keras.models import load_model

# Delete if you don't have GPU rtx 3000 series 
# from tensorflow.compat.v1 import ConfigProto
# from tensorflow.compat.v1 import InteractiveSession

# config = ConfigProto()
# config.gpu_options.allow_growth = True
# session = InteractiveSession(config=config)

sns.set_style("whitegrid")
PATH = os.path.dirname(os.path.abspath(__file__))
def get_concat_h(im1, im2):
    dst = Image.new('RGB', (im1.width + im2.width, im1.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst

def get_proba_plot(data_type):
    buffer = io.BytesIO()
    plt.subplots(figsize = (25,15))
    ax = sns.barplot(x='proba', y='type', data=data_type, palette = "Blues_r")
    ax.set_xlabel('Probability')
    plt.yticks(fontsize = 30)
    plt.xticks(fontsize = 30)
    plt.ylabel("Type", fontsize = 38)
    plt.xlabel("Probability", fontsize = 38);
    plt.title("Model Results", fontsize = 50)
    plt.savefig(buffer, format='png')
#     plt.show()
    plt.close()
    buffer.seek(0)
    chart_probability= Image.open(buffer).resize((512+256,512))
    return chart_probability

def remove_transparency(image):
    new_image = Image.new("RGBA", image.size, "WHITE")
    new_image.paste(image, (0, 0), image)
    new_image.convert('RGB')
    return new_image
def get_pokemon_show(pokemon_img, pokemon = ""):
    if isinstance(pokemon_img,str):
        pokemon_img = Image.open(pokemon_img)
    pokemon_img = pokemon_img.resize((256,256)).convert("RGBA")
    
#     if pokemon_img.mode=="RGBA":
    pokemon_img = remove_transparency(pokemon_img)
#     display(pokemon_img)
#     print(np.array(pokemon_img).min(),np.array(pokemon_img).max())
    pokedex_number,type_1,type_2,species =\
            data.loc[data["name"] == pokemon,["pokedex_number","type_1","type_2","species"]].values[0]
    background = Image.open(os.path.join(PATH,f"utils/types/backs/{type_1}.png")).resize((512,512))
    type_1_img = Image.open(os.path.join(PATH,f"utils/types/cut/{type_1}.png")).resize((134//2,172//2))
    type_1_img = remove_transparency(type_1_img)
    background.paste(type_1_img,box = (0,400))

    if type_2 != "No_type":
        type_2_img = Image.open(os.path.join(PATH,f"utils/types/cut/{type_2}.png")).resize((134//2,172//2))
        type_2_img = remove_transparency(type_2_img)
        background.paste(type_2_img,box = (80,400),mask = 0)
        
    background.paste(pokemon_img,(100,100))
    draw = ImageDraw.Draw(background)
    font_1 = ImageFont.truetype(font = os.path.join(PATH, "utils/fonts/NIKOLETA.ttf"),size =  40)
    font_2 = ImageFont.truetype(font = os.path.join(PATH, "utils/fonts/NIKOLETA.ttf"),size =  30)
    pokemon = " ".join(pokemon.split(" ")[:2])
    # draw.text((256, 420), f"{pokedex_number}. {pokemon}",(0,0,0),font=font_1)
    draw.text((100, 50), f"{pokedex_number}. {pokemon}",(0,0,0),font=font_1)

    draw.text((256, 420), species,(0,0,0),font=font_2)
    return background

def predict_type(pokemon_img,pokemon):
    if isinstance(pokemon_img,str):
        pokemon_img = Image.open(pokemon_img)
    cart_pokemon = get_pokemon_show(pokemon_img,pokemon)
    img_test = np.array((pokemon_img.resize((128,128))).convert("RGB"))
    img_test = preprocess_input(img_test)
    pokemon_predict = model.predict(np.array([img_test])).round(4)[0]*100
    data_type = pd.DataFrame(zip(classes,pokemon_predict),columns = ["type","proba"])
    data_type.sort_values("proba",ascending=False, ignore_index = True,inplace=True)
    chart_probability = get_proba_plot(data_type)
    result = get_concat_h(cart_pokemon, chart_probability)
    return result

data=pd.read_csv(os.path.join(PATH, "utils/pokedex_(Update_04.21).csv"), index_col="Unnamed: 0")
data["name"].replace("Type: Null","Type_null",inplace=True)
data["type_2"].fillna("No_type",inplace=True)
classes = ['Bug', 'Dark', 'Dragon', 'Electric', 'Fairy', 'Fighting', 'Fire',
           'Flying', 'Ghost', 'Grass', 'Ground', 'Ice', 'No 2nd type', 'Normal',
           'Poison', 'Psychic', 'Rock', 'Steel', 'Water']

# classes = ['bug','dark', 'dragon', 'electric', 'fairy', 'fighting', 'fire', 'flying', 'ghost', 
#            'grass', 'ground', 'ice', 'no 2nd type', 'normal', 'poison', 'psychic', 'rock', 'steel', 'water']

model = load_model(os.path.join( PATH, "utils/pokemon_model.h5"))

print("Model loaded")