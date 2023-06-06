import re

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
        '''while True:
            break
            tmp = ver_arr.pop( 0 )
            flg = True
            for i in range( 0, len( ver_arr ) ):
                print( i )
                if tmp == ver_arr[ i ]:
                    flg = False
                    break
            if flg:
                result.append( tmp )
        for i in range( len( arr ) ):
            tmp = arr[ i ]
            flg = True
            for j in range( len( arr ) ):
                if result[ i ] == tmp:
                    flg = False
                    break
            if flg:
                result.append( tmp )
        '''
        return result

    @staticmethod
    def truncate_string(text, max_length):
        if len(text) <= max_length:
            return text
        else:
            return text[:max_length] + "..."