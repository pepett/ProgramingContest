window.onload = ()=>{

}
let IsPlayMusic = '';
let Playing = 0;

function PlayMusic(SongURL){
    if(SongURL == 'None'){
        alert(SongURL);
        return;
    }
    if(IsPlayMusic.src == SongURL){
    if(!IsPlayMusic.paused){
        IsPlayMusic.pause();
        console.log('pause')
    }else{
        IsPlayMusic.play();
        console.log('play')
        Playing = 1;
    }
    }else{
        if(Playing == 0){
        IsPlayMusic = new Audio(SongURL);
        IsPlayMusic.play();
        Playing = 1
        console.log('playnew : '+IsPlayMusic.src);
        }else{
            IsPlayMusic.pause();
            console.log('pause')
            Playing = 0;
        }
    }
}
function IsPlayTex(PlayBTN){
    console.log(PlayBTN.classList);
    if(PlayBTN.classList == "PlaySongBT"){
        PlayBTN.classList.remove("PlaySongBT");
        PlayBTN.classList.add("StopSongBT");
    }else{
        PlayBTN.classList.remove("StopSongBT");
        PlayBTN.classList.add("PlaySongBT");
    }
};