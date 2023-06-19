window.onload = ()=>{
    UserRadioBox = document.getElementsByClassName("UserRadioBox");
    UserFavorite = document.getElementById("UserFavorite");
    UserHistory = document.getElementById("UserHistory");
    UserProFile = document.getElementById("UserProFile");
    FavLabel = document.getElementById("FavLabel");
    HisLabel = document.getElementById("HisLabel");
    SetLabel = document.getElementById("SetLabel");
    checkbox();
}

const input_file = document.getElementById("id_image");
input_file.addEventListener("change", function (e) {
  const file = e.target.files[0];//複数ファイルはfiles配列をループで回す
  const reader = new FileReader();
  const image = document.getElementById("NewUserIcon");
  reader.addEventListener("load", function () {
    image.src = reader.result;
  }, false);

  if (file) {
    reader.readAsDataURL(file);
  }
})

textColor = "#00de64";
textColor2 = "#ffffff";

UserRadioBox = document.getElementsByClassName("UserRadioBox");
UserFavorite = document.getElementById("UserFavorite");
UserHistory = document.getElementById("UserHistory");
UserProFile = document.getElementById("UserProFile");
FavLabel = document.getElementById("FavLabel");
HisLabel = document.getElementById("HisLabel");
SetLabel = document.getElementById("SetLabel");

UserRadioBox[0].addEventListener('click', () =>{
    checkbox();
});
UserRadioBox[1].addEventListener('click', () =>{
    checkbox();
});
UserRadioBox[2].addEventListener('click', () =>{
    checkbox();
});

function checkbox(){
    if(UserRadioBox[0].checked){
        UserFavorite.style.display = 'block';
        UserHistory.style.display = 'none';
        UserProFile.style.display = 'none';
        FavLabel.style.color = textColor;
        HisLabel.style.color = textColor2;
        SetLabel.style.color = textColor2;
    }
    if(UserRadioBox[1].checked){
        UserFavorite.style.display = 'none';
        UserHistory.style.display = 'block';
        UserProFile.style.display = 'none';
        FavLabel.style.color = textColor2;
        HisLabel.style.color = textColor;
        SetLabel.style.color = textColor2;
    }
    if(UserRadioBox[2].checked){
        UserFavorite.style.display = 'none';
        UserHistory.style.display = 'none';
        UserProFile.style.display = 'block';
        FavLabel.style.color = textColor2;
        HisLabel.style.color = textColor2;
        SetLabel.style.color = textColor;
    }
};