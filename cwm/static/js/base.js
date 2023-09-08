window.onload = ()=>{

}

//ボタン
const scroll_to_top_btn = document.querySelector('#scrollBT');

//クリックイベントを追加
scroll_to_top_btn.addEventListener( 'click' , scroll_to_top );

function scroll_to_top(){
	window.scroll({top: 0, behavior: 'smooth'});
};


//スクロール時のイベントを追加
window.addEventListener( 'scroll' , scroll_event );

function scroll_event(){

    //console.log(window.scrollY);
	
	if(window.scrollY > 300){
        scroll_to_top_btn.style.opacity = '1';
        scroll_to_top_btn.style.transform = 'translateY(0px)';
	}else if(window.scrollY < 300){
        scroll_to_top_btn.style.transform = 'translateY(-100px)';
		scroll_to_top_btn.style.opacity = '0';
	}
	
};
//document.getElementById( 'searchBtn' ).onclick = document.querySelector( 'form' ).submit();