$().ready(function () {

    var url_string = window.location.href;
    var url = new URL(url_string);
    var c = url.searchParams.get('location');
    if (!c) {
        c = [55.751407, 37.618877];
    } else {
        c = c.split(', ');
    }

    var map = L.map('map', {minZoom: 1, maxZoom: 18}).setView(c, 16);
    L.tileLayer('https://{s}.tile.osm.org/{z}/{x}/{y}.png', {attribution: ''}).addTo(map);
    var leafletView = new PruneClusterForLeaflet();

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
    var blueIcon = new LeafIcon({
        iconUrl: '/static/map_osm/images/blue.png'
    })

    var colors = ['#42a7f5', '#5df542'],
    pi2 = Math.PI * 2;

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
    request.open("GET", '/static/map_osm/data.json?t=' + (new Date()).getTime(), false);
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
        var marker_icon = blueIcon;
        if (json[i]['c'] == 'g'){
            marker_icon = greenIcon;
        }
        var marker = new PruneCluster.Marker(json[i]['lt'], json[i]['lg'], {
            popup: s, icon: marker_icon
        });
        marker.category = 0;
        if (json[i]['c'] == 'g'){
            marker.category = 1;
        }
        leafletView.RegisterMarker(marker);
    }

    L.control.locate({flyTo: true, keepCurrentZoomLevel: true, drawCircle: false, strings: {
        title: 'Отправить свое местоположение', popup: 'Ваше местоположение'
    }}).addTo(map);
    map.addLayer(leafletView);

});