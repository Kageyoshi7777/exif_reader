import exifread
import json
from arrays import film_simulation, noise_reduction, grain_effect, \
                   color_chrome_effect, color_chrome_effect_blue, color, \
                   sharp, dynamic_range

f = open("images/jeff.JPG", 'rb')

tags = exifread.process_file(f)


for tag in tags.keys():
    if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
        print ("Key: %s, value %s" % (tag, tags[tag]))