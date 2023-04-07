var password = document.getElementById('password');
var passwordConfirm = document.getElementById('confirm_password');
var confirmMsg = document.getElementById('same');
document.getElementById('circle_sign_btn').setAttribute('disabled', true);
function passConfirm() {
    if (password.value == passwordConfirm.value) {
        confirmMsg.innerHTML = "비밀번호가 일치합니다.";
        document.getElementById('confirm_password').className = 'form-control input-md is-valid';
    } else {
        document.getElementById('circle_sign_btn').setAttribute('disabled', true);
        confirmMsg.innerHTML = "비밀번호 불일치합니다.";
        document.getElementById('confirm_password').className = 'form-control input-md is-invalid';
    }
}

function complete() {
    alert('동아리 등록신청이 완료됐습니다.');
}

function passSign() {
    var team_agree = document.getElementById('team_agree').checked;
    if (team_agree == true && password.value == passwordConfirm.value) {
        document.getElementById('circle_sign_btn').removeAttribute('disabled');
    } else {
        document.getElementById('circle_sign_btn').setAttribute('disabled', true);
    }
}
function id_duplicate_check() {
    var check_id = document.getElementById('id').value;
    var result = $.post("circle/manage/id_check", { id: check_id }, function (id_result) {
        if (id_result.id == 1) 
        {
            alert('중복된 아이디입니다!');
            document.getElementById('circle_sign_btn').setAttribute('disabled', true);
            document.getElementById('id').className = 'form-control input-md is-invalid';
        } else 
        { 
            alert('아이디를 사용할 수 있습니다!');
            document.getElementById('id').className = 'form-control input-md is-valid';
        }
    })
}