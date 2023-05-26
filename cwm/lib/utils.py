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
    def truncate_string(text, max_length):
        if len(text) <= max_length:
            return text
        else:
            return text[:max_length] + "..."