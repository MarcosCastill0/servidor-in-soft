from wsgiref.simple_server import make_server

def app(environ, start_response):
    status = "200 OK"
    headers = [("Content-Type", "text/plain")]
    start_response(status, headers)

    # Leyendo el environ (diccionario) captura la ruta y el verbo 
    ruta = environ.get("PATH_INFO", "") 
    verbo = environ.get("REQUEST_METHOD", "")

    msg = f"ruta: {ruta}, verbo: {verbo}"
    return [msg.encode("utf-8")]

if __name__ == "__main__":
    with make_server("", 9292, app) as server:
        print("Servidor en el puerto 9292")
        server.serve_forever()

"""
Levantamos server sin librerias externas y luego creamos la funcion 
app que procesa cada peticion. __name__ == "__main__": garantiza que 
solo se ejecuta al correr este archivo directamente, make server crea 
el servidor y luego server forever lo deja encendido esuchando peticiones
"""
