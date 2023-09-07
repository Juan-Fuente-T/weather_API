                          #//////////////////////////////////////#
                        #                                      #
                        ###           Weather APP            ###    
                        #                                      #
                        #//////////////////////////////////////#



                                              #WEATHER APP v0.0.3
"""
Esta aplicación multiplataforma (Windows, Linux, Mac) convierte una cantidad de una moneda en codigo ISO, por ejemplo EUR (euros), en el valor correspondiente en otra divisa, por ejemplo USD (dolares americanos), y opera mediante interfaz alfanumérica en el terminal del sistema operativo :
"""
# ©2023 Apliccion d epronóstico del tiempo de Juan Fuente

"""Novedades de la versión 0.0.2
- Se Integra la API de openmeteo.com
- Se integra la API de Nominatim
- Se verifica la validez de postal_code y location
- Se integra Timezonefinder para localizar la zona horaria
"""

#Listado de funciones: comprobar_cantidad_moneda (recoge la cantidad de moneda a convertir y evalua la calidad de los datos), comprobar_divisa(recoge las monedas introducidas por el usuario, asegura la calidad de los datos y devuelve separados el nombre y el valor de la moneda. Se usa tanto para obtener la moneda como la divisa.)



                            #BLOQUE DE IMPORTACIONES
import requests #se necesita requests instalado con pip para hacer llamada a la API de conversion

from geopy.exc import GeocoderTimedOut
from geopy.geocoders import Nominatim
import pgeocode
from timezonefinder import TimezoneFinder
import re
#response = requests.get('https://postal-codes.cybo.com/', verify=False)



                            #BLOQUE DE CAPTURA DE DATOS MEDIANTE API


"""#RESULTADO DE LA API
weather = {'latitude': 52.52, 'longitude': 13.419998, 'generationtime_ms': 0.8310079574584961, 'utc_offset_seconds': 7200, 'timezone': 'Europe/Berlin', 'timezone_abbreviation': 'CEST', 'elevation': 38.0, 'current_weather': {'temperature': 21.2, 'windspeed': 5.8, 'winddirection': 274, 'weathercode': 0, 'is_day': 1, 'time': '2023-09-04T12:00'}, 'daily_units': {'time': 'iso8601', 'apparent_temperature_max': '°C', 'apparent_temperature_min': '°C', 'precipitation_probability_mean': '%', 'weathercode': 'wmo code',
'sunrise': 'iso8601', 'sunset': 'iso8601'}, 'daily': {'time': ['2023-09-04', '2023-09-05', '2023-09-06', '2023-09-07', '2023-09-08', '2023-09-09', '2023-09-10'], 'apparent_temperature_max': [25.1, 27.0, 28.7, 27.3, 27.6, 29.8, 30.0], 'apparent_temperature_min': [11.0, 14.3, 14.7, 16.2, 16.1, 17.1, 15.3], 'precipitation_probability_mean': [0, 0, 0, 0, 0, 0, 3], 'weathercode':
[45, 3, 1, 3, 1, 0, 45], 'sunrise': ['2023-09-04T06:22', '2023-09-05T06:23', '2023-09-06T06:25', '2023-09-07T06:27', '2023-09-08T06:28', '2023-09-09T06:30', '2023-09-10T06:32'], 'sunset': ['2023-09-04T19:48', '2023-09-05T19:46', '2023-09-06T19:44', '2023-09-07T19:41', '2023-09-08T19:39', '2023-09-09T19:37', '2023-09-10T19:34']}}"""



#url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&timezone={timezone}&daily=temperature_2m_1h,precipitation_probability_mean,weathercode,sunrise,sunset&current_weather=true&forecast_days=7"

#funcion que compruebaque la localicacion sea valida, si lo es devuelve longitu y latitud
debugging = True


def geocode_location(location):
    
    print("Comprobando entrada datos Location Nominating:", location)
    geolocator = Nominatim(user_agent="myWeatherApp")
    print(f"Geocodificando la ubicación: {location}")
    location_data = geolocator.geocode(location)
    print("location_data", location)
    try:
        location_data = geolocator.geocode(location, timeout=10)
        if location_data:
            latitude = location_data.latitude
            longitude = location_data.longitude
            tf = TimezoneFinder()
            timezone = tf.timezone_at(lng=longitude, lat=latitude)
            print(f"Ubicación encontrada. Latitud: {latitude}, Longitud: {longitude}")
            return latitude, longitude,timezone
        else:
            print("No se pudo encontrar la ubicación.")
            return None, None, None
    except GeocoderTimedOut:
        print("Tiempo de espera agotado al buscar la ubicación.")
        return None
    except Exception as e:
        print(f"Ocurrió un error al buscar la ubicación: {e}")
        return None
    
#funcion que comprueba que el codigo postal sea valido en cuyo caso devuelve la longitu y latitud

def geocode_postal_code(postal_code):
    geocoder = pgeocode.Nominatim('es')
    location_data = geocoder.query_postal_code(postal_code)
    latitude = location_data.latitude if not location_data.empty else None
    longitude = location_data.longitude if not location_data.empty else None
    
    if latitude is not None and longitude is not None:
        tf = TimezoneFinder()
        timezone = tf.timezone_at(lng=longitude, lat=latitude)
        if debugging:
            print("Log y lat postal_code:", longitude, latitude)
            print("Timezone postal_code:", timezone)
        return latitude, longitude, timezone
    else:
        return None, None, None
    #Log y lat location: 7.540121 44.933143
    
"""def is_postal_code(input_value):
    nomi = pgeocode.Nominatim('ES')
    location = nomi.query_postal_code(input_value)
    if location.empty:
        return False #el codigo postal no es valido
    else: 
        return True #el codigo postyal es valido"""
def is_postal_code(input_value):
# Expresión regular para verificar si el input es un código postal (formato numérico de 5 dígitos)
    postal_code_pattern = r'^\d{5}$'

    # Verificar si el input coincide con el patrón de código postal
    if re.match(postal_code_pattern, input_value):
        return True  # Es un código postal válido
    else:
        return False  # No es un código postal válido (asumimos que es una ciudad)       
        

#funcion que devuelve el timezone para location o postal_code
def get_timezone(location):
    coordinates = geocode_location(location)
    if coordinates:
        latitude, longitude = coordinates
        tf = TimezoneFinder()
        timezone = tf.timezone_at(lng=longitude, lat=latitude)
        if debugging:
            print("Timezone location:", timezone)
        return timezone
    else:
        coordinates = geocode_postal_code(postal_code)
        if coordinates:
            latitude, longitude = coordinates
            tf = TimezoneFinder()
            timezone = tf.timezone_at(lng=longitude, lat=latitude)
            if debugging:
                print("Timezone postal _code:", timezone)
            return timezone
        else:
            return None



def get_weather(latitude, longitude, timezone):
    #city = request.args.get('city')
    #weather_response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid=097cb4956829efc4877aa5dd20140f59')
    #weather = weather_response.json()
    #forecast_text = f'El pronóstico del tiempo para {city} es: {weather["weather"][0]["description"]}.'
    #print(weather)
    weather_response = requests.get(f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&timezone={timezone}&daily=apparent_temperature_max,apparent_temperature_min,precipitation_probability_mean,weathercode,sunrise,sunset&current_weather=true&forecast_days=7')
    
    weather = weather_response.json()
    print(weather)

    #city = "madrid"

    #print(weather)
    # convertir el pronóstico del tiempo a texto
    #forecast_text = f'El pronóstico del tiempo para {city} es: {weather["current_weather"]["winddirection"]}.'
    #print(forecast_text)


#----------------------LOGICA---------------------

input_value = input("Introduce tu Ciudad o código postal: ")
#location = input("Introduce tu Ciudad o código postal: ")
#postal_code = input("Introduce tu Ciudad o código postal: ")

#location, postal_code = is_postal_code(input_value)
if is_postal_code(input_value):
    postal_code= input_value
    location = None
else: 
    location = input_value
    postal_code =None
    
"""    
if location:
    latitude, longitude = geocode_location(location)
    if not latitude or not longitude:
        postal_code = input_value
elif postal_code:
    latitude, longitude = geocode_postal_code(postal_code)
    if not latitude or not longitude:
        location = input_value """   
if location:
    latitude, longitude, timezone = geocode_location(location)
elif postal_code:
    latitude, longitude, timezone = geocode_postal_code(postal_code)
else:
    print("Debes proporcionar una localidad o codigo postal validos")
    exit()
"""timezone = get_timezone(location)
if not timezone:
    timezone = get_timezone(postal_code)"""
    
if debugging:
    print("Datos antes de funcion get_weather:", latitude, longitude)

# Verificar si se obtuvieron valores válidos
if latitude is not None and longitude is not None and timezone is not None:
    # Llamar a get_weather con los valores obtenidos
    get_weather(latitude, longitude, timezone)
else:
    print("No se pudieron obtener coordenadas o zona horaria para la ubicación.")


#RESULTADO DE LA API
{'latitude': 52.52, 'longitude': 13.419998, 'generationtime_ms': 0.8310079574584961, 'utc_offset_seconds': 7200, 'timezone': 'Europe/Berlin', 'timezone_abbreviation': 'CEST', 'elevation': 38.0, 'current_weather': {'temperature': 21.2, 'windspeed': 5.8, 'winddirection': 274, 'weathercode': 0, 'is_day': 1, 'time': '2023-09-04T12:00'}, 'daily_units': {'time': 'iso8601', 'apparent_temperature_max': '°C', 'apparent_temperature_min': '°C', 'precipitation_probability_mean': '%', 'weathercode': 'wmo code',
'sunrise': 'iso8601', 'sunset': 'iso8601'}, 'daily': {'time': ['2023-09-04', '2023-09-05', '2023-09-06', '2023-09-07', '2023-09-08', '2023-09-09', '2023-09-10'], 'apparent_temperature_max': [25.1, 27.0, 28.7, 27.3, 27.6, 29.8, 30.0], 'apparent_temperature_min': [11.0, 14.3, 14.7, 16.2, 16.1, 17.1, 15.3], 'precipitation_probability_mean': [0, 0, 0, 0, 0, 0, 3], 'weathercode':
[45, 3, 1, 3, 1, 0, 45], 'sunrise': ['2023-09-04T06:22', '2023-09-05T06:23', '2023-09-06T06:25', '2023-09-07T06:27', '2023-09-08T06:28', '2023-09-09T06:30', '2023-09-10T06:32'], 'sunset': ['2023-09-04T19:48', '2023-09-05T19:46', '2023-09-06T19:44', '2023-09-07T19:41', '2023-09-08T19:39', '2023-09-09T19:37', '2023-09-10T19:34']}}

#keys = list(divisas['rates'].keys()) #se cogen los nombres de las divisas y se meten en una lista donde poder comparar si están las elegidas por el usuario

#diccionario de divisas ordenadas alfabeticamente por su nombre en castellano




        #/////////////////////////#
        #// ##   FUNCIONES   ## //#         
        #/////////////////////////#

#Listado de funciones: comprobar_cantidad_moneda (recoge la cantidad de moneda a convertir y evalua la calidad de los datos), comprobar_divisa(recoge las monedas introducidas por el usuario, asegura la calidad de los datos y devuelve separados el nombre y el valor de la moneda. Se usa tanto para obtener la moneda como la divisa.)

        


