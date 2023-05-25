window.onload = ()=>{

}
let music_history = [];

const PlayMusic = ( url, btn )=>{
    if( url == 'None' ){//プレビューできない場合
        alert( 'この曲は再生できません' )
        return ;
    }
    let history_flg = true;
    for( let i = 0;i < music_history.length;i ++ ){//履歴から参照
        console.log( music_history[ i ].src + "を参照しました" )
        if( music_history[ i ].src == url ){//履歴にある場合
            if( !music_history[ i ].paused ){
                music_history[ i ].pause();
                IsPlayTex(btn);
                console.log( music_history[ i ].src + "を停止しました" )
            }else{
                music_history[ i ].play();
                IsPlayTex(btn);
                console.log( music_history[ i ].src + 'を開始しました' )
            }
            history_flg = false;
        }else{
            console.log( music_history[ i ].src + "をストップしました" )
            if( !music_history[ i ].paused )
                music_history[ i ].pause();
                IsPlayTex(btn);
        }
    }
    if( history_flg ){
        music_history.push( new Audio( url ) );
        music_history[ music_history.length - 1 ].play();
        console.log( music_history[ music_history.length - 1] + 'を開始しました_1' )
        IsPlayTex(btn);
        music_history[music_history.length - 1 ].addEventListener("ended", ()=>{
            IsPlayTex(btn);
          });
    }
}

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
};