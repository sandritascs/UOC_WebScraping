import requests
from bs4 import BeautifulSoup

# Variable global para user agent de las peticiones
global headers
headers = {'User-Agent': 'Mozilla/5.0'}

def getAmenaza(html):

	"""
    Función para obtener el grado de amenaza

    Parameters
    ----------
    html: str
        html con la etiqueta img

    Return
    ---------
    grado: str
    	Grado de amenaza en clasificación animal

    """

    # De la url obtengo la parte final
	url_grado_parts = html.img["data-lazy-src"].split("/")
	last_part = url_grado_parts.pop()

	# Cojo el número del nombre de la imagen que indica el grado de amenaza
	number = [int(temp) for temp in last_part if temp.isdigit()]

	grado = ''

	if number[0] == 1:
		grado = 'NE'
	elif number[0] == 2:
		grado = 'DD'
	elif number[0] == 3:
		grado = 'LC'
	elif number[0] == 4:
		grado = 'NT'
	elif number[0] == 5:
		grado = 'VU'
	elif number[0] == 6:
		grado = 'EN'
	elif number[0] == 7:
		grado = 'CR'
	elif number[0] == 8:
		grado = 'EW'
	elif number[0] == 9:
		dgrado = 'EX'

	return grado


def getDataAnimal (animal_url, name):

	"""
    Función para obtener los datos de la url de cada animal

    Parameters
    ----------
    animal_url: str
        Url del animal.
    name: str
        Nombre del grupo al que pertenece el animal

    Return
    ---------
    dataAnimal: dict
    	Diccionario con los atributos de cada animal

    """

	dataAnimal = {}

	# Descargamos el html del animal.
	animal_page = requests.get(animal_url, headers=headers)
	soup_animal = BeautifulSoup(animal_page.content, 'html.parser')

	# Para obtener la zona, partimos la url y la cogemos de la posición necesaria.
	url_parts = animal_url.split("/")

	# Leemos las etiquetas necesarias para ver los atributos del animal
	count_caract = 1
	for item in soup_animal.article.find_all('div',{"class":"box-ficha-animal--caracteristica"}):

		all_p = item.find_all('p')

		for content in all_p:

			if count_caract == 1:
				dataAnimal['nombre_comun'] = content.string
			elif count_caract==2:
				dataAnimal['especie'] = content.string
			elif count_caract==3:
				dataAnimal['familia'] = content.string
			elif count_caract==4:
				dataAnimal['orden'] = content.string
			elif count_caract==5:
				dataAnimal['clase'] = content.string
			
		count_caract = count_caract + 1

	dataAnimal['grupo'] = name
	dataAnimal['zona'] = url_parts[4]

	# Obtenemos las características
	for item in soup_animal.article.find_all('div',{"class":"vc_tta-panel"}):

		dataAnimal[item['id']] = item.p.string


	# Grado amenaza
	'''
	Hay 9 categorias, desde la 1 que es NE hasta la 9 que es EX
	'''
	item_grado = soup_animal.article.find('div', {"class":"box-grado-amenaza--image"})
	
	dataAnimal['grado_amenaza'] = getAmenaza(item_grado)


	return dataAnimal

def getWebData(webUrl):

	"""
    Función para obtener los datos de la url principal

    Parameters
    ----------
    webUrl: str
        Url principal para descargar

    Return
    ---------
    listAnimals: list
    	Lista de animales. Es el dataset final.

    """
	
	# Descargamos la página
	page = requests.get(webUrl, headers=headers)

	# Formateamos con la librería BeautifulSoup
	soup = BeautifulSoup(page.content, 'html.parser')

	# Leemos las etiquetas donde se encuentran las url de cada animal
	clasification = soup.find_all('div', {"class":"box-clasificacion-animales"})

	count = 0
	listAnimals = []
	for eachClass in clasification:

		# nombre del grupo
		name = eachClass.h2.span.string		

		'''
		Obtenemos los links de cada animal y llamamos a la función para leer y obtener
		los datos de cada url y lo añadimos a la lista.
		'''
		for li in eachClass.find_all('a'):

			url_animal = li.get('href')			
			dataAnimal = getDataAnimal(url_animal,name)
			listAnimals.append(dataAnimal)
			count = count + 1

	print("Total animals {}".format(count))

	return listAnimals



