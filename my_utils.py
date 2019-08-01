import PIL.Image
import os
import json
import re
import xml.etree.ElementTree as et
import pdb

def parse_xml_bbox(filename):
    tree = et.parse(filename)
    root = tree.getroot()
    #pdb.set_trace()
    if root[2].tag == "path":
        xmin = int(root[6][4][0].text)
        ymin = int(root[6][4][1].text)
        xmax = int(root[6][4][2].text)
        ymax = int(root[6][4][3].text)
    else:
        xmin = int(root[5][4][0].text)
        ymin = int(root[5][4][1].text)
        xmax = int(root[5][4][2].text)
        ymax = int(root[5][4][3].text)
    
    scale = max(xmax - xmin, ymax - ymin) / 200
    center = ((xmin+xmax)/2 , (ymin+ymax)/2)
    return scale, center

def my_crop(filename, data):
    #pdb.set_trace()
    image_pil = PIL.Image.open(filename)
    if 'crop_rect' in data.keys() and data['crop_rect'] is not None:  # Now, it doesn't works
        bbox = data['crop_rect']
    else:   
        prefix = os.path.splitext(filename)[0]
        #idx = int(re.findall(r"\d+", filename)[1])  # bcz dir have 0
        xml_file = prefix + ".xml"
        _, center = parse_xml_bbox(xml_file)
        xmin = max(center[0]-200, 0)
        ymin = max(center[1]-200, 0)
        xmax = min(center[0]+200, 1280)
        ymax = min(center[1]+200, 720)
        bbox = [xmin, ymin, xmax, ymax]
    output_image = image_pil.crop((xmin, ymin, xmax, ymax))
    return output_image, bbox

if __name__ == "__main__":
    filename = "D:/0test/1.jpg"
    filename2 = "D:/0test/1.json"
    with open(filename2, 'rb') as f:
        data = json.load(f)
    image, bbox = my_crop(filename, data)
    image.show()