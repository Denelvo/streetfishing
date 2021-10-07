
import exifread
# Open image file for reading (binary mode)
f = open('333_IMG_20211003_155620.jpeg', 'rb')
# Return Exif tags
tags = exifread.process_file(f)

for tag in tags.keys():
    if tag in ('Image DateTime', 'GPS GPSLongitudeRef', 'GPS GPSLatitude', 'GPSLongitudeRef', 'GPS GPSLongitude'):
        print("Key: %s, value %s" % (tag, tags[tag]))
