let play_music = {
    audio: null,//Audio
    is_play: false,//boolean
};

const loading = document.querySelector( '#loading' );

const correct = () => {
    const user_name = document.getElementsByClassName( 'user-name' );
    const comment_text = document.getElementsByClassName( 'comment-text' );
    const comments = document.getElementsByClassName( 'comment-list' )[ 0 ];
    let arr = [];

    const elem = document.createElement( 'div' );
    elem.setAttribute( 'class', 'comment-contents' );
    if( user_name.length == 0 )
        elem.innerHTML = '<h2>コメントはまだありません</h2>';
    for( let i = 0;i < user_name.length;i ++ ){
        console.log( user_name[ i ].innerHTML )
        console.log( comment_text[ i ].innerHTML )
        //elem.append( user_name[ i ] );
        //elem.append( comment_text[ i ] );
    }
    comments.innerHTML = '';
    comments.appendChild( elem );
}

addEventListener( 'DOMContentLoaded', ()=>{
    correct();
} )

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