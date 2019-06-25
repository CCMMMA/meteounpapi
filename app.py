from flask import Flask, request, jsonify
from flask_restplus import Resource, Api

app = Flask(__name__)
api = Api(app)

baseMaps = {
    "navionicsMarine": {
        "name": {
            "it":"Navionics Marine Chart",
            "en":"Navionics Marine Chart"
        },
        "type": "navionics",
        "extras": {
            "navKey": 'Navionics_webapi_00480',
            "chartType": "JNC.NAVIONICS_CHARTS.NAUTICAL",
            "isTransparent": False,
            "logoPayoff": True,
            "zIndex": 1
        }
    },
    "navionicsSonar": {
        "name": {
            "it":"Navionics Marine Sonar",
            "en":"Navionics Marine Sonar"
        },
        "type": "navionics",
        "extras": {
            "navKey": 'Navionics_webapi_00480',
            "chartType": 'JNC.NAVIONICS_CHARTS.SONARCHART',
            "isTransparent": False,
            "zIndex": 1
        }
    },
    "navionicsSky": {
        "name": {
            "it":"Navionics Ski Chart",
            "en":"Navionics Ski Chart"
        },
        "type": "navionics",
        "extras": {
            "navKey": 'Navionics_webapi_00480',
            "chartType": 'JNC.NAVIONICS_CHARTS.SKI',
            "isTransparent": False,
            "zIndex": 1
        }
    },
    "satellite": {
        "name": {
            "it":"Satellite",
            "en":"Satellite"
        },
        "type":"tiled",
        "url:":'http://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        "extras": {
                    "attribution": 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'
        }
    },
    "darkGray": {
        "name": {
            "it":"Toni scuri",
            "en":"Dark Gray"
        },
        "type": "tiled",
        "url:": "http://{s}.sm.mapstack.stamen.com/(toner-lite,$fff[difference],$fff[@23],$fff[hsl-saturation@20])/{z}/{x}/{y}.png",
        "extras": {
            "attribution": 'Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ, TomTom, Intermap, iPC, USGS, FAO, NPS, NRCAN, GeoBase, Kadaster NL, Ordnance Survey, Esri Japan, METI, Esri China (Hong Kong), and the GIS User Community'
        }
    },
    "osm": {
        "name": {
            "it":"Open Street Map",
            "en":"Open Street Map"
        },
        "type": "tiled",
        "url":'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        "extras": {
            "attribution": '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        }
    }
}

layers={
    "info": {
        "name": {
            "it":"Info",
            "en":"Info"
        },
        "type":"icon",
        "extras": {
        }
    },
    "wind": {
        "name": {
            "it":"Vento",
            "en":"Wind"
        },
        "type":"velocity",
        "url":"http://api.meteo.uniparthenope.it/products/wrf5/forecast/{domain}/grib/json?date={ncepDate}",
        "extras": {
            "displayValues": True,
            "displayOptions": {
                "velocityType": 'Wind 10m',
                "position": 'bottomleft',
                "displayPosition": 'bottomleft',
                "displayEmptyString": 'No wind data',
                "angleConvention": 'meteoCW',
                "speedUnit": 'kt'
            },
            "minVelocity": 0,
            "maxVelocity": 25.72,
            "velocityScale": 0.005,
            "colorScale": [
                "#000033", "#0117BA", "#011FF3", "#0533FC", "#1957FF", "#3B8BF4",
                "#4FC6F8", "#68F5E7", "#77FEC6", "#92FB9E", "#A8FE7D", "#CAFE5A",
                "#EDFD4D", "#F5D03A", "#EFA939", "#FA732E", "#E75326", "#EE3021",
                "#BB2018", "#7A1610", "#641610"]
        }
    },
    "cloud": {
        "name": {
            "it":"Nuvolosit&agrave;",
            "en":"Cloud"
        },
        "type":"wms",
        "url": 'http://data.meteo.uniparthenope.it/ncWMS2/wms/lds/opendap/wrf5/{domain}/archive/{year}/{month}/{day}/wrf5_{domain}_{ncepDate}.nc',
        "extras": {

            "layers": 'CLDFRA_TOTAL',
            "styles": 'raster/tcldBars',
            "format": 'image/png',
            "transparent": True,
            "opacity": 0.8,
            "COLORSCALERANGE": "0.125,1",
            "NUMCOLORBANDS": "250",
            "ABOVEMAXCOLOR": "extend",
            "BELOWMINCOLOR": "transparent",
            "BGCOLOR": "extend",
            "LOGSCALE": "false"
        }
    },
    "t2c": {
        "name": {
            "it":"Temperatura a 2m",
            "en":"Temperature at 2m"
        },
        "type":"wms",
        "url": 'http://data.meteo.uniparthenope.it/ncWMS2/wms/lds/opendap/wrf5/{domain}/archive/{year}/{month}/{day}/wrf5_{domain}_{ncepDate}.nc',
        "extras": {
            "layers": 'T2C',
            "styles": 'default-scalar/tspBars',
            "format": 'image/png',
            "transparent": True,
            "opacity": 0.8,
            "COLORSCALERANGE": "-40,50",
            "NUMCOLORBANDS": "19",
            "ABOVEMAXCOLOR": "extend",
            "BELOWMINCOLOR": "extend",
            "BGCOLOR": "extend",
            "LOGSCALE": "false"
        }
    },
    "rain": {
        "name": {
            "it":"Pioggia",
            "en":"Rain"
        },
        "type":"wms",
        "url": 'http://data.meteo.uniparthenope.it/ncWMS2/wms/lds/opendap/wrf5/{domain}/archive/{year}/{month}/{day}/wrf5_{domain}_{ncepDate}.nc',
        "extras": {
            "layers": 'DELTA_RAIN',
            "styles": 'raster/crhBars',
            "format": 'image/png',
            "transparent": True,
            "opacity": 0.8,
            "COLORSCALERANGE": ".2,60",
            "NUMCOLORBANDS": "15",
            "ABOVEMAXCOLOR": "extend",
            "BELOWMINCOLOR": "transparent",
            "BGCOLOR": "extend",
            "LOGSCALE": "false"
        }
    },
    "snow": {
        "name": {
            "it":"Neve",
            "en":"Snow"
        },
        "type":"wms",
        "url": 'http://data.meteo.uniparthenope.it/ncWMS2/wms/lds/opendap/wrf5/{domain}/archive/{year}/{month}/{day}/wrf5_{domain}_{ncepDate}.nc',
        "extras": {
            "layers": 'HOURLY_SWE',
            "styles": 'raster/sweBars',
            "format": 'image/png',
            "transparent": True,
            "opacity": 0.8,
            "COLORSCALERANGE": "0.5,15.5",
            "NUMCOLORBANDS": "6",
            "ABOVEMAXCOLOR": "extend",
            "BELOWMINCOLOR": "transparent",
            "BGCOLOR": "extend",
            "LOGSCALE": "false"
        }
    },
}

maps={
    "weather": {
        "name": {
            "it":"Previsioni Meteo",
            "en":"Weather Forecast"
        },
        "baseMaps":[
            { "satellite": True },
            { "darkGray": False },
            { "osm": False}
        ],
        "layers": [
            { "cloud": True },
            { "t2c": False },
            { "rain": True },
            { "snow": True },
            { "wind": True },
            { "info": False },
        ]
    },
    "muggles": {
        "name": {
            "it":"Previsioni Meteo Semplificate",
            "en":"Easy Weather Forecast"
        },
        "baseMaps":[
            { "satelline": True },
        ],
        "layers": [
            { "cloud": True },
            { "rain": True },
            { "snow": True },
            { "wind": True },
            { "info": True },
        ]
    },
    "nautical": {
        "name": {
            "it":"Previsioni Meteo Nautiche",
            "en":"Nautical Weather Forecast"
        },
        "baseMaps":[
            { "navionicsMarine": True },
            { "navionicsSonar": False }
        ],
        "layers": [
            { "cloud": True },
            { "t2c": False },
            { "rain": True },
            { "snow": True },
            { "wind": True }
        ]
    },
}

@api.route('/basemaps')
class BaseMaps(Resource):
    def get(self):
        return jsonify(baseMaps)

@api.route('/basemaps/<name>')
class BaseMapsByName(Resource):
    def get(self,name):
        return jsonify(baseMaps[name])

@api.route('/layers')
class Layers(Resource):
    def get(self):
        return jsonify(layers)

@api.route('/layers/<name>')
class LayersByName(Resource):
    def get(self,name):
        return jsonify(layers[name])

@api.route('/maps')
class Maps(Resource):
    def get(self):
        return jsonify(maps)

@api.route('/maps/<name>')
class MapsByName(Resource):
    def get(self,name):
        return jsonify(maps[name])

if __name__ == '__main__':
    app.run(debug=True)