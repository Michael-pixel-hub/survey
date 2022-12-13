$().ready(function () {

    var url_string = window.location.href;
    var url = new URL(url_string);
    var c = url.searchParams.get('location');
    if (!c) {
        c = [59.936404, 30.31603];
    } else {
        c = c.split(', ');
    }

    var map = L.map('map', {minZoom: 1, maxZoom: 18}).setView(c, 16);
    L.tileLayer('https://{s}.tile.osm.org/{z}/{x}/{y}.png', {attribution: ''}).addTo(map);
    var leafletView = new PruneClusterForLeaflet();

    var colors = ['#2A81CB', '#FFD326', '#CB2B3E', '#2AAD27', '#CB8427', '#CAC428', '#9C2BCB', '#7B7B7B', '#3D3D3D'],
        pi2 = Math.PI * 2,
        icons = [blueIcon, goldIcon, redIcon, greenIcon, orangeIcon, yellowIcon, violetIcon, greyIcon, blackIcon]


    leafletView.BuildLeafletClusterIcon = function(cluster) {
        var e = new L.Icon.MarkerCluster();
        e.stats = cluster.stats;
        e.population = cluster.population;
        return e;
    };

    L.Icon.MarkerCluster = L.Icon.extend({
        options: {
            iconSize: new L.Point(44, 44),
            className: 'prunecluster leaflet-markercluster-icon'
        },

        createIcon: function () {
            // based on L.Icon.Canvas from shramov/leaflet-plugins (BSD licence)
            var e = document.createElement('canvas');
            this._setIconStyles(e, 'icon');
            var s = this.options.iconSize;
            e.width = s.x;
            e.height = s.y;
            this.draw(e.getContext('2d'), s.x, s.y);
            return e;
        },

        createShadow: function () {
            return null;
        },

        draw: function(canvas, width, height) {

            var lol = 0;

            var start = 0;
            for (var i = 0, l = colors.length; i < l; ++i) {

                var size = this.stats[i] / this.population;


                if (size > 0) {
                    canvas.beginPath();
                    canvas.moveTo(22, 22);
                    canvas.fillStyle = colors[i];
                    var from = start + 0.14,
                        to = start + size * pi2;

                    if (to < from) {
                        from = start;
                    }
                    canvas.arc(22,22,22, from, to);

                    start = start + size*pi2;
                    canvas.lineTo(22,22);
                    canvas.fill();
                    canvas.closePath();
                }

            }

            canvas.beginPath();
            canvas.fillStyle = 'white';
            canvas.arc(22, 22, 18, 0, Math.PI*2);
            canvas.fill();
            canvas.closePath();

            canvas.fillStyle = '#555';
            canvas.textAlign = 'center';
            canvas.textBaseline = 'middle';
            canvas.font = 'bold 12px sans-serif';

            canvas.fillText(this.population, 22, 22, 40);
        }
    });

    var request = new XMLHttpRequest();
    request.open("GET", '/static/map_osm/data_smoroza.json?t=' + (new Date()).getTime(), false);
    request.send(null)
    var json = JSON.parse(request.responseText);
    for (var i = 0; i < json.length; i++) {

        var s = '<b>Код магазина: ' + json[i]['sc'] + '</b><br/>'
        s += '<b>' + json[i]['scn'] + '</b><br/>'
        s += json[i]['sa'] + '<br/>'
        if (json[i]['sct']) {
            s += '<b>' + json[i]['sct'] + '</b><br/>'
        }
        s += json[i]['tx'];

        var m = new PruneCluster.Marker(json[i]['lt'], json[i]['lg'], {
            popup: s, icon: icons[json[i]['c']]
        });
        leafletView.RegisterMarker(m);
        m.category = json[i]['c']


        // var s = '<b>Код магазина:' + json[i]['sc'] + '</b><br/>'
        // s += json[i]['sa'] + '<br/>'
        // if (json[i]['sct']) {
        //     s += '<b>' + json[i]['sct'] + '</b><br/>'
        // }
        // s += json[i]['tx'];
        // var marker_icon = blueIcon;
        // if (json[i]['c'] == 'g'){
        //     marker_icon = greenIcon;
        // }
        // // var marker = new PruneCluster.Marker(json[i]['lt'], json[i]['lg'], {
        // //     popup: s, icon: marker_icon
        // // });
        // var marker = new L.Icon.MarkerCluster(json[i]['lt'], json[i]['lg']);
        // marker.category = 0;
        // if (json[i]['c'] == 'g'){
        //     marker.category = 1;
        // }
        // leafletView.RegisterMarker(marker);
    }

    L.control.locate({flyTo: true, keepCurrentZoomLevel: true, drawCircle: false, strings: {
        title: 'Отправить свое местоположение', popup: 'Ваше местоположение'
    }}).addTo(map);
    map.addLayer(leafletView);

});