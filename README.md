# servidor-in-soft

###
Construir un servidor HTTP en Python usando solo wsgiref.simple_server (sin frameworks como Flask), que administre una lista de tareas en memoria y soporte los cuatro verbos HTTP principales:

GET /tasks → devuelve todas las tareas (200 OK)
GET /tasks/{id} → devuelve una tarea puntual (200 o 404 si no existe)
POST /tasks → crea una tarea nueva con el JSON recibido (201 Created)
PATCH /tasks/{id} → modifica solo los campos enviados, sin tocar el resto (200 o 404)
DELETE /tasks/{id} → elimina una tarea (200/204 o 404)

Todo en un único archivo server.py, corriendo en 
http://localhost:9292.

Recibir y responder en JSON (json.loads / json.dumps), con header Content-Type: application/json.

Devolver los códigos de estado correctos según cada verbo.
Que PATCH sea realmente parcial (no reemplace la tarea entera).

Probar todo con curl (o el script demo-verbos-http.sh) y guardar la evidencia (por ejemplo en evidencia.txt), mostrando que después de un DELETE, un GET a esa tarea devuelve 404.

GET = Mostrame 
Solo lee, nunca modifica nada en el servidor. Repetirlo infinitamente siempre da el mismo resultado.
GET /tasks/1 "mostrar la tarea 1"

POST = Crea uno nuevo 
Crea un nuevo recurso cada vez que se llama. Repetirlo no da el mismo resultado: cada llamada genera algo distinto. 
POST /tasks "Comprar pan" si lo mando dos veces, quedan dos tareas separadas (id distintos entre tareas)

PATCH = Cambia solo esto 
Modifica parcialmente un recurso existente, solo cambiando los campos que le mando. Repetirlo con los mismos datos deja todo igual, no cambia nada mas
PATCH /tasks/1 {"done": true} la tarea 1 queda marcada como hecha. Si lo mando de nuevo, sigue igual de "hecha", no pasa nada distinto

DELETE = Borralo 
Borra un recurso. Repetirlo sobre algo ya borrado no cambia nada, sigue estado borrado. 
DELETE /tasks/1 borra la tarea 1. Si lo mando otra vez, la tarea sigue sin existir, no hay ningun cambio nuevo. 
###