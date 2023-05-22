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