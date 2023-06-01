window.onload = ()=>{
    UserRadioBox = document.getElementsByClassName("UserRadioBox");
    UserFavorite = document.getElementById("UserFavorite");
    UserHistory = document.getElementById("UserHistory");
    UserProFile = document.getElementById("UserProFile");
    checkbox();
}
UserRadioBox = document.getElementsByClassName("UserRadioBox");
UserFavorite = document.getElementById("UserFavorite");
UserHistory = document.getElementById("UserHistory");
UserProFile = document.getElementById("UserProFile");

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
    }
    if(UserRadioBox[1].checked){
        UserFavorite.style.display = 'none';
        UserHistory.style.display = 'block';
        UserProFile.style.display = 'none';
    }
    if(UserRadioBox[2].checked){
        UserFavorite.style.display = 'none';
        UserHistory.style.display = 'none';
        UserProFile.style.display = 'block';
    }
};