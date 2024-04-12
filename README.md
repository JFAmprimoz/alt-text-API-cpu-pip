# Alt Text API - CPU only version
Alt Text API CPU-only is a REST API that accepts image URLs, files, or base64 strings and responds with a caption. It runs a pretrained Salesforce/blip2-opt-2.7b.

## System Requirements and Download Size
### Memory
To be able to caption images in a reasonable time frame (2-3 seconds) please use a system with at least 16GB of RAM (32GB if you are using Windows Subsystem for Linux as WSL only has access to half of the total system RAM). The model takes about 8 GB of RAM so the requirement is probably somewhere between 8-16, but we've only tested at 8 and 16. Where there isn't enough memory to load the whole model ontop of other system requirements, the time to process an image will extend to 15 seconds and beyond.

### Download Size
 **WARNING:**  The first time you run the program it will download the full sized model, **aproximately 15 GB.** Keep this in mind if using a metered connection. The model will be cached on your drive, and future runs of the program will not require the download again.

## Installation
1. Create and activate an environment with python 3.11.8
2. Clone this repo and cd into it
3. Use `pip install -r requirements.txt` to import required packages.
4. Run the server: `$ uvicorn main:app`

## Usage
Go to (http://localhost:8000/docs) for API documentation on how to structure requests. You can also test the API from that URL by clicking on a title to expand the section, then clicking "Try it out".

### From the Model Providers
#### Bias, Risks, Limitations, and Ethical Considerations
BLIP2-OPT uses off-the-shelf OPT as the language model. It inherits the same risks and limitations as mentioned in Meta's model card.

Like other large language models for which the diversity (or lack thereof) of training data induces downstream impact on the quality of our model, OPT-175B has limitations in terms of bias and safety. OPT-175B can also have quality issues in terms of generation diversity and hallucination. In general, OPT-175B is not immune from the plethora of issues that plague modern large language models.

BLIP2 is fine-tuned on image-text datasets (e.g. LAION ) collected from the internet. As a result the model itself is potentially vulnerable to generating equivalently inappropriate content or replicating inherent biases in the underlying data.

BLIP2 has not been tested in real world applications. It should not be directly deployed in any applications. Researchers should first carefully assess the safety and fairness of the model in relation to the specific context they’re being deployed within.

## Thanks
Heartfelt thanks to [Nickolas Kenyeres](https://github.com/knicklabs) and [Tolga Balci](https://github.com/tolga-balci) for recommendations, testing, and feedback. 
