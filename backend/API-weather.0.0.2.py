                        #//////////////////////////////////////#
                        #                                      #
                        ###      CALCULADORA DE DIVISAS    ###    
                        #                                      #
                        #//////////////////////////////////////#



                                              #CALCULADORA DE DIVISAS v0.0.6
"""
Esta aplicación multiplataforma (Windows, Linux, Mac) convierte una cantidad de una moneda en codigo ISO, por ejemplo EUR (euros), en el valor correspondiente en otra divisa, por ejemplo USD (dolares americanos), y opera mediante interfaz alfanumérica en el terminal del sistema operativo :
"""
# ©2023 Calculadora de divisas de Juan Fuente

"""Novedades de la versión 0.2.1
- Integración de un segundo calculo para mostrar al usuario el valor de una unidad de una divisa respecto a su moneda
"""

#Listado de funciones: comprobar_cantidad_moneda (recoge la cantidad de moneda a convertir y evalua la calidad de los datos), comprobar_divisa(recoge las monedas introducidas por el usuario, asegura la calidad de los datos y devuelve separados el nombre y el valor de la moneda. Se usa tanto para obtener la moneda como la divisa.)

""" Datos sobre las API que proporcionan los valores de cambios:
Open Exchange Rates: Ofrece una API gratuita y de pago para obtener tasas de cambio en tiempo real. Limitada a 250 llamadas gratuitas. https://exchangeratesapi.io/.

https://fixer.io/#pricing_plan  Esta otra es otra opcion, está limitada a 100 llamadas mensuales gratuitas.
api_key = "f2baf06515a80876d3222353abba6060"  #API key(opcion reserva)
url = f"http://data.fixer.io/api/latest?access_key={api_key}" #url que sirve los datos(opcion reserva)
"""


                            #BLOQUE DE IMPORTACIONES
import requests #se necesita requests instalado con pip para hacer llamada a la API de conversion

from geopy.geocoders import Nominatim
import pgeocode
from timezonefinder import TimezoneFinder
#response = requests.get('https://postal-codes.cybo.com/', verify=False)



                            #BLOQUE DE CAPTURA DE DATOS MEDIANTE API
#weather_response = requests.get(f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&timezone={timezone}&daily=apparent_temperature_max,apparent_temperature_min,precipitation_probability_mean,weathercode,sunrise,sunset&current_weather=true&forecast_days=7')
#weather = weather_response.json()

#RESULTADO DE LA API
weather = {'latitude': 52.52, 'longitude': 13.419998, 'generationtime_ms': 0.8310079574584961, 'utc_offset_seconds': 7200, 'timezone': 'Europe/Berlin', 'timezone_abbreviation': 'CEST', 'elevation': 38.0, 'current_weather': {'temperature': 21.2, 'windspeed': 5.8, 'winddirection': 274, 'weathercode': 0, 'is_day': 1, 'time': '2023-09-04T12:00'}, 'daily_units': {'time': 'iso8601', 'apparent_temperature_max': '°C', 'apparent_temperature_min': '°C', 'precipitation_probability_mean': '%', 'weathercode': 'wmo code',
'sunrise': 'iso8601', 'sunset': 'iso8601'}, 'daily': {'time': ['2023-09-04', '2023-09-05', '2023-09-06', '2023-09-07', '2023-09-08', '2023-09-09', '2023-09-10'], 'apparent_temperature_max': [25.1, 27.0, 28.7, 27.3, 27.6, 29.8, 30.0], 'apparent_temperature_min': [11.0, 14.3, 14.7, 16.2, 16.1, 17.1, 15.3], 'precipitation_probability_mean': [0, 0, 0, 0, 0, 0, 3], 'weathercode':
[45, 3, 1, 3, 1, 0, 45], 'sunrise': ['2023-09-04T06:22', '2023-09-05T06:23', '2023-09-06T06:25', '2023-09-07T06:27', '2023-09-08T06:28', '2023-09-09T06:30', '2023-09-10T06:32'], 'sunset': ['2023-09-04T19:48', '2023-09-05T19:46', '2023-09-06T19:44', '2023-09-07T19:41', '2023-09-08T19:39', '2023-09-09T19:37', '2023-09-10T19:34']}}

"""latitude = 42.653101
longitude = -8.879068
timezone = "Europe/Berlin"
"""

#url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&timezone={timezone}&daily=temperature_2m_1h,precipitation_probability_mean,weathercode,sunrise,sunset&current_weather=true&forecast_days=7"

def geocode_location(location):
    geolocator = Nominatim(user_agent="weather_app")
    location_data = geolocator.geocode(location)
    if location_data:
        latitude = location_data.latitude
        longitude = location_data.longitude
        return latitude, longitude
    else:
        return None

def geocode_postal_code(postal_code):
    geocoder = pgeocode.Nominatim('es')
    location_data = geocoder.query_postal_code(postal_code)
    if not location_data.empty:
        latitude = location_data.latitude
        longitude = location_data.longitude
        return latitude, longitude
    else:
        return None
    
def is_postal_code(input_value):
    nomi = pgeocode.Nominatim('ES')
    location = nomi.query_postal_code(input_value)
    if location.empty:
        return False #el codigo postal no es valido
    else: 
        return True #el codigo postyal es valido

def get_timezone(location):
    coordinates = geocode_location(location)
    if coordinates:
        latitude, longitude = coordinates
        tf = TimezoneFinder()
        timezone = tf.timezone_at(lng=longitude, lat=latitude)
        return timezone
    else:
        coordinates = geocode_postal_code(postal_code)
        if coordinates:
            latitude, longitude = coordinates
            tf = TimezoneFinder()
            timezone = tf.timezone_at(lng=longitude, lat=latitude)
            return timezone
        else:
            return None


def get_weather(latitude, longitude, timezone):
    #city = request.args.get('city')
    #weather_response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid=097cb4956829efc4877aa5dd20140f59')
    #weather = weather_response.json()
    #forecast_text = f'El pronóstico del tiempo para {city} es: {weather["weather"][0]["description"]}.'
    #print(weather)

    city = "madrid"

    print(weather)
    # convertir el pronóstico del tiempo a texto
    #forecast_text = f'El pronóstico del tiempo para {city} es: {weather["current_weather"]["winddirection"]}.'
    #print(forecast_text)

#----------------------LOGICA---------------------
input_value = input("Introduce tu Ciudad o código postal: ")

location, postal_code = is_postal_code(input_value)

latitude, longitude = geocode_location(location), geocode_postal_code(postal_code)

timezone = get_timezone(location)
if not timezone:
    timezone = get_timezone(postal_code)

get_weather(latitude, longitude, timezone)


#RESULTADO DE LA API
{'latitude': 52.52, 'longitude': 13.419998, 'generationtime_ms': 0.8310079574584961, 'utc_offset_seconds': 7200, 'timezone': 'Europe/Berlin', 'timezone_abbreviation': 'CEST', 'elevation': 38.0, 'current_weather': {'temperature': 21.2, 'windspeed': 5.8, 'winddirection': 274, 'weathercode': 0, 'is_day': 1, 'time': '2023-09-04T12:00'}, 'daily_units': {'time': 'iso8601', 'apparent_temperature_max': '°C', 'apparent_temperature_min': '°C', 'precipitation_probability_mean': '%', 'weathercode': 'wmo code',
'sunrise': 'iso8601', 'sunset': 'iso8601'}, 'daily': {'time': ['2023-09-04', '2023-09-05', '2023-09-06', '2023-09-07', '2023-09-08', '2023-09-09', '2023-09-10'], 'apparent_temperature_max': [25.1, 27.0, 28.7, 27.3, 27.6, 29.8, 30.0], 'apparent_temperature_min': [11.0, 14.3, 14.7, 16.2, 16.1, 17.1, 15.3], 'precipitation_probability_mean': [0, 0, 0, 0, 0, 0, 3], 'weathercode':
[45, 3, 1, 3, 1, 0, 45], 'sunrise': ['2023-09-04T06:22', '2023-09-05T06:23', '2023-09-06T06:25', '2023-09-07T06:27', '2023-09-08T06:28', '2023-09-09T06:30', '2023-09-10T06:32'], 'sunset': ['2023-09-04T19:48', '2023-09-05T19:46', '2023-09-06T19:44', '2023-09-07T19:41', '2023-09-08T19:39', '2023-09-09T19:37', '2023-09-10T19:34']}}

#keys = list(divisas['rates'].keys()) #se cogen los nombres de las divisas y se meten en una lista donde poder comparar si están las elegidas por el usuario

#diccionario de divisas ordenadas alfabeticamente por su nombre en castellano


#impresion de bienvenida
print(">")
print("""Bienvenido a su calculadora de divisas. 

Introduciendo la CANTIDAD, 
el codigo de su MONEDA
y el codigo de la DIVISA a la que la desea convertir,
obtendrá el valor correspondiente.""")

        #/////////////////////////#
        #// ##   FUNCIONES   ## //#         
        #/////////////////////////#

#Listado de funciones: comprobar_cantidad_moneda (recoge la cantidad de moneda a convertir y evalua la calidad de los datos), comprobar_divisa(recoge las monedas introducidas por el usuario, asegura la calidad de los datos y devuelve separados el nombre y el valor de la moneda. Se usa tanto para obtener la moneda como la divisa.)

#funcion para obtener el dato de cantidad correcto
def comprobar_cantidad_moneda(cantidad_moneda): 
    moneda_correcta = False #variable de control para el bucle
    while not moneda_correcta: #el bucle se ejecuta siempre que la variable sea true
        cantidad_moneda_auxiliar = cantidad_moneda.replace(",", "").replace(".", "")#se eliminan posibles punto o coma para comprobar que sean solo digitos y por lo tanto pueda convertirse a un numero
        try: #iniciamos un try para poder capturar posibles errores
            if cantidad_moneda_auxiliar.isnumeric(): #se comprueba que la variable sea numerica
                cantidad_moneda = float(cantidad_moneda.replace(",", ".")) #se asigna a la variable un numero float valido, con un punto si lo tuviese
                moneda_correcta = True #se convierte la variable a true para cerrar el bucle
            else:
                raise ValueError #se lanza una excepcion si no se ha introducido un numero
        except ValueError:
            print()
            cantidad_moneda = input("Por favor, utilice valores numericos. Introduzca la cantidad nuevamente: ") #Se solicita de nuevo el dato tras notificar el error en la introduccion
            print()
    return cantidad_moneda #se devuelve el valor correcto

#funcion para obtener tanto la moneda como la divisa
def comprobar_divisa():
    divisa_usuario = "" 
    divisa_correcta = False #variable de control para el bucle
    while not divisa_correcta: #el bucle se ejecuta siempre que la variable no sea true
        if divisa_usuario in keys:
            nombre_divisa_usuario = divisas['rates'][divisa_usuario] #se asigna el valor de la divisa a una variable
            divisa_correcta = True #se convierte la variable a true para cerrar el bucle
        
           
        else:
            print()
            divisa_usuario = input("""     
Por favor, introduzca una moneda en formato codigo ISO, por ejemplo EUR.                   
Si desea ver un listado de los codigos ISO de las monedas pulse 1: 
 """).upper() #input para solicitar datos forzados a mayusculas
            print()
        if divisa_usuario == "1": #si el dato introducido en el input es 1 se le muestra un diccionario con los codigos ISO
            print(diccionario_currencies)

            
            
    return (divisa_usuario, nombre_divisa_usuario) #devuelve los valores

## MEJORAR LEGIBILIDAD DE RETORNO POR PANTALLA (MILLARES SEPARADOS POR PUNTOS, DECIMALES POR COMAS) ##
def prettify_number(numero: float):
    
    #Saneamos valores de entrada
    try:
        numero=float(numero)
    except ValueError:
        return str(numero)

    #Pasamos número a cadena para poder trabajar con él
    numero=str(numero)

    #Separamos parte entera de parte decimal
    [n, d]=(numero).split(".")

    #Invertimos la cadena entera
    n=n[::-1]

    #Viajamos por la cadena, insertando un punto cada tres dígitos
    j=0
    m=[]
    for i in n:
        if j==3:
            m.append(".")
            j=1
        else:
            j+=1

        m.append(i)
    #Convertimos la lista en cadena y volvemos a invertir        
    m="".join(m)[::-1]

    #Si es decimal, añadimos coma y parte decimal; si no, nos quedamos solo con la parte entera
    if d!="0":
        m=m+","+d
    
    return m

                        #//////////////////////////////////#
                        #//##  MOTOR DE LA APLICACION  ##//#         
                        #//////////////////////////////////#

#variable para controlar el bucle principal
nueva_operacion = "s" 
#variable para realizar pruebas e ir imprimiendo datos para control
debuggin = True

#se realiza un bucle para controlar que una posible nueva operacion
while nueva_operacion == "s": #bucle mientras la nueva operacion es un si ("s") a una nueva operacion por parte de usuario
    if nueva_operacion == "n": #si la eleccion del usuario es no (n) se cierra la aplicacion
        print()
        print("Gracias por utilizar su calculadora de divisas.¡Hasta la proxima!") #impresion de despedida
        print()
    else:
        #se solicitan datos de capital al usuario
        print(">")
        cantidad_moneda = comprobar_cantidad_moneda(input("Por favor introduzca la cantidad que desea convertir: ")) #input para recibir el capital del usuario, que inmediatamente es gestionado por la funcion correspondiente
        print()
        print( "Usted ha seleccionado", prettify_number(cantidad_moneda), "como cantidad.") #impresion de confirmación para el usuario
        
        
        #input para recibir el tipo de divisa del usuario
        nombre_divisa_usuario, divisa_usuario = comprobar_divisa() #se pasan datos a dos variables llamando a la funcion
        nombre_moneda_usuario, moneda_usuario = nombre_divisa_usuario, divisa_usuario #se convierten los datos recibidos de la funcion a los necesarios en la primera parte de la formula de calculo de conversion
        
        print()
        print( "Usted ha seleccionado", nombre_moneda_usuario, "como moneda.") #impresion de confirmación para el usuario
       
        
        nombre_divisa_usuario, divisa_usuario = comprobar_divisa() #se pasan datos a dos variables llamando a la funcion, estas dos variables son necesarios en la segunda parte de la formula de calculo de conversion
        
        print()
        print( "Usted ha seleccionado", nombre_divisa_usuario, "como divisa.") #impresion de confirmación para el usuario
        print()
        
        
        
        #se realizan los calculos necesarios
        cambio_divisa = round(cantidad_moneda * (1/divisas['rates'][nombre_moneda_usuario]) * divisas['rates'][nombre_divisa_usuario],5) #se realiza la conversion y se redondea el resultado a 5 decimales
        valor_unidad_divisa = divisas['rates'][nombre_divisa_usuario] / divisas['rates'][nombre_moneda_usuario]#se calcula el valor de una unidad de su moneda a divisa
        valor_unidad_moneda = divisas['rates'][nombre_moneda_usuario] / divisas['rates'][nombre_divisa_usuario]#se calcula el valor de una unidad de la divisa en su moneda
        #FORMULA: Valor de la moneda de destino = Valor de la moneda de origen * (1 / Valor de la moneda de origen respecto al euro) * Valor de la moneda de destino respecto al euro

        
        #se imprime el resultado
        print()
        print("El valor de 1", nombre_moneda_usuario,"es de", prettify_number(valor_unidad_divisa), nombre_divisa_usuario) #impresion de resultado para valor de una sola unidad, con funcion prettify intedrada
        print()
        print("El valor de 1", nombre_divisa_usuario,"es de", prettify_number(valor_unidad_moneda), nombre_moneda_usuario) #impresion de resultado para valor de una sola unidad, con funcion prettify intedrada
        print()
        print("El cambio de", prettify_number(cantidad_moneda), nombre_moneda_usuario,"es de", prettify_number(cambio_divisa), nombre_divisa_usuario) #impresion de resultado para valor de la cantidad solicitada, con funcion prettify intedrada
        print()
        
    
    #se consulta si se desea realizar una nueva operacion  
    nueva_operacion = str(input("Desea realizar una nueva consulta? S/n Teclee s ó n: ")).lower() #input consultando posible nueva operacion o cierre forzado a minusculas para que coincida con el dato almacenado en la variable

    if nueva_operacion == "n": #valor para cierre de la aplicacion
        print()
        print("Gracias por utilizar su calculadora de divisas.¡Hasta la proxima!") #impresion de despedida
        print()
        


