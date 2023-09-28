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

for( let i = 0;i < document.getElementsByClassName( 'edit-btn' ).length;i ++ ){
    document.getElementsByClassName( 'edit-btn' )[ i ].addEventListener( 'click', ( e ) => {
        const obj = document.getElementsByClassName( 'edit-form' )[i];
        // alert( i )
        if( obj.style.display == 'none' ){
            obj.style.display = 'block';
            e.target.value = 'キャンセル';
        }else{
            obj.style.display = 'none';
            e.target.value = '編集';
        }
    }, false );
}

/*
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
}*/

//textareaの高さ自動設定
window.addEventListener( 'DOMContentLoaded', () => {
    const rts = document.querySelectorAll( '.reply-text' );
    rts.forEach( (rt) => {
        rt.setAttribute( 'style', `height: ${ rt.scrollHeight / 2 }px;` );
        rt.addEventListener( 'input', setTextareaHeight );
    });
    function setTextareaHeight(){
        const tmp = this.value
        if( tmp.split( /\r*\n/ ).length == 1 ){
            this.style.height = 'auto';
            this.style.height = `${ this.scrollHeight / 2 }px`;
            return ;
        }
        this.style.height = 'auto';
        this.style.height = `${ this.scrollHeight }px`;
    }
    
} );



for(let i = 0;i < document.getElementsByClassName('reply-text').length;i++){
    document.getElementsByClassName('reply-text')[i].addEventListener("keyup", (e) =>{
        if (document.getElementsByClassName('reply-text')[i].value == ""){//編集不可
            document.getElementsByClassName( 'reply-submit' )[ i ].classList.remove( 'hover-reply-submit' );
            document.getElementsByClassName('reply-submit')[i].classList.add('replyBT_off');
            document.getElementsByClassName('reply-submit')[i].disabled = true;
        }else{//編集可
            document.getElementsByClassName( 'reply-submit' )[ i ].classList.add( 'hover-reply-submit' );
            document.getElementsByClassName('reply-submit')[i].classList.remove('replyBT_off');
            document.getElementsByClassName('reply-submit')[i].disabled = false;
        }
    });
}

const modal = document.querySelector('.js-modal'); // layer要素に付与したjs-modalクラスを取得し変数に格納
const modalButton = document.querySelector('#firstdeleteBT'); // button要素に付与した1st_deleteBTクラスを取得し、変数に格納

// モーダルボタンをクリックしたときのイベントを登録
modalButton.addEventListener('click', () => {
  modal.classList.add('is-open');
});

const modalClose = document.querySelector('#NotdeleteBT');　// xボタンのjs-close-buttonを取得し変数に格納

modalButton.addEventListener('click', () => {
  modal.classList.add('is-open');
});

modalClose.addEventListener('click', () => { // xボタンをクリックしたときのイベントを登録
  modal.classList.remove('is-open'); 
});