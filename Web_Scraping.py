# -- ¡¡¡IMPORTANTE!!! --
# Antes de ejecutar deben instalarse las librerías requests y BeautifulSoup desde la terminal. 
# Para ello, teniendo en cuenta que la versión de Python es 3.12, deben ejecutarse:
# >> pip installs requests
# >> pip installs bs4
# ----- LIBRERÍAS -----
# Se importa la librería requests para realizar la petición de conexión a la página web
import requests
#Se importa la librería Beautiful para realizar Web Scraping sobre la página web
from bs4 import BeautifulSoup
# ----- VARIABLES -----
# Estas variables representan los colores con los que se van a mostrar los mensajes por terminal
azul = "\33[1;36m"
blanco = "\33[1;37m"
amarillo = "\33[0;33m"
# ----- PROCEDIMIENTOS -----
def datos_Scraping(url):
    # ----- DEFINICIÓN DE LA PETICIÓN -----
    # Se inicializa el diccionario donde se almacenan las variables a extraer y sus valores
    d={}
    # Se definen las cabeceras para la petición. Desde el modo inspeccionar del navegador se puede obtener el user-agent que utiliza
    headers = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"}
    # Se realiza la petición con la que se extraen los datos
    # Para ello, se muestra un mensaje por terminal indicando sobre qué url se va a realizar la petición
    print(f'{azul}Realizando la petición: {amarillo}{url}{blanco}')
    # Se crea la petición con la url y las cabeceras definidas previamente. Además, se añade un timeout por si tardase demasiado tiempo en ejecutar la petición
    req = requests.get(url, headers=headers, timeout=10)
    # Se imprime el código de respuesta obtenido de la petición
    print(f'{azul}Código de respuesta...: {amarillo}{req.status_code} {req.reason}{blanco}')
    # En caso de que la petición no sea exitosa
    if req.status_code != 200:
        # Salta una excepción con el mensaje de error y el código de estado correspondientes
        return {"error" : f"{req.reason}", "status_code" : f"{req.status_code}"}
    # Si todo va bien, se procede a extraer los datos mediante Web Scraping
    # ----- EXTRACCIÓN DE DATOS SIN BEAUTIFULSOUP -----
    # Existen variables que se pueden extraer directamente de la url desde la que se realiza la petición, como es el caso de la url del producto o el id del producto
    # Para extraer la url del producto, simplemente se extrae la url de la petición
    d["url"] = req.url
    # El id del producto se localiza al final de la url hasta el caracter '/'. Para extraerlo, se puede obtener la url, partirla por '/' y extraer el último dato 
    d["id"] = d["url"].split("/")[-1]
    # ----- EXTRACCIÓN DE DATOS CON BEAUTIFULSOUP -----
    # Para extraer las siguientes variables se requiere de Web Scraping y, por tanto, de la librería BeautifulSoup. 
    # Para ello, se define el objeto BeautifulSoup a partir del código que se encuentra en req.text y se convierte a HTML con "html.parser" 
    soup = BeautifulSoup(req.text, "html.parser")
    # La extracción de datos se debe hacer de forma minuciosa, inspeccionando la página y averiguando dónde están localizadas
    # El nombre del producto se obtiene de la siguiente manera:
    # - find("tipo de elemento", "nombre de la clase, id u objeto donde se almacene"): Localiza la primera coincidencia en el código HTML
    # - text: Convierte el resultado a texto
    # - strip(): Extrae el dato del texto 
    # Por último, el dato se almacena en el diccionario
    d["nombre_producto"] = soup.find("h2", class_="product-title").text.strip()
    # La url de la imagen del producto se obtiene de la siguiente manera:
    # - find("tipo de elemento", "nombre de la clase, id u objeto donde se almacene"): Localiza la primera coincidencia en el código HTML
    # - attrs: Obtiene todos los parámetros que se encuentran almacenados en el objeto localizado
    # - get("donde se encuentra el dato"): Extrae el dato concreto de todos los parámetros extraídos con la instrucción anterior
    # Por último, el dato se almacena en el diccionario
    d["url_imagen"] = soup.find("img", id="product-cover").attrs.get("src")
    # Las plataformas del producto se obtienen de la siguiente manera:
    # - find("tipo de elemento", "nombre de la clase, id u objeto donde se almacene"): Localiza la primera coincidencia en el código HTML
    # - find_all("tipo de elemento", "nombre de la clase, id u objeto donde se almacene"): Localiza todos los valores que coincidan con la etiqueta, ya que 
    #   puede estar disponible para varias plataformas
    objs_plat = soup.find("dd").find_all("a")
    d["plataformas"] = []
    for item in objs_plat:
        # Por cada elemento que se haya localizado, se extrae y se convierte a texto. Por último, se almacena en la colección
        d["plataformas"].append(item.text.strip())
    # La valoración, como puede estar vacía, se debe tratar con una estructura try/except. Además, en la página desde la que se realiza el ejemplo, la valoración se
    # expresa en estrellas. La puntuación queda almacenada en el objeto HTML que está definido div class = "review-points-4".
    try:
        # Para extraer la valoración se hacen los siguientes pasos:
        # - find("tipo de elemento", "nombre de la clase, id u objeto donde se almacene"): Localiza la primera coincidencia en el código HTML
        # - attrs: Obtiene todos los parámetros que se encuentran almacenados en el objeto localizado
        # - get("donde se encuentra el dato"): Extrae el dato concreto de todos los parámetros extraídos con la instrucción anterior
        c_point = soup.find("a", class_="reviews-points-m").attrs.get("class")[-1]
        # Se extrae la valoración del último lugar de la cadena y se convierte a entero
        puntos = int(c_point[-1])
        # Por último, el dato se almacena en el diccionario como un entero
        d["valoracion"] = int(puntos)
    # Si no hay una valoración, se almacena un objeto vacío
    except:
        d["valoracion"] = None
    # Los precios, como pueden estar vacíos, se debe tratar con una estructura try/except. Además, en la página desde la que se realiza el ejemplo, los precios se
    # encuentran en un mismo objeto, por lo que deben separarse primero y tartarse después.
    # Para ello, se extrae el objeto precio con find()  
    obj_precio = soup.find("div", class_="buy--price")
    try:
        # Para extraer el precio original se hacen los siguientes pasos:
        # - find("tipo de elemento", "nombre de la clase, id u objeto donde se almacene"): Localiza la primera coincidencia en el código HTML
        # - text: Convierte el objeto a texto
        # - replace("dato que se quiere reemplazar", "dato por el que se reemplaza"): Reemplaza los elementos que no son necesarios para convertirlos a float
        # Por último, se convierte el dato a float y se almacena
        d["precio_original"] = float(obj_precio.find("small").text.replace("€","").replace(",","."))
    # Si no hay un precio original (porque no está en stock), se almacena un objeto vacío
    except:
        d["precio_original"] = None
    try:
        # Para extraer el precio actual hay que extraer la parte entera y la parte decimal porque ambas están separadas. 
        # Para la parte entera se hacen los siguientes pasos:
        # - find("tipo de elemento", "nombre de la clase, id u objeto donde se almacene"): Localiza la primera coincidencia en el código HTML
        # - text: Convierte el objeto a texto
        # - strip(): Extrae el dato del texto 
        # - split(): Se separa el dato la parte
        p_int = obj_precio.find("span").text.strip().split("\n")[0].strip()
        # Para la parte decimal se hacen los siguientes pasos:
        # - find("tipo de elemento", "nombre de la clase, id u objeto donde se almacene"): Localiza la primera coincidencia en el código HTML
        # - text: Convierte el objeto a texto
        # - replace("dato que se quiere reemplazar", "dato por el que se reemplaza"): Reemplaza los elementos que no son necesarios para convertirlos a float
        p_dec = obj_precio.find("span", class_="decimal").text.replace("'",".")
        # Por último, se juntan ambos datos, el resultado se convierte a float y se almacena
        d["precio_actual"] = float(p_int + p_dec)
    # Si no hay un precio actual (porque no hay un descuento), se almacena un objeto vacío
    except:
        d["precio_actual"] = None
    # Devuelve el diccionario creado
    return d
# ----- MAIN -----
if __name__ == "__main__":
    # Se define la url de la página web sobre la que se va a realizar Web Scraping
    url = "https://www.game.es/ACCESORIOS/AURICULARES/PC-GAMING/GAME-HX-WPRO-AURICULARES-GAMING-INALAMBRICOS-NEGRO/220178"
    # Se invoca al procedimiento datos_Scraping con la url y los resultados se almacenan en la variable datos
    datos = datos_Scraping(url)
    # Del diccionario resultante se extraen los datos obtenidos y se realiza el tratamiento 
    for clave, valor in datos.items():
        # Para cada clave (que se muestra en mayúsculas), se muestra el valor correspondiente
        print(f'{azul}{clave.upper()}: {amarillo}{valor}{blanco}')
    # Se termina el programa
    exit(0)