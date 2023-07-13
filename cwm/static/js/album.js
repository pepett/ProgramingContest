
window.onload = ()=>{

}

const albumsongs = document.getElementsByClassName( 'PlaySongBT' );
const albumbox = document.getElementsByClassName( 'albumbox' );


for( let i = 0;i < albumsongs.length;i++){
    if (albumsongs[i].value == 'None'){
        let alertbox = document.createElement('span');
        alertbox.textContent = 'プレビュー再生が出来ない曲です';
        alertbox.className = 'alertbox';

        console.log('Value == None');
        console.log(i);
        albumbox[i].appendChild(alertbox)
    }
}