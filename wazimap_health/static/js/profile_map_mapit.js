// extend the default Wazimap ProfileMaps object to add mapit support

var BaseProfileMaps = ProfileMaps;
ProfileMaps = function() {
    var self = this;
    this.mapit_url = GeometryLoader.mapit_url;

    _.extend(this, new BaseProfileMaps());

    this.drawAllFeatures = function() {
        var self = this;
        var geo = this.geo;
        var geo_level = geo.this.geo_level;
        var geo_code = geo.this.geo_code;
        var geo_version = geo.this.version;

        // add demarcation boundaries
        if (geo_level == 'country') {
            this.map.setView({lat: -28.4796, lng: 10.698445}, 5);
        } else {
            // draw this geometry
            GeometryLoader.loadGeometryForGeo(geo_level, geo_code, geo_version, function(feature) {
                self.drawFocusFeature(feature);
            });
        }
	if (geo_level == 'district'){
	    var greenIcon = new L.Icon({
		iconUrl: '/static/js/vendor/images/marker-icon-green.png',
		shadowUrl: '/static/js/vendor/images/marker-shadow.png',
		iconSize: [25, 41],
		iconAnchor: [12, 41],
		popupAnchor: [1, -34],
		shadowSize: [41, 41]
	    });
	    var healthGroup = new L.LayerGroup().addTo(this.map);
	    var pharmaGroup = new L.LayerGroup().addTo(this.map);
	    var marieGroup = new L.LayerGroup().addTo(this.map);
	    GeometryLoader.loadPointsForHealth(geo_code, function(data){
                var map = self.map;
                data['data'].forEach(function(facility){
		    if (facility['dataset'] == 'private_pharmacies'){
			L.marker([facility['latitude'],
				  facility['longitude']],
				 {icon: greenIcon}).addTo(pharmaGroup).bindPopup(facility['name']).on('click', function(){
			window.location = '/profiles/point-'+ facility['facility_code']+'/';
			      }).on('mouseover', function(e){
				  this.openPopup();
			      });
		    }else if (facility['dataset'] == 'public_facilities'){
			L.marker([facility['latitude'],
				  facility['longitude']]).addTo(healthGroup).bindPopup(facility['name']).on('click', function(){
			window.location = '/profiles/point-'+ facility['facility_code']+'/';
			      }).on('mouseover', function(e){
				  this.openPopup();
			      });
		    }else{
			L.marker([facility['latitude'],
				  facility['longitude']],
				 {icon: greenIcon}).addTo(marieGroup).bindPopup(facility['name']).on('click', function(){
			window.location = '/profiles/point-'+ facility['facility_code']+'/';
			      }).on('mouseover', function(e){
				  this.openPopup();
			      });
		    }
                });
	    });
	    
	    var overlayMap = {'Health Facilities': healthGroup, 'Private Pharmacies': pharmaGroup};
	    L.control.layers(null,overlayMap).addTo(this.map);
	}
	
	
	if (geo_level == 'point'){
	    GeometryLoader.loadLatLngForGeo(geo_code, function(data){
		var map = self.map;
		L.marker([data['latitude'], data['longitude']]).addTo(map);
		map.setView([data['latitude'], data['longitude']], 15);
	    });
	}
	


        // peers
        var parents = _.keys(geo.parents);
        if (parents.length > 0) {
          self.drawSurroundingFeatures(geo_level, parents[0], null, geo_version);
        }

        // every ancestor up to just before the root geo
        for (var i = 0; i < parents.length-1; i++) {
          self.drawSurroundingFeatures(parents[i], parents[i+1], null, geo_version);
        }

        // children
        if (geo.this.child_level) {
          self.drawSurroundingFeatures(geo.this.child_level, geo_level, geo_code, geo_version);
        }
    };

    // Add map shapes for a level, limited to within the parent level (eg.
    // wards within a municipality).
    this.drawSurroundingFeatures = function(level, parent_level, parent_code, parent_version) {
        var code,
            parent,
            self = this,
            url;

        parent_code = parent_code || this.geo.parents[parent_level].geo_code;
        parent_version = parent_version || this.geo.parents[parent_level].geo_version;
        parent = MAPIT.level_codes[parent_level] + '-' + parent_code;

        // code of 'level', if any?
        if (this.geo.this.geo_level == level) {
            code = this.geo.this.geo_code;
        } else if (this.geo.parents[level]) {
            code = this.geo.parents[level].geo_code;
        }

        GeometryLoader.loadGeometrySet(parent + '|' + MAPIT.level_codes[level], level, parent_version, function(geojson) {
            // don't include this smaller geo, we already have a shape for that
            geojson.features = _.filter(geojson.features, function(f) {
                return f.properties.code != code;
            });

            self.drawFeatures(geojson);
        });

        // if we're loading districts, we also want to load metros, because
        // districts don't give us full coverage
	// We also need to load the point that
        if (level == 'district') {
            GeometryLoader.loadGeometrySet(parent + '|' + MAPIT.level_codes.municipality, 'municipality', parent_version, function(geojson) {
                // only keep metros
                geojson.features = _.filter(geojson.features, function(f) {
                    // only metro codes are three letters
                    return f.properties.code.length == 3;
                });

                self.drawFeatures(geojson);
            });
        }
    };
};
