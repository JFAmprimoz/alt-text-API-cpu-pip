import base64
from typing import Annotated, IO
from io import BytesIO
import requests
from fastapi import Body, FastAPI, File
from PIL import Image
import torch
from transformers import Blip2Processor, Blip2ForConditionalGeneration


processor = model = None

def prepare_model(model_path):
    global processor, model
    
    processor = Blip2Processor.from_pretrained(model_path)
    model = Blip2ForConditionalGeneration.from_pretrained(model_path
                                                      , torch_dtype=torch.bfloat16
                                                     )
    model = torch.compile(model)

    return processor, model

def image_closed(im):
    try:
        im.load()
    except ValueError:
        return "yes"
    return "no"

def image_from_url(img_url:str):
    
    return Image.open(requests.get(img_url, stream=True).raw)

def image_from_file(img_file:IO):
 
    return Image.open(BytesIO(img_file))

def image_from_base64(base64_string:str):
    img_file = base64.b64decode(base64_string)
 
    return Image.open(BytesIO(img_file))


def caption_image(image: IO, cap_processor: object, cap_model: object):
    raw_image = image.convert('RGB')
    inputs = cap_processor(raw_image, return_tensors="pt").to(torch.float16)
    out = cap_model.generate(**inputs, max_new_tokens=20)

    caption_txt = cap_processor.decode(out[0], skip_special_tokens=True)

    return caption_txt

prepare_model('Salesforce/blip2-opt-2.7b')

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.post("/caption-url/")
async def caption_url(img_url: Annotated[str, Body(embed=True)]):
    image = image_from_url(img_url)
    caption = caption_image(image, processor, model)
    image.close()
    image_closed_explicit = image_closed(image)
    
    return {"Img URL":img_url
            , "Caption": caption
            , "close explicit": image_closed_explicit
            }

@app.post("/caption-file/")
async def caption_file(img_file: bytes = File(...)):
    image = image_from_file(img_file)
    caption = caption_image(image, processor, model)
    image.close()
    image_closed_explicit = image_closed(image)
    
    return {"Caption": caption
            , "close explicit": image_closed_explicit
            }

@app.post("/encode-base64/")
async def encode_file(img_file: bytes = File(...)):
    base64_string = base64.b64encode(img_file).decode('utf-8')
    
    return {"Base64 String": base64_string
            }

@app.post("/caption-base64/")
async def caption_base64(base64_string: Annotated[str, Body(embed=True)]):
    image = image_from_base64(base64_string)
    caption = caption_image(image, processor, model)
    image.close()
    image_closed_explicit = image_closed(image)
    
    return {"Caption": caption
            , "close explicit": image_closed_explicit
            }