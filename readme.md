# Cronometrador de vueltas

## Contexto
En las carreras de [automovilismo chilote](https://www.instagram.com/automovilismochilote/) hace falta un cronometrador de vueltas.

Esta es una implentación en micropython sobre ESP32 y ya veremos que más (web back end). El plan es ponerlo en operación en un carrera antes que acabe el 2025.

![Diagrama alto nivel](/docs/images/diagram.svg "Diagrama alto nivel")

## instrucciones para desarrolladores
### Setup
Necesitas:
 - un entorno python (ej: `conda create -n mpy312 python=3.12`)
 - [mpremote](https://docs.micropython.org/en/latest/reference/mpremote.html) (`pip install mpremote`)
 - driver on windows?
  - [esp-idf](https://github.com/espressif/esp-idf) (opcional recomendado)

 ### Comandos

 #### Copiar del computador al microcontrolador

 ```mpremote fs cp transmiter.py :main.py```

#### Copiar del microcontrolador al computador

 ```mpremote fs cp :main.py transmiter.py```

 #### Corrar TODO el microcontrolador

```esptool.py erase_flash```

#### Instalar micropython en el microcontrolador

```esptool --chip esp32 write_flash -z 0x1000 ~/Downloads/ESP32_GENERIC-20250911-v1.26.1.bin```