let play_music = {
    audio: null,//Audio
    is_play: false,//boolean
};

const correct = () => {
    let user_name = document.getElementsByClassName( 'user-name' );
    let comment_text = document.getElementsByClassName( 'comment-text' );
    let delete_form = document.getElementsByClassName( 'delete-form' );
    let id = document.getElementsByClassName( 'id' );
    const comments = document.getElementsByClassName( 'comment-list' )[ 0 ];

    const elem = document.createElement( 'div' );
    elem.setAttribute( 'class', 'comment-contents' );
    if( user_name.length == 0 )
        elem.innerHTML = '<h2>コメントはまだありません</h2>';
    for( let i = 0;i < user_name.length;i ++ ){
        elem.innerHTML += user_name[ i ].outerHTML;
        elem.innerHTML += comment_text[ i ].outerHTML;
        if( delete_form.length == 0 ){
            continue;
        }else{
            delete_form[ i ].appendChild( id[ i ] );
            elem.innerHTML += delete_form[ i ].outerHTML;
        }
    }
    
    comments.innerHTML = '';
    comments.appendChild( elem );
}

addEventListener( 'DOMContentLoaded', ()=>{
    //correct();
} )

for( let i = 0;i < document.getElementsByClassName( 'edit-btn' ).length;i ++ ){
    document.getElementsByClassName( 'edit-btn' )[ i ].addEventListener( 'click', ( e ) => {
        const obj = document.getElementsByClassName( 'edit-form' )[ i ];
        if( obj.style.display == 'none' ){
            obj.style.display = 'block';
            e.target.value = 'キャンセル';
        }else{
            obj.style.display = 'none';
            e.target.value = '編集';
        }
    }, false );
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