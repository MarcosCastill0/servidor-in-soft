import json
from wsgiref.simple_server import make_server

tasks = []
next_id = 1 #Contador para ID unicos de c/tarea

def function(environ, start_response):
    
    ruta = environ.get("PATH_INFO" , "")
    verbo = environ.get("REQUEST_METHOD" , "")

    if verbo == "GET" and ruta == "/tasks":
        status = "200 Ok"
        headers = [("content-Type" , "application/json")] #Respuesta en JSON
        start_response(status, headers)
        body = json.dumps(tasks).encode("utf-8")
        return [body] #Convierte la lista a JSON

#Leer paquete recibido
    if verbo == "POST" and ruta == "/tasks":
        size = int(environ.get("CONTENT_LENGTH" , 0) or 0) #or 0 Por si viene vacia
        unprocessed_body = environ["wsgi.input"].read(size)
        body_info = json.loads(unprocessed_body) #Convierte JSON

#Crear la nueva tarea y agg a la lista 
        global next_id
        new_tasks = {}
        new_tasks["id"] = next_id
        new_tasks["title"] = body_info.get("title" , "")
        new_tasks["description"] = body_info.get("description" , "")

        tasks.append(new_tasks)
        next_id += 1

#Creacion de la respuesta 
        status = "201 Created"
        headers = [("content-Type" , "application/json")] #Respuesta en JSON
        start_response(status, headers)
        body = json.dumps(new_tasks).encode("utf-8")
        return [body] #Convierte la lista a JSON

#Ver una tarea especifica con su ID
    if verbo == "GET" and ruta.startswith("/tasks/"):
        id_texto = ruta.replace("/tasks/" , "")
        id_tarea = int (id_texto)

        tarea_encontrada = None
        for t in tasks:
            if t["id"] == id_tarea:
                tarea_encontrada = t

        if tarea_encontrada is None:
            status = "404 Not Found"
            headers = [("Content-Type" , "application/json")]
            start_response(status , headers)
            body = json.dumps({"error": "404 Not Found"}).encode("utf-8")
            return [body]

        status = "200 Ok"
        headers = [("Content-Type" , "application/json")]
        start_response(status , headers)
        body = json.dumps(tarea_encontrada).encode("utf-8")
        return [body]

    if verbo == "PATCH" and ruta.startswith("/tasks/"):
        id_texto = ruta.replace("/tasks/" , "")
        id_tarea = int(id_texto)

        tarea_encontrada = None 

        for t in tasks:
            if t["id"] == id_tarea:
                tarea_encontrada = t
        
        if tarea_encontrada is None:
            status = "404 Not Found"
            headers = [("Content-Type" , "application/json")]
            start_response(status , headers)
            body = json.dumps({"error": "404 Not Found"}).encode("utf-8")
            return [body]

        size = int(environ.get("CONTENT_LENGTH" , 0) or 0)
        unprocessed_body = environ["wsgi.input"].read(size)
        cambios = json.loads(unprocessed_body)

        for clave in cambios:
            tarea_encontrada[clave] = cambios[clave]

        status = "200 Ok"
        headers = [("Content-Type" , "application/json")]
        start_response(status , headers)
        body = json.dumps(tarea_encontrada).encode("utf-8")
        return [body]

    if verbo == "DELETE" and ruta.startswith("/tasks/"):
        id_texto = ruta.replace("/tasks/" , "")
        id_tarea = int(id_texto)

        tarea_encontrada = None 
        for t in tasks:
            if t["id"] == id_tarea:
                tarea_encontrada = t

        if tarea_encontrada is None:
            status = "404 Not Found" 
            headers = [("Content-Type" , "application/json")]
            start_response(status , headers)
            body = json.dumps({"error": "404 Not Found"}).encode("utf-8")
            return [body]
        
        tasks.remove(tarea_encontrada)

        status = "200 Ok"
        headers = [("Content-Type" , "application/json")]
        start_response(status , headers)
        body = json.dumps({"message": "Task deleted successfully"}).encode("utf-8")
        return [body]

    #Si no coincide retorna 404 en JSON
    status = "404 Not Found"
    headers = [("Content-Type" , "application/json")]
    start_response(status , headers)
    body = json.dumps({"error": "404 Not Found"}).encode("utf-8")
    return [body]

if __name__ == "__main__":
    with make_server("" , 9292 , function) as server:
        print("Servidor en el puerto 9292")
        server.serve_forever()