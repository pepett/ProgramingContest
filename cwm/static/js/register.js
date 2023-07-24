window.onload = ()=>{

}

let pass = document.getElementById( 'id_password' );
let passcheck = document.getElementById( 'id_passwordcheck' );
let btnEye = document.getElementById( 'PassLook' );

let flg = 0;

minval = 6;
mintext = '文字数が'+minval+'文字以下です。';
notsametext = 'パスワードが一致していません。';

pass.addEventListener("keyup", ( e ) => {
    if(passcheck.value){
        if(pass.value.length < minval){
            passON(mintext);
        }else if (pass.value != passcheck.value){
            passON(notsametext);
            checkON(notsametext);
        }else{
            document.querySelector('.new').className = 'PassAlert new';
            document.querySelector('.newcheck').className = 'PassAlert newcheck';
        }
    }else{
        if(pass.value.length <= minval){
            passON(mintext);
        }else{
            document.querySelector('.new').className = 'PassAlert new';
        }
    }
});

passcheck.addEventListener("keyup", ( e ) => {
    if (pass.value){
        if (pass.value == passcheck.value & pass.value.length == passcheck.value.length){
            if (passcheck.value.length > minval){
                document.querySelector('.newcheck').className = 'PassAlert newcheck';
                document.querySelector('.new').className = 'PassAlert new';
            }else{
                checkON(mintext);
            }
        }else{
            checkON(notsametext);
        }
    }else{
        passON('パスワードを入力してください');
    }
    if(!passcheck.value){
        checkON('パスワードを入力してください');
    }
});

function passON(text){
    document.querySelector('.new').innerHTML = text;
    document.querySelector('.new').classList.add('PassOn');
    document.querySelector('.new').classList.remove('PassOff');
}

function checkON(text){
    document.querySelector('.newcheck').innerHTML = text;
    document.querySelector('.newcheck').classList.add('PassOn');
    document.querySelector('.newcheck').classList.remove('PassOff');
}

function PassLook(){
    if (pass.type == "text") {
        pass.type = "password";
        btnEye.innerHTML = eye_opentex;
    }else{
        pass.type = "text";
        btnEye.innerHTML = eye_closetex;
    }
}