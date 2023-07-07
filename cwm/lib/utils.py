import re
import math
from PIL import Image, ImageDraw, ImageFont
import random

class Utils:
    @staticmethod
    def sharp( text ):
        index = text.split( '#' )
        result = []
        index.pop( 0 )
        for t in index:
            tmp = t.split()
            result.append( tmp[ 0 ] )
        
        return result
    
    @staticmethod
    def del_duplicate( arr, is_rough ):
        ver_arr = arr
        result = []
        num = []
        for i in range( len( arr ) ):
            flg = True
            text = ver_arr[ i ]
            for j in range( len( result ) ):
                if text == result[ j ]:
                    flg = False
                    break
            if flg:
                result.append( text )
        return result

    @staticmethod
    def truncate_string(text, max_length):
        if len(text) <= max_length:
            return text
        else:
            return text[:max_length] + "..."
    @staticmethod
    def round( n ):
        _n, _ = math.modf( n )
        if ( _n * 10 ) > 4.9:
            return int( n ) + 1
        else:
            return int( n )
    
    @staticmethod
    def CreateUserImage(text):

        img_size = (500,500)
        img_color = (int(random.uniform(100,255)),int(random.uniform(100,255)),int(random.uniform(100,255)))
        text_color = (255,255,255)
        fontsize = 200
        ttfontname = "../static/font/meiryob.ttc"

        img = Image.new('RGB', img_size,img_color)
        draw = ImageDraw.Draw(img)


        font = ImageFont.truetype(ttfontname, fontsize)
        textWidth, textHeight = draw.textsize(text[0],font)
        img_w,img_h = img.size
        x = ((img_w - textWidth)/2)
        y = (img_h - (img_h - textHeight/2))
        print(img_w,img_h)
        print(textHeight,textWidth)
        print((x,y))
        draw.text((x,y), text[0], fill=text_color, font=font)

        filename="images/{}.jpg".format(text)
        img.save("media_local/"+filename)

        return filename