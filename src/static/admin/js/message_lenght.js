var $ = django.jQuery || grp.jQuery;

$().ready(function () {

    function calc_message_lenght() {
            
            $('#symb_count').html('Набрано ' + $("#id_message").val().length + " символов");
    }
    $('#id_message').keyup(function() {
        calc_message_lenght();
        if ($("#id_title").val().length > 0 && $("#id_message").val().length > 0) {
            $('#send_message').prop('disabled', false);
        }
        else {
            $('#send_message').prop('disabled', true);
        }
    });
    $('#id_title').keyup(function() {
        if ($("#id_title").val().length > 0 && $("#id_message").val().length > 0) {
            $('#send_message').prop('disabled', false);
        }
        else {
            $('#send_message').prop('disabled', true);
        }
    });
});
