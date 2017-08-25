# Instalación Python

mkdir virto_assistant

cd virto_assistant

virtualenv env --no-site-packages

source ./enb/bin/activate

## [pocketsphinx](https://github.com/cmusphinx/pocketsphinx) ([CMU Sphinx](https://cmusphinx.github.io/))

> sudo apt-get install -y swig libpulse-dev
> sudo pip install pocketsphinx


## Python speech recognition

> sudo pip install SpeechRecognition
>
> sudo apt-get install libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0
>
> sudo apt-get install ffmpeg libav-tools
> sudo pip install pyaudio

los datos de pocketsphinx

    Bajar los datos del español (por defecto tiene en-US) y ponerlos en:

    <https://sourceforge.net/projects/cmusphinx/files/Acoustic%20and%20Language%20Models/Spanish/>

    env/lib/python2.7/site-packages/speech_recognition/pocketsphinx-data
    app_dir/pocketsphinx-data

        es-ES
            --> language-model.lm.bin
            --> pronounciation-dictionary.dict
            --> acoustic-model
                --> feat.params, mdef, ... variances

    Poner en pronounciation-dictionary.dict las palabras que queramos que se reconozcan y NO existen ya
    virto b i r t o

# Node

## pocketsphinx

[node-pocketsphinx](https://github.com/cmusphinx/node-pocketsphinx)

## node speech recognition

Hay modulos con poco soporte:

- portaudio Node bindings for PortAudio
- jsaudio JsAudio is to Node / JS as PyAudio is to Python


# Google

## [api.ai](https://api.ai/)

- Logueados en google con la cuenta que sea dar permisos
  https://console.api.ai/api-client/#/login
- Crear el agente + intents + ...

[SDKs](https://api.ai/docs/sdks)

[Access tokens](https://api.ai/docs/reference/agent/#using_access_tokens)

    En la configuración del agente hay 2 tokens.

    Caution: Use the developer access token for managing entities and intents and the `client access` token for making queries.

    este token es el que se usa en los SDKs, que internamente lo mandan como: Authorization: Bearer YOUR_ACCESS_TOKEN

python SDK:

    sudo apt-get install python-pyaudio python-numpy
    pip install apiai

node SDK:

    npm install apiai

## [Google Speech api](https://cloud.google.com/speech/)

Python: pip install --upgrade google-api-python-client

[Credenciales](https://developers.google.com/identity/protocols/application-default-credentials)

    Desde la consola se crea una Service account key.
    El JSON de credenciales se tiene que descargar en la máquina que las va a usar (que nadie lo robe :) )

    Poner en la variable de entorno GOOGLE_APPLICATION_CREDENTIALS el path al fichero JSON.

    En python (speechRecognition) se puede pasar directamente el contenido del fichero en el constructor


## Comunicación Python node.js

Usando [0MQ](http://zguide.zeromq.org/)

Se puede usar PUB/SUB para que sea mas sencillo.

Install
    sudo apt-get install libtool pkg-config build-essential autoconf automake uuid-dev
    sudo apt-get install checkinstall

    0MQ version 4.2.2 stable, released on 2017/02/18

    wget https://github.com/zeromq/libzmq/releases/download/v4.2.2/zeromq-4.2.2.tar.gz
    tar -xvzf zeromq-4.2.2.tar.gz

    cd zeromq-4.2.2
    ./configure
    make
    sudo checkinstall
    sudo ldconfig

    Python install:
        pip install pyzmq
