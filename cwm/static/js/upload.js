window.onload = ()=>{
  const Albums = document.getElementsByClassName("album_radio");
  let SelectAlbum = document.getElementsByName("SelectAlbum");
  for(let j = 0;j < Albums.length;j++){
    if (SelectAlbum[j].checked == true){
      console.log('add')
      Albums[j].classList.add('album_radio_select');
    }else{
      console.log('remove')
      Albums[j].classList.remove('album_radio_select');
    }
  }
  let album_name = document.getElementsByName("album_name");
  let album_image = document.getElementsByName("album_image");
  album_image[0].required = true;
  album_name[0].required = false;
  album_name[0].disabled = true;
  album_name[0].style.display = "none"
  IconBox.style.display = "flex"
}

const full_input_file = document.getElementById("id_music_track_full");
full_input_file.addEventListener("change", function (e) {
  console.log(full_input_file);
  const file = e.target.files[0];//複数ファイルはfiles配列をループで回す
  const FilenameText = document.getElementById("full_filename");
  const NewFilename = file.name.split('.');
  const reader = new FileReader();
  const full_audio = document.getElementById("full_prebox");
  reader.addEventListener("load", function () {
    let song = document.createElement('audio');
        song.controls = true;
        song.src = reader.result;
        song.type = "audio/"+NewFilename[1];
        song.loop = true;

    if(full_audio.childElementCount){
        full_audio.innerHTML = "";
        full_audio.appendChild(song);
    }else{
        full_audio.appendChild(song);
    }
    FilenameText.innerHTML = omittedContent(NewFilename[0])+"."+NewFilename[1];

  }, false);

  if (file) {
    reader.readAsDataURL(file);
  }
})

const pre_input_file = document.getElementById("id_music_track_preview");
pre_input_file.addEventListener("change", function (e) {
  console.log(pre_input_file);
  const file = e.target.files[0];//複数ファイルはfiles配列をループで回す
  const FilenameText = document.getElementById("pre_filename");
  const NewFilename = file.name.split('.');
  const reader = new FileReader();
  const pre_audio = document.getElementById("pre_prebox");
  reader.addEventListener("load", function () {
    let song = document.createElement('audio');
        song.controls = true;
        song.src = reader.result;
        song.type = "audio/"+NewFilename[1];
        song.loop = true;

    if(pre_audio.childElementCount){
        pre_audio.innerHTML = "";
        pre_audio.appendChild(song);
    }else{
        pre_audio.appendChild(song);
    }
    FilenameText.innerHTML = omittedContent(NewFilename[0])+"."+NewFilename[1];

  }, false);

  if (file) {
    reader.readAsDataURL(file);
  }
})

const album_input_file = document.getElementById("id_album_image");
album_input_file.addEventListener("change", function (e) {
  console.log(album_input_file);
  const file = e.target.files[0];//複数ファイルはfiles配列をループで回す
  const FilenameText = document.getElementById("FilenameText");
  const NewFilename = file.name.split('.');
  const reader = new FileReader();
  const image = document.getElementById("AlbumIcon");
  reader.addEventListener("load", function () {
    image.src = reader.result;
    FilenameText.innerHTML = omittedContent(NewFilename[0])+"."+NewFilename[1];
  }, false);
  if (file) {
    reader.readAsDataURL(file);
  }
})

const Albums = document.getElementsByClassName("album_radio");
const IconBox = document.getElementById("IconBox");

for (let i = 0;i < Albums.length;i++){
  Albums[i].addEventListener("click", function (e) {
    let SelectAlbum = document.getElementsByName("SelectAlbum");
    for(let j = 0;j < Albums.length;j++){
      if (SelectAlbum[j].checked == true){
        console.log('add')
        Albums[j].classList.add('album_radio_select');
      }else{
        console.log('remove')
        Albums[j].classList.remove('album_radio_select');
      }
    }
    let album_name = document.getElementsByName("album_name");
    let album_image = document.getElementsByName("album_image");
    if (SelectAlbum[i].value == 'Single'){
      album_image[0].required = true;
      album_name[0].required = false;
      album_name[0].disabled = true;
      album_name[0].style.display = "none"
      IconBox.style.display = "flex"
    }else if (SelectAlbum[i].value == 'MakeAlbum'){
      album_image[0].required = true;
      album_name[0].required = true;
      album_name[0].disabled = false;
      album_name[0].style.display = "block"
      IconBox.style.display = "flex"
    }else{
      album_image[0].required = false;
      album_name[0].required = false;
      album_name[0].disabled = false;
      IconBox.style.display = "none"
    }
  });
}