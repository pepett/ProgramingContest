let play_music = {
    audio: null,//Audio
    is_play: false,//boolean
};

const loading = document.querySelector( '#loading' );

const correct = () => {
    let user_name = document.getElementsByClassName( 'user-name' );
    let comment_text = document.getElementsByClassName( 'comment-text' );
    const comments = document.getElementsByClassName( 'comment-list' )[ 0 ];

    const elem = document.createElement( 'div' );
    elem.setAttribute( 'class', 'comment-contents' );
    if( user_name.length == 0 )
        elem.innerHTML = '<h2>コメントはまだありません</h2>';
    for( let i = 0;i < user_name.length;i ++ ){
        console.log( user_name[ i ].innerHTML )
        console.log( comment_text[ i ].innerHTML )
        elem.innerHTML += user_name[ i ].outerHTML;
        elem.innerHTML += comment_text[ i ].outerHTML;
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