import csv
import os

# Vemos si el directorio principal existe o no para crearlo. Si ya existe no lo vamos a borrar.
def createDirectory (path_toCreate):
        
    '''
    Función para crear el directorio principal si no existe.

    Parameters
    ----------
    path_toCreate: str
        Ruta del directorio.

    '''

    if not os.path.exists(path_toCreate) or not os.path.isdir(path_toCreate):
        os.makedirs(path_toCreate)


def writeFile(dataset,headers,pathFile):

	"""
	Función para crear y escribir un fichero csv.

    Parameters
    ----------
    pathFile: str
        Ruta del fichero.
    dataset: dict
        Datos para escribir en el csv.
    headers: list
    	Cabeceras de las columnas
	"""

	try:

		with open(pathFile,'w', newline='', encoding='utf-8') as f_write:

			writer = csv.writer(f_write)

			writer.writerow(headers)

			for row in dataset:
				writer.writerow(row.values())

	except FileNotFoundError as e:

		print("Error al abrir el fichero {} ".format(e))
