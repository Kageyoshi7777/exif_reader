import exifread
import json
from arrays import film_simulation, noise_reduction, grain_effect, \
                   color_chrome_effect, color_chrome_effect_blue, color, \
                   sharp, dynamic_range


def read_image(file_path: str):
    """This function reads image from path and transform its values to be more readable"""
    with open(file_path, 'rb') as image_file:
        tags = exifread.process_file(image_file)

    # take the camera model
    camera = str(tags.pop("Image Model"))

    # create a dictionary of EXIF tags
    keys_to_pop = {"MakerNote Tag 0x1401": "Simulation",
                   "MakerNote Tag 0x1402": "DynamicRangeSetting",
                   "MakerNote Tag 0x1041": "Highlights",
                   "MakerNote Tag 0x1040": "Shadows",
                   "MakerNote Saturation": "Color",
                   "MakerNote Tag 0x100E": "NoiseReduction",
                   "MakerNote Sharpness": "Sharpness",
                   "MakerNote Tag 0x1047": "GrainEffect",
                   "MakerNote Tag 0x1048": "ColorChromeEffect",
                   "MakerNote WhiteBalance": "White Balance",
                   "MakerNote WhiteBalanceFineTune": "White Balance Shift"}
    
    # dict_variable = {key:value for (key,value) in dictonary.items()}
    datas = {value: str(tags.get(key)) for key, value in keys_to_pop.items()}
    datas = {key: str(value) for key, value in datas.items()}
    return datas

# not all cameras does have this parameters
try:
    datas["DynamicRangeSetting2"] = tags.pop("MakerNote Tag 0x1403")
    datas["Kelvin"] = tags.pop("MakerNote ColorTemperature")
    # datas["Clarity"] = tags.pop("MakerNote Tag 0x100F")
    # datas["GrainEffectSize"] = tags.pop("MakerNote Tag 0x104C")
    # datas["ColorChromeFXBlue"] = tags.pop("MakerNote Tag 0x104E")
except KeyError:
    pass


for key in datas:
    datas[key] = str(datas[key])

datas["Simulation"] = film_simulation.get(datas["Simulation"])
datas["NoiseReduction"] = noise_reduction.get(datas["NoiseReduction"])
datas["Highlights"] = round(int(datas["Highlights"]) / -16)
datas["Shadows"] = round(int(datas["Shadows"]) / -16)
datas["GrainEffect"] = grain_effect.get(datas["GrainEffect"])
datas["ColorChromeEffect"] = color_chrome_effect.get(datas["ColorChromeEffect"])
datas["Color"] = color.get(datas["Color"])
datas["White Balance Shift"] = [round(x / 20) for x in json.loads(datas["White Balance Shift"])]
datas["Sharpness"] = sharp.get(datas["Sharpness"].lower())
datas["DynamicRangeSetting"] = dynamic_range.get(datas["DynamicRangeSetting"].lower())
if datas["DynamicRangeSetting"] == "Manual":
    datas["DynamicRangeSetting"] = datas["DynamicRangeSetting2"]
    del datas['DynamicRangeSetting2']
if datas["White Balance"] == "Kelvin":
    datas["White Balance"] = datas["Kelvin"]
    del datas['Kelvin']

# try:
#     datas["ColorChromeFXBlue"] = color_chrome_effect_blue.get(datas["ColorChromeFXBlue"])
# except KeyError:
#     pass

with open("simulations/" + camera + ".json") as json_file:
    simulations = json.load(json_file)

for key in datas:
    datas[key] = str(datas[key])
    print(key, ":", datas[key])


print()
print("---" * 14)
print()
for key in simulations:
    if simulations[key] == datas:
        print(key)
