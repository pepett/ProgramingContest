
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
        let nurl =  music_history[ i ].src; 
        if( music_history[ i ].src.indexOf( 'http://localhost:', 0 ) >= 0 ){
            nurl = music_history[ i ].src.replace( /http:\/\/localhost:[0-9]{4}/, "" );
        }
        if( url == nurl ){//履歴にある場合
            //alert(nurl)
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
            if( !music_history[ i ].paused ){

                music_history[ i ].pause();
                //IsPlayTex(btn);
                stop_display( play_btn_history[ i ] );
            }
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

const scrollElement = document.querySelectorAll("#trackbox");

for(let i = 0;i < scrollElement.length;i++){
    scrollElement[i].addEventListener("wheel", (e) => {
    if (Math.abs(e.deltaY) < Math.abs(e.deltaX)) return;
    e.preventDefault();
    //console.log(i)
    scrollElement[i].scrollLeft += e.deltaY;
    });
}

const scrollsongtext = document.querySelectorAll(".ScrollText");
const songnametext = document.querySelectorAll(".SongNameText");

for(let i = 0;i < scrollsongtext.length;i++){
    //console.log(i+" : "+scrollsongtext[i].innerHTML)
    //console.log(i+".clientWidth: "+scrollsongtext[i].clientWidth)
    //console.log(i+".clientWidth: "+songnametext[i].clientWidth)
    if (scrollsongtext[i].clientWidth >= songnametext[0].clientWidth){
        scrollsongtext[i].classList.add("ScrollSongText")
    }
};

const mus_img = document.querySelectorAll(".music_img");
const logo_img = document.querySelectorAll(".Site_Logo");

for(let i = 0;i < mus_img.length;i++){
    //console.log(i+" : "+mus_img[i].id)
    if(mus_img[i].id.length == 25){
        logo_img[i].src = CWM_logo;
        logo_img[i].style.width = '30px';
        logo_img[i].style.height = '30px';
    };
};

const entries = performance.getEntriesByType("navigation");
entries.forEach((entry) => {
  if (entry.type === "back_forward") {
    window.location.reload()
    }
});