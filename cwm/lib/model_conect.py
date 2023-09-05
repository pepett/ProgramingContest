from cwmapp.models import HistoryList, LikeList
from lib.spotify_conect import SPOTIFY

class ModelMus:
    @staticmethod
    def setHistory(id):

        Mus = HistoryList.objects.filter(history_userid = id)
        result = []
        
        for i in range(Mus.count()):
            for j in range(Mus.count())[i + 1:]:
                if Mus[i].history_music_id == Mus[j].history_music_id:
                    print('Mus:'+str(i)+':'+str(j))
                    print('music_id:'+Mus[i].history_music_id+':'+Mus[j].history_music_id)
                    Mus[i].delete()
                    break
        
        for i in Mus:
            x = SPOTIFY.track(i.history_music_id)
            result.append(x)

        result.reverse()

        return result

    @staticmethod
    def setLiked(id):

        Mus = LikeList.objects.filter(like_userid = id)
        result = []
        
        for i in range(Mus.count()):
            for j in range(Mus.count())[i + 1:]:
                if Mus[i].like_music_id == Mus[j].like_music_id:
                    print('Mus:'+str(i)+':'+str(j))
                    print('music_id:'+Mus[i].like_music_id+':'+Mus[j].like_music_id)
                    Mus[i].delete()
                    break
        
        for i in Mus:
            x = SPOTIFY.track(i.like_music_id)
            result.append(x)

        result.reverse()

        return result