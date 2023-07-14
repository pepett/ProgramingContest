window.onload = ()=>{

}

let oldpass = document.getElementById( 'oldpassword' );
let oldpasscheck = document.getElementById( 'oldpasswordcheck' );

let newpass = document.getElementById( 'newpassword' );
let newpasscheck = document.getElementById( 'newpasswordcheck' );

SetNewPass();

let flg = 0;

minval = 8;
mintext = '文字数が'+minval+'文字以下です。';
notsametext = 'パスワードが一致していません。';
sametext2 = '現在のパスワードと新しいパスワードが同じです。'

oldpass.addEventListener("keyup", ( e ) => {
    if(oldpass.value == oldpasscheck.value){
        if(oldpass.value != newpass.value){
            document.querySelector('.old').className = 'PassAlert old PassOff';
            SetNewPass();
            document.querySelector('.oldcheck').className = 'PassAlert oldcheck PassOff';
            SetNewPass();
        }else{
            oldpassON(sametext2)
        }
    }else{
        oldpassON(notsametext);
    }
});

oldpasscheck.addEventListener("keyup", ( e ) => {
    if (oldpasscheck.value == oldpass.value){
        document.querySelector('.oldcheck').className = 'PassAlert oldcheck PassOff';
        SetNewPass();
        document.querySelector('.old').className = 'PassAlert old PassOff';
        SetNewPass();
    }else{
        oldcheckON(notsametext);
    }
});

newpass.addEventListener("keyup", ( e ) => {
    if (newpass.value.length > minval){//新しいパスワードがminval以上
        if (newpass.value == oldpass.value){//新しいパスワードが前のパスワードと同じ
            newpassON(sametext2)
        }else{
            document.querySelector('.new').className = 'PassAlert new PassOff';
            SetNewPass();
        }
    }else{
        newpassON(mintext);
    }
});

newpasscheck.addEventListener("keyup", ( e ) => {
    if (newpasscheck.value == newpass.value){
        if (newpass.value.length > minval){
            document.querySelector('.newcheck').className = 'PassAlert newcheck PassOff';
            SetNewPass();
            document.querySelector('.new').className = 'PassAlert new PassOff';
            SetNewPass();
        }else if(newpass.value == oldpass.value){
            newcheckON(sametext2);
        }else{
            newcheckON(notsametext);
        }
    }else{
        newcheckON(notsametext);
    }
});

function SetNewPass(){
    subBT =  document.querySelector('#submit');
    console.log(document.getElementsByClassName('PassOff').length);
    if (document.getElementsByClassName('PassOff').length == 4){
        subBT.classList.remove('submit_off');
        subBT.disabled = false;
    }else{
        subBT.classList.add('submit_off');
        subBT.disabled = true;
    }
}

function oldpassON(text){
    document.querySelector('.old').innerHTML = text;
    document.querySelector('.old').classList.add('PassOn');
    document.querySelector('.old').classList.remove('PassOff');
    SetNewPass();
}

function oldcheckON(text){
    document.querySelector('.oldcheck').innerHTML = text;
    document.querySelector('.oldcheck').classList.add('PassOn');
    document.querySelector('.oldcheck').classList.remove('PassOff');
    SetNewPass();
}

function newpassON(text){
    document.querySelector('.new').innerHTML = text;
    document.querySelector('.new').classList.add('PassOn');
    document.querySelector('.new').classList.remove('PassOff');
    SetNewPass();
}

function newcheckON(text){
    document.querySelector('.newcheck').innerHTML = text;
    document.querySelector('.newcheck').classList.add('PassOn');
    document.querySelector('.newcheck').classList.remove('PassOff');
    SetNewPass();
}