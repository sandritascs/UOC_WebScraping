from scraping import getWebData
from utils import createDirectory, writeFile

# Direcciones y ficheros principales.
url = 'https://www.bioparcfuengirola.es/animales/clasificacion-animal/'
directory = '../csv'
file = '../csv/dataset.csv'

# Obtenemos los datos de la web.
datasetFinal = getWebData(url)

# Creamos el directorio si no existe.
createDirectory(directory)

# Cabeceras para el csv
headers = ['nombre_comun', 
			'especie', 
			'familia',
			'orden',
			'clase',
			'grupo',
			'zona',
			'habitat',
			'dieta',
			'gestacion',
			'crias',
			'vida',
			'grado_amenaza'
			]

# Guardamos el dataset en un fichero csv
writeFile(datasetFinal, headers, file)