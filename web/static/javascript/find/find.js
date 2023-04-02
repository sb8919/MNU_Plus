$(document).ready(function() {
    const width = window.innerWidth;
    if (width<1198){
        document.getElementById('screen').style.width='100%';
    }
    else{
        document.getElementById('screen').style.width='90%';
    }
});
