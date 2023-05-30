let play_music = {
    audio: null,//Audio
    is_play: false,//boolean
};


window.onload = () => {
}

const play = ( obj, url ) => {
    if( play_music.audio == null ){
        play_music.audio = new Audio( url );
        play_music.audio.addEventListener("ended", ()=>{
            play_music.is_play = false;
            obj.innerHTML = PlayBTimg;
        });
    }
    if( play_music.is_play ){
        play_music.audio.pause();
        play_music.is_play = false;
        obj.innerHTML = PlayBTimg;
    }else{
        play_music.audio.play();
        play_music.is_play = true;
        obj.innerHTML = StopBTimg;
    }
}