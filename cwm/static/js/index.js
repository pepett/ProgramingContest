window.onload = ()=>{

}

window.onunload = ( e ) =>{
    const elem = document.getElementsByClassName( 'PlaySongBT' );
    for( let i = 0;i < elem.length;i ++ ){
        stop_display( elem[ i ] );
    }
    music_history = [];
    play_btn_history = [];
}

let music_history = [];
let play_btn_history = [];

const PlayMusic = ( url, btn ) => {
//console.log( url )
    if( url == 'None' ){//プレビューできない場合
        alert( 'この曲は再生できません' )
        return ;
    }
    let history_flg = true;
    for( let i = 0;i < music_history.length;i ++ ){//履歴から参照
        //console.log( music_history[ i ].src + "を参照しました" )
        if( music_history[ i ].src == url ){//履歴にある場合
            if( !music_history[ i ].paused ){
                music_history[ i ].pause();
                //IsPlayTex(btn);
                stop_display( play_btn_history[ i ] );
                //console.log( music_history[ i ].src + "を停止しました" )
            }else{
                music_history[ i ].play();
                //IsPlayTex(btn);
                play_display( play_btn_history[ i ] );
                //console.log( music_history[ i ].src + 'を開始しました' )
            }
            history_flg = false;
        }else{
            //sconsole.log( music_history[ i ].src + "をストップしました" )
            if( !music_history[ i ].paused )
                music_history[ i ].pause();
                //IsPlayTex(btn);
                stop_display( play_btn_history[ i ] );
        }
    }
    if( history_flg ){
        music_history.push( new Audio( url ) );
        play_btn_history.push( btn );
        music_history[ music_history.length - 1 ].play();
        play_display( btn );
        //sIsPlayTex(btn);
        
        //console.log( music_history[ music_history.length - 1] + 'を開始しました_1' )
        
        music_history[music_history.length - 1 ].addEventListener("ended", ()=>{
            //IsPlayTex(btn);
            stop_display( btn );
        });
    }
}

//new
const play_display = ( btn ) => {
    btn.classList.remove("PlaySongBT");
    btn.classList.add("StopSongBT");
    btn.innerHTML = StopBTimg;
}

const stop_display = ( btn ) =>{
    btn.classList.remove("StopSongBT");
    btn.classList.add("PlaySongBT");
    btn.innerHTML = PlayBTimg;
}
/* 
function IsPlayTex(btn){
    if (btn.classList == "PlaySongBT"){
        btn.classList.remove("PlaySongBT");
        btn.classList.add("StopSongBT");
        btn.innerHTML = StopBTimg;
    }else{
        btn.classList.remove("StopSongBT");
        btn.classList.add("PlaySongBT");
        btn.innerHTML = PlayBTimg;
    }
} */
