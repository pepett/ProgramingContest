window.onload = ()=>{

}
let IsPlayMusic = '';
let Playing = 0;

function PlayMusic(SongURL,PlayBTN){
    if(SongURL == 'None'){
        alert(SongURL);
        return;
    }
    if(IsPlayMusic.src == SongURL){
    if(!IsPlayMusic.paused){
        IsPlayTex(PlayBTN);
        IsPlayMusic.pause();
        console.log('pause')
    }else{
        IsPlayTex(PlayBTN);
        IsPlayMusic.play();
        console.log('play')
        Playing = 1;
    }
    }else{
        if(Playing == 0){
        IsPlayMusic = new Audio(SongURL);
        IsPlayMusic.play();
        IsPlayTex(PlayBTN);
        Playing = 1
        console.log('playnew : '+IsPlayMusic.src);
        }else{
            IsPlayTex(PlayBTN);
            IsPlayMusic.pause();
            console.log('pause')
            Playing = 0;
        }
    }
}
function IsPlayTex(PlayBTN){
    if(PlayBTN.classList == "PlaySongBT"){
        PlayBTN.classList.remove("PlaySongBT");
        PlayBTN.classList.add("StopSongBT");
        PlayBTN.innerHTML = StopBTtex;
    }else{
        PlayBTN.classList.remove("StopSongBT");
        PlayBTN.classList.add("PlaySongBT");
        PlayBTN.innerHTML = PlayBTtex;
    }
};