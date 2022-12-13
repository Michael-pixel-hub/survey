function switch_types () {
    $('#survey_taskstep_task-group div.dynamic-survey_taskstep_task').each(function(){

        const step_type = $(this).find('div.field-step_type select').val();
        const photo_field_1 = $(this).find('div.field-photo_inspector');
        const photo_field_2 = $(this).find('div.field-photo_check_assortment');
        const photo_field_3 = $(this).find('div.field-photo_check');
        const photo_field_4 = $(this).find('div.field-photo_from_gallery');
        const photo_field_5 = $(this).find('div.field-photo_out_reason');
        const photo_field_6 = $(this).find('div.field-photo_out_requires');
        const questionnaire_field_1 = $(this).find('div.field-questionnaire');

        if (step_type === 'photos') {
             photo_field_1.show();
             photo_field_2.show();
             photo_field_3.show();
             photo_field_4.show();
             photo_field_5.show();
             photo_field_6.show();
        }else {
             photo_field_1.hide();
             photo_field_2.hide();
             photo_field_3.hide();
             photo_field_4.hide();
             photo_field_5.hide();
             photo_field_6.hide();
        }

        if (step_type === 'questionnaire') {
             questionnaire_field_1.show();
        }else {
             questionnaire_field_1.hide();
        }

    });
}

$().ready(function () {
    switch_types();
    $('#survey_taskstep_task-group div.dynamic-survey_taskstep_task div.field-step_type select').change(function () {
        switch_types();
    });
    $('.add-row').click(function(e) {
        switch_types();
        $('#survey_taskstep_task-group div.dynamic-survey_taskstep_task div.field-step_type select').change(function () {
            switch_types();
        });
    });
});