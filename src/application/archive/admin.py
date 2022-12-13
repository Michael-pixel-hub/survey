from django.template.loader import render_to_string

from application.survey.models import Assortment as StoreAssortment
from application.survey.filters import CodeFilter, TaskFilter, RegionFilter, ClientFilter
from django.apps.registry import apps
from django.contrib import admin
from django.db.models import Q
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from .models import ArchiveTasksExecutionBase, ArchiveTasksExecution, ArchiveTasksExecutionImage, \
    ArchiveTasksExecutionAssortmentBefore, ArchiveTasksExecutionAssortment, ArchiveTasksExecutionQuestionnaire


@admin.register(ArchiveTasksExecution)
class ArchiveTaskExecutionAdmin(admin.ModelAdmin):

    change_list_template = 'admin/change_list_archive.html'

    class Media:
        js = (
            '//ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js',
            '/static/admin/js/archive.js',
            '/static/admin/js/jquery.cookie.js',
        )

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.load_data()

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return True

    def load_data(self):
        try:
            end_date = ArchiveTasksExecution.objects.only('date_start').latest('date_start').date_start
            self.year_end = end_date.year
            self.month_end = end_date.month
            start_date = ArchiveTasksExecution.objects.only('date_start').earliest('date_start').date_start
            self.year_start = start_date.year
            self.month_start = start_date.month
        except:
            self.year_start = self.year_end = 2021
            self.month_start = self.month_end = 1

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        try:
            readonly_fields.remove('date_start')
        except:
            pass
        return readonly_fields

    def get_year(self, request):

        archive_year = self.year_start
        if 'archive_year' in request.COOKIES:
            try:
                archive_year = int(request.COOKIES['archive_year'])
                if archive_year not in range(self.year_start, self.year_end + 1):
                    archive_year = self.year_start
            except:
                archive_year = self.year_start

        return archive_year

    def get_months(self, request):

        year = self.get_year(request)
        if year == self.year_start and year == self.year_end:
            return range(self.month_start, self.month_end + 1)
        if year == self.year_start:
            return range(self.month_start, 13)
        if year == self.year_end:
            return range(1, self.month_end + 1)
        return range(1, 13)

    def get_month(self, request):

        archive_month = None

        if 'archive_month' in request.COOKIES:
            try:
                archive_month = int(request.COOKIES['archive_month'])
                if archive_month not in self.get_months(request):
                    archive_month = None
            except:
                archive_month = None

        if archive_month is None:
            archive_month = self.get_months(request)[0]

        return archive_month

    def get_queryset(self, request):

        self.load_data()

        year = self.get_year(request)
        month = self.get_month(request)
        if month < 10:
            month = f'0{month}'

        if 't' in apps.all_models['archive']:
            del apps.all_models['archive']['t']

        class T (ArchiveTasksExecutionBase):
            class Meta:
                db_table = f'archive_tasks_executions_y{year}_m{month}'

        qs = T.objects.all()

        return qs

    def changelist_view(self, request, extra_context=None):
        if extra_context is None:
            extra_context = {}
        extra_context['archive_years'] = range(self.year_start, self.year_end + 1)
        extra_context['archive_year'] = self.get_year(request)
        extra_context['archive_months'] = self.get_months(request)
        extra_context['archive_month'] = self.get_month(request)
        return super().changelist_view(request, extra_context)

    def get_status_html(self, obj):
        if obj.status == 1:
            return mark_safe('<span style="color: gray">%s</span>' % obj.get_status_display())
        if obj.status == 3:
            return mark_safe('<span style="color: blue">%s</span>' % obj.get_status_display())
        if obj.status == 4:
            return mark_safe('<span style="color: green">%s</span>' % obj.get_status_display())
        if obj.status == 5:
            return mark_safe('<span style="color: red">%s</span>' % obj.get_status_display())
        if obj.status == 6:
            return mark_safe('<b>%s</b>' % obj.get_status_display())
        return obj.get_status_display()
    get_status_html.allow_tags = True
    get_status_html.short_description = _('Status')

    def store_short(self, obj):
        if obj.store is None:
            return '-'
        s = str(obj.store)
        if len(s) > 100:
            s = s[:100] + '...'
        return s
    store_short.short_description = _('Store')

    def map_html(self, obj):

        if obj.longitude is None or obj.latitude is None or obj.distance is None:
            return mark_safe('-')

        s = '''
            <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css"
       integrity="sha512-xodZBNTC5n17Xt2atTPuE1HxjVMSvLVW9ocqUKLsCC5CXdbqCmblAshOMAS6/keqq/sMZMZ19scR4PsZChSR7A=="
       crossorigin=""/>
            <!-- Make sure you put this AFTER Leaflet's CSS -->
     <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"
       integrity="sha512-XQoYMqMTK8LvdxXYG3nZ448hOEQiglfqkJs1NOQV44cWnUrBc8PkAOcXy20w0vlaXaVUearIOBhiXZ5V3ynxwA=="
       crossorigin=""></script>
            <style>
                .field-status_html p  {font-size: 16px !important}
                #task_images-group {max-height: 800px; overflow-y: scroll}
                #map {width:800px; height:400px}
            </style>
            <div id="map"></div>
            <script type="text/javascript">
                $().ready(function () {
                    var map = L.map('map', {minZoom: 1, maxZoom: 18}).setView([{latitude}, {longitude}], 16);

    //L.tileLayer('https://{s}.tilessputnik.ru/{z}/{x}/{y}.png', {
        //attribution: ''
    //}).addTo(map);   

    L.tileLayer('https://{s}.tile.osm.org/{z}/{x}/{y}.png', {
        attribution: ''
    }).addTo(map);          

    var LeafIcon = L.Icon.extend({
        options: {
           iconSize:     [34, 41],
           iconAnchor:   [12, 37],
           popupAnchor:  [2, -36]
        }
    });

    var greenIcon = new LeafIcon({
        iconUrl: '/static/map_osm/images/green.png'
    })     
    var redIcon = new LeafIcon({
        iconUrl: '/static/map_osm/images/red.png'
    })                                     

                    var marker = L.marker([{latitude}, {longitude}], {icon: greenIcon}).addTo(map);                
                    var marker_store = L.marker([{store_latitude}, {store_longitude}], {icon: redIcon}).addTo(map);                
                    var bounds = [[{latitude}, {longitude}], [{store_latitude}, {store_longitude}]];
                    var pathLine = L.polyline([[{latitude}, {longitude}], [{store_latitude}, {store_longitude}]], {color: "#3985db", weight: 4}).addTo(map);

                    if ({distance} < 0.14) {
                        var popup = L.popup().setContent('{distance} км');                                
                        pathLine.bindPopup(popup);
                        var popup2 = L.popup().setContent('Местонахождение сюрвеера');                                
                        marker.bindPopup(popup2);
                        var popup3 = L.popup().setContent('Местонахождение магазина');                                
                        marker_store.bindPopup(popup3) ;                      
                    } else {
                        var popup = L.popup({closeOnClick: false, autoClose: false}).setContent('{distance} км');                                
                        pathLine.bindPopup(popup).openPopup();
                        var popup2 = L.popup({closeOnClick: false, autoClose: false}).setContent('Местонахождение сюрвеера');                                
                        marker.bindPopup(popup2).openPopup();       
                        var popup3 = L.popup({closeOnClick: false, autoClose: false}).setContent('Местонахождение магазина');                                
                        marker_store.bindPopup(popup3).openPopup();                        
                    }                                                      
                    map.fitBounds(bounds, {paddingTopLeft: [50, 50]});   
                    //alert(map.getBoundsZoom());   
                });
            </script>
            '''

        s = s.replace('{longitude}', str(obj.longitude))
        s = s.replace('{latitude}', str(obj.latitude))
        s = s.replace('{store_longitude}', str(obj.store.longitude))
        s = s.replace('{store_latitude}', str(obj.store.latitude))
        s = s.replace('{distance}', str(obj.distance / 1000))

        if obj.distance:
            return mark_safe(s)
        else:
            return mark_safe('-')
    map_html.allow_tags = True
    map_html.short_description = _('Map')

    def images_simple(self, obj):
        images = ArchiveTasksExecutionImage.objects.filter(task_id=obj.id).filter(~Q(constructor_step_name=''))
        html = ''
        for i in images:
            html += '<a target="_blank" href="https://admin.shop-survey.ru/' + i.image.url + \
                    '" title="' + i.constructor_step_name + '"><img style="max-height: 300px; margin-right: 10px; ' \
                    'margin-bottom: 10px" src="https://admin.shop-survey.ru/' + i.image.url + '" alt="" /></a>'
        return mark_safe(html)
    images_simple.allow_tags = True
    images_simple.short_description = _('Images all')

    def images_simple_before(self, obj):
        images = ArchiveTasksExecutionImage.objects.filter(task_id=obj.id, type='before')
        html = ''
        for i in images:
            html += '<a target="_blank" href="https://admin.shop-survey.ru/' + i.image.url + \
                    '" title="Увеличить изображение"><img style="max-height: 300px; margin-right: 10px; ' \
                    'margin-bottom: 10px" src="https://admin.shop-survey.ru/' + i.image.url + '" alt="" /></a>'
        return mark_safe(html)
    images_simple_before.allow_tags = True
    images_simple_before.short_description = _('Images before')

    def images_simple_after(self, obj):
        images = ArchiveTasksExecutionImage.objects.filter(task_id=obj.id, type='after')
        html = ''
        for i in images:
            html += '<a target="_blank" href="https://admin.shop-survey.ru/' + i.image.url + \
                    '" title="Увеличить изображение"><img style="max-height: 300px; margin-right: 10px; ' \
                    'margin-bottom: 10px" src="https://admin.shop-survey.ru/' + i.image.url + '" alt="" /></a>'
        return mark_safe(html)
    images_simple_after.allow_tags = True
    images_simple_after.short_description = _('Images after')

    def images_simple_check(self, obj):
        images = ArchiveTasksExecutionImage.objects.filter(task_id=obj.id, type='check')
        html = ''
        for i in images:
            html += '<a target="_blank" href="https://admin.shop-survey.ru/' + i.image.url + \
                    '" title="Увеличить изображение"><img style="max-height: 300px; margin-right: 10px; ' \
                    'margin-bottom: 10px" src="https://admin.shop-survey.ru/' + i.image.url + '" alt="" /></a>'
        return mark_safe(html)
    images_simple_check.allow_tags = True
    images_simple_check.short_description = _('Images check')

    # def store_assortment_full(self, obj):
    #     goods = list(StoreAssortment.objects.filter(store=obj.store))
    #     goods_after = ArchiveTasksExecutionAssortment.objects.filter(task_id=obj.id)
    #     data = []
    #     for i in goods:
    #         item = {'name': i.good.name, 'in_store': False, 'count': i.count}
    #         for j in goods_after:
    #             if i.good.code and i.good.code == j.good.code:
    #                 item['in_store'] = True
    #         data.append(item)
    #     html = render_to_string('admin/fields/store_assortment_full.html', {'data': data})
    #     return mark_safe(html)
    # store_assortment_full.allow_tags = True
    # store_assortment_full.short_description = ''

    def assortment_before_full(self, obj):
        data = ArchiveTasksExecutionAssortmentBefore.objects.filter(task_id=obj.id)
        html = render_to_string('admin/fields/assortment_full.html', {'data': data})
        return mark_safe(html)
    assortment_before_full.allow_tags = True
    assortment_before_full.short_description = ''

    def assortment_full(self, obj):
        data = ArchiveTasksExecutionAssortment.objects.filter(task_id=obj.id)
        html = render_to_string('admin/fields/assortment_full.html', {'data': data})
        return mark_safe(html)
    assortment_full.allow_tags = True
    assortment_full.short_description = ''

    def questionnaire_full(self, obj):
        data = ArchiveTasksExecutionQuestionnaire.objects.filter(task_id=obj.id)
        html = render_to_string('admin/fields/questionnaire_full.html', {'data': data})
        return mark_safe(html)
    questionnaire_full.allow_tags = True
    questionnaire_full.short_description = ''

    list_display = ('user', 'user_name', 'user_surname', 'task', 'date_start', 'date_end', 'store_short', 'check_type',
                    'is_auditor', 'source', 'get_status_html', )
    list_display_links = ('user', )

    fieldsets = (
        (None, {
            'fields': ('user', 'task', 'money', 'money_source', 'store', 'step', 'source',)
        }),
        (_('Comments'), {
            'fields': ('comments', 'comments_internal',)
        }),
        (_('Status change'), {
            'fields': ('status', 'is_auditor', 'comments_status', 'check_type', 'check_user')
        }),
        (_('Dates'), {
            'fields': ('date_start', 'date_end_user', 'date_end',)
        }),
        (_('Coordinates'), {
            'fields': ('longitude', 'latitude', 'map_html', 'distance',)
        }),
        (_('Inspector'), {
            'classes': ('collapse',),
            'fields': ('inspector_is_work', 'inspector_link_html', 'inspector_status', 'inspector_status_before',
                       'inspector_error',
                       'inspector_upload_images_text', 'inspector_recognize_text', 'inspector_report_text',
                       'inspector_positions_text', 'inspector_report_id', 'inspector_report_id_before',
                       'inspector_is_alert',)
        }),
        (_('Mailing'), {
            'classes': ('collapse',),
            'fields': ('telegram_channel_status',)
        }),
        (_('Images'), {
            'fields': ('images_simple', 'images_simple_before', 'images_simple_after', 'images_simple_check')
        }),
        # (_('AVAIL ASSORTMENT STORE'), {
        #     'fields': ('store_assortment_full',)
        # }),
        (_('Avail assortments before'), {
            'fields': ('assortment_before_full',)
        }),
        (_('Avail assortments'), {
            'fields': ('assortment_full',)
        }),
        (_('Questionnaire'), {
            'fields': ('questionnaire_full',)
        }),
    )

    search_fields = ['task__name', 'user__username', 'user__first_name', 'user__last_name', 'user__telegram_id',
                     'user__phone', 'user__name', 'user__surname', 'user__email', 'store__address', 'comments',
                     'inspector_status']
    raw_id_fields = ['user', 'store']
    readonly_fields = ['date_start', 'map_html', 'inspector_link_html', 'images_simple',
                       'images_simple_before', 'images_simple_after', 'images_simple_check',
                       'assortment_before_full', 'assortment_full', 'questionnaire_full']
    date_hierarchy = 'date_start'
    list_filter = ('status', 'source', 'user__status_legal', 'check_type', 'is_auditor', TaskFilter, ClientFilter, RegionFilter,
                   CodeFilter)
    list_select_related = ('user', 'store', 'task', 'store__client', 'user__rank')
    list_per_page = 50
