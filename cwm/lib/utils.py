import re
import math
from PIL import Image, ImageDraw, ImageFont
import random,string

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
    def n_dup(arr):
        if len( arr ) == 0:
            return [ { 'tag_name': '', 'tag_num': 0 } ]
        v_arr = arr
        results = []
        while True:#v_arrがなくなるまでループ
            v_arr_first=v_arr.pop(0)#カウントする要素を取得
            v_arr_update=[]#タグを取り除いた配列
            j=1#タグの個数(初期値は1)(ループが回ってる時点で1こは確定である)
            for i in v_arr:
                if i==v_arr_first:#v_arr_firstと元の配列がかぶっているか
                    j+=1#かぶっていたら+1(タグの個数を記録)
                    continue#かぶっていたら追加しない
                v_arr_update.append( i )#まだ重複チェックしてないものを残す
            results.append( { 'tag_name': v_arr_first, 'tag_num': j } )
            v_arr.clear()
            v_arr.extend( v_arr_update )
            if len(v_arr)==0:
                break
        shape_results = sorted( results, key = lambda x: x[ 'tag_num' ], reverse = True )
        return shape_results

    @staticmethod
    def del_duplicate( arr, is_rough ):#タグのかぶりをなくす
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
    def truncate_string(text, max_length):#文字列を指定の長さにする
        if len(text) <= max_length:
            return text
        else:
            return text[:max_length] + "..."
    @staticmethod
    def round( n ):#四捨五入してintにキャストする
        _n, _ = math.modf( n )
        if ( _n * 10 ) > 4.9:
            return int( n ) + 1
        else:
            return int( n )
    
    @staticmethod
    def CreateUserImage(text,uuid):#ユーザの画像作成

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

        filename="images/{}.jpg".format(uuid)
        img.save("media_local/"+filename)

        return filename
    
    @staticmethod
    def randomname(n):
        randlst = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
        return ''.join(randlst)