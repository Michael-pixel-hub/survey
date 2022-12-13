var $ = django.jQuery || grp.jQuery;

$().ready(function () {

    function calc_images_count() {

        var data = {
            'data_start': $('#te_datetime_start').val(),
            'data_end': $('#te_datetime_end').val(),
            'id_user': $('#id_user').val(),
            'id_task': $('#id_task').val(),
            'id_client': $('#id_client').val(),
            'id_imagestep': $('#id_imagestep').val()
        }

        $.ajax({
            url: '/survey/data/images/count/',
            data: data,
            beforeSend: function() {
                $('#images_count').html('Считаем...');
                $('#download_images').prop('disabled', true);
            },
        }).done(function(data) {
            $('#images_count').html(data);
            try {
                count = parseInt(data);
                if (count > 0 && count < 5000) {
                    $('#download_images').prop('disabled', false);
                }
            } catch {
                $('#download_images').prop('disabled', true);
            }
        });

    }

    // $('#te_datetime_start, #te_datetime_end').focusout(function() {
    //     calc_images_count();
    // });
    $('#te_datetime_start, #te_datetime_end').focus(function() {
        calc_images_count();
    });
    $('#te_datetime_start, #te_datetime_end').change(function() {
        calc_images_count();
    });
    $('#id_user, #id_client, #id_imagestep').focus(function() {
        calc_images_count();
    });
    $('#id_user, #id_client, #id_imagestep').change(function() {
        calc_images_count();
    });
    $('#download_images_form').submit(function( event ) {
        $('#download_images_text').show();
    });
    $('#id_task').focus(function() {
        $("#id_imagestep").val("");
        calc_images_count().change();
        $("#id_imagestep").empty();
    });
    $('#id_task').change(function() {
        $("#id_imagestep").val("");
        calc_images_count()
        $("#id_imagestep").empty();
    });
    

});
