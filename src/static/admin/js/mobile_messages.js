var $ = django.jQuery || grp.jQuery;

$().ready(function () {

    function calc_users_count() {

        var data = {
            'id_user': $('#id_user').val(),
            'advisor': $('#id_advisor').val(),
            'status_legal': $('#id_status_legal').val(),
            'user_type': $('#id_user_type').val(),
            'user_status': $('#id_user_status').val(),
            'rank': $('#rank').val(),
            'title': $('#id_title').val(),
            'message': $('#id_message').val(),
        }

        $.ajax({
            url: '/mobile/message/users/count/',
            data: data,
            beforeSend: function() {
                $('#users_count').html('Считаем...');
            },
        }).done(function(data) {
            $(document).on('change', '.this', function() {
                console.log('Element with class "this" has changed');
                console.log('New value is: ' + $(this).val());
            }); 
            $('#users_count').html(data);
        });

    }

    $('#id_user, #id_user_status, #rank').on('select2:select', function (e) {
        calc_users_count();
    });

    $('#id_user, #id_user_status, #rank').on('select2:close', function (e) {
        calc_users_count();
    });

    $('#id_advisor, #status_legal, #id_user_type,\
       #id_title, #id_message').focus(function() {
        calc_users_count();
    });
    $('#id_advisor, #status_legal, #id_user_type,\
       #id_title, #id_message').change(function() {
        calc_users_count();
    });
});
