/*ローディングjsここから*/
const loading = document.querySelector( '#loading' );

let Btns = document.getElementsByClassName('PlaySongBT');
for(let i=0;i < Btns.length;i++){
    console.log(Btns[i].value)
    if(Btns[i].value == 'None'){
        Btns[i].style.display = 'none';
    }
}
 
window.addEventListener( 'load', () => {
  loading.classList.add( 'loaded' );
}, false );
/*ここまで*/