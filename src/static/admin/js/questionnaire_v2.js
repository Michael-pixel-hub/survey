function switch_choices () {
    $('#survey_taskquestionnairequestion_task-group tr.form-row').each(function(){
        const question_type = $(this).find('td.field-question_type select').val();
        const choices_obj = $(this).find('td.field-choices textarea');
        if (question_type == 'choices') {
            choices_obj.show();
        }else {
            choices_obj.hide();
        }
    });
}

$().ready(function () {
    switch_choices();
    $('#survey_taskquestionnairequestion_task-group tr.form-row td.field-question_type select').change(function () {
        switch_choices();
    });
    $('.add-row').click(function(e) {
        switch_choices();
        $('#survey_taskquestionnairequestion_task-group tr.form-row td.field-question_type select').change(function () {
            switch_choices();
        });
    });
});