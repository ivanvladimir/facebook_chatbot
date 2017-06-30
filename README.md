# facebook_chatbot

Chatbot webhooks para facebook

## Instalación

Para obtener el código puede clonarlo o bajarlo

### Clonar

    git clone git@github.com:ivanvladimir/facebook_chatbot.git

### Bajarlo

Bajarlo de a 
[aquí](https://github.com/ivanvladimir/facebook_chatbot/archive/master.zip)

Descomprimir

## Habilitar virtualenv

Instalar virtualenv

    sudo apt install virtualenv

Activar virtualenv en el directorio con el código

    source facebook_chatbot/bin/activate

## Instalar los requierements

En el directorio del código hacer

    pip install -r requierements.txt

## Habilitar _ngrok_

_ngrok_ es una herramienta de tunel que nos permitirá exponer nuestro servicio 
en una dirección url pública

    1. Obtenerlo [aquí](https://ngrok.com/download)
    2. Descomprimir
    3. Ejecutar 

        ./ngrok 5000

    4. Al ejecutarse te dará una dirección publica, con esa hay que configurar 
       el chatbot en facebook

Nota, en caso de usar otro puerto, registrarlo de esa forma.

## Chatbot en Facebook

    1. Crear una Página de Facebook
    2. Registrarse como desarrollador
    3. Crear una nueva aplicación
    4. Activar el servicio de messenger para dicha aplicación
    5. Asignar token de verificación, y obtener token de acceso al archivo de 
       configuración
    6. Probar en el chat de la página


## Ejecutarlo

Para ejecutarlo de forma normal
    
    python app.py 

Despues de esto ir al navegador y la siguiente dirección: http://127.0.0.1:5000/

Para ejecutarlo con un archivo específico:


    python app.py --aiml NOMBRE_ARCHIVO
