import requests
from bs4 import BeautifulSoup

# URL de la página de Transfermarkt de la selección argentina
url = "https://www.transfermarkt.es/argentinien/startseite/verein/3437"

# Encabezados para la solicitud HTTP
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

# Realizar la solicitud GET a la página
response = requests.get(url, headers=headers)

# Verificar si la solicitud fue exitosa
if response.status_code == 200:
    # Parsear el contenido HTML de la página
    soup = BeautifulSoup(response.content, "html.parser")

    # Encontrar la tabla que contiene la lista de jugadores
    table = soup.find("table", {"class": "items"})

    # Crear un conjunto para almacenar los nombres de los jugadores (evita duplicados)
    jugadores = set()

    # Iterar sobre las filas de la tabla, omitiendo encabezados innecesarios
    for row in table.find_all("tr")[1:]:
        # Encontrar la celda que contiene el nombre del jugador
        name_cell = row.find("td", {"class": "hauptlink"})
        if name_cell:
            # Extraer el texto del nombre y agregarlo al conjunto
            jugador = name_cell.get_text(strip=True)
            jugadores.add(jugador)

    # Generar el contenido HTML
    html_content = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Jugadores de la Selección Argentina</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            h1 { color: #2c3e50; }
            ul { list-style-type: disc; padding-left: 20px; }
            li { margin: 5px 0; }
        </style>
    </head>
    <body>
        <h1>Jugadores de la Selección Argentina</h1>
        <ul>
    """

    # Agregar cada jugador como un elemento de lista
    for jugador in jugadores:
        html_content += f"            <li>{jugador}</li>\n"

    # Cerrar las etiquetas HTML
    html_content += """
        </ul>
    </body>
    </html>
    """

    # Guardar el contenido en un archivo HTML
    with open("jugadores_seleccion_argentina.html", "w", encoding="utf-8") as file:
        file.write(html_content)

    print("Archivo HTML generado: jugadores_seleccion_argentina.html")
else:
    print(f"Error al acceder a la página. Código de estado: {response.status_code}")
