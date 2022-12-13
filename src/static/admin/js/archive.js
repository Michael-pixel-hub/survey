$().ready(function () {

    $('#changelist-search div').append($('#archive-year')).append($('#archive-month'));
    $('#archive-year, #archive-month').css('display', 'inline-block');
    $('#archive-year select').change(function () {
        $.cookie('archive_year', $(this).val());
        $.cookie('archive_month', 1);
        document.location.reload();
    });
    $('#archive-month select').change(function () {
        $.cookie('archive_month', $(this).val());
        document.location.reload();
    });

});