$(function() {
    $('#id_new_password').keyup(function(){
        score_password($(this).val());
    });
});
function score_password(password)
{
    var points = new Array();
    points[0] = gettext("Very Weak");
    points[1] = gettext("Weak");
    points[2] = gettext("Better");
    points[3] = gettext("Medium");
    points[4] = gettext("Strong");
    points[5] = gettext("Strongest");
    points[6] = gettext("Password not entered");

    var score   = 0;
    //if password is not entered
    if (password.length == 0){
        score = 6;
    }
    //if password bigger than 6 give 1 point
    if (password.length > 6) score++;

    //if password has both lower and uppercase characters give 1 point  
    if ((password.match(/[a-z]/)) && (password.match(/[A-Z]/))) score++;

    //if password has at least one number give 1 point
    if (password.match(/\d+/)) score++;

    //if password has at least one special caracther give 1 point
    if (password.match(/.[!,@,#,$,%,^,&,*,?,_,~,-,(,)]/))   score++;

    //if password bigger than 12 give another 1 point
    if (password.length > 8) score++;
    //Assign description and meter
    $('#password_description').text('').text(points[score]);
    for (var i=0; i<= 10; i++) {
        $('#password_strength').removeClass("strength" + i);
    }    
    $('#password_strength').addClass("strength" + score);
}
