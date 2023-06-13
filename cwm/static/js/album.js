import PreviewMusic from './lib/utils.js';

addEventListener( 'DOMContentLoaded', ()=>{
    const preview_class = document.getElementsByClassName( 'preview' );
    let previews = [];
    for( let i = 0;i < preview_class.length;i ++){
        previews.push( new PreviewMusic( preview_class[ i ].dataset.preview, '.preview > button > img', i ) );
        preview_class[ i ].addEventListener( 'click', ( e )=>{
            for( let j = 0;j < previews.length;j ++ ){
                if( i == j ){//押した音楽を操作
                    if( previews[ i ].is_play ){
                        previews[ i ].stop();
                    }else{
                        previews[ i ].play();
                    }
                }else{
                    if( previews[ j ].is_play ){//他の音楽が再生中か
                        previews[ j ].stop();
                    }
                }
            }
        } )
    }
} )
