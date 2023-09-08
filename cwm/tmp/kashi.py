
import lyricsgenius
 
token = 'G8LsaiLh6YFWz0i7l9NPe1XyXrJaG0-3OpluWBbeuvUXxA_MlnAm1HIbQSI9kF26'

genius = lyricsgenius.Genius(token)

song = genius.search_song("ELLEGARDEN Red Hot")
if not song == None:
	print( '----------' )
	print(str( song.lyrics ))
	print( '----------' )