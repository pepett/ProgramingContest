/*
    
*/

class PreviewMusic{
    
    constructor( preview_url, img_class, img_num ){
        this.preview_url = preview_url;
        this.img_class = img_class;
        this.img_num = img_num;
        this.is_play = false;
        this.audio = new Audio( preview_url );
    }
    play(){
        this.audio.play();
        document.querySelectorAll( this.img_class )[ this.img_num ].src = '/static/img/tmp/stop.png';
        this.is_play = true;
    }
    stop(){
        this.audio.pause();
        document.querySelectorAll( this.img_class )[ this.img_num ].src = '/static/img/tmp/play_green.png';
        this.is_play = false;
    }
}