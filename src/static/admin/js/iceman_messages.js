var $ = django.jQuery || grp.jQuery;

$().ready(function () {

    function calc_users_count() {

        var data = {
            'id_user': $('#id_user').val(),
            'advisor': $('#id_advisor').val(),
            'status_legal': $('#id_status_legal').val(),
            'user_type': $('#id_user_type').val(),
            'iceman_status': $('#id_iceman_status').val(),
            'region': $('#id_region').val(),
            'last_order_date': $('#id_last_order_date').val(),
            'is_overdue': $('#id_is_overdue').val(),
            'title': $('#id_title').val(),
            'message': $('#id_message').val(),
        }

        $.ajax({
            url: '/iceman/message/users/count/',
            data: data,
            beforeSend: function() {
                $('#users_count').html('Считаем...');
            },
        }).done(function(data) {
            $('#users_count').html(data);
        });

    }

    $('#id_user, #id_iceman_status, #id_region').on('select2:select', function () {
        calc_users_count();
    }).on('select2:close', function () {
        calc_users_count();
    });

    $('#id_user, #id_advisor, #status_legal, #id_user_type, #id_iceman_status, #id_regions,\
       #id_last_order_date, #id_is_overdue, #id_title, #id_message').focus(function() {
           calc_users_count();
    });
    $('#id_user, #id_advisor, #status_legal, #id_user_type, #id_iceman_status, #id_regions,\
       #id_last_order_date, #id_is_overdue, #id_title, #id_message').change(function() {
           calc_users_count();
    });
});
