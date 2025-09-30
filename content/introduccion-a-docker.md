# Introducción a Docker

<!-- author: Néstor Jimeno -->
<!-- date: 2025-02-20 -->
<!-- tags: Docker, Desarrollo de software -->
<!-- language: spanish -->

## Introducción

Docker es una herramienta que permite empaquetar aplicaciones y sus dependencias en **contenedores** ligeros, asegurando que funcionen de la misma manera en cualquier sistema. 
 
Estos contenedores proporcionan un **entorno aislado** que garantiza que la aplicación se ejecute de manera consistente en cualquier sistema, ya sea en desarrollo, pruebas o producción. Al eliminar las diferencias entre los entornos, Docker facilita la colaboración y mejora la eficiencia, permitiendo a los desarrolladores centrarse en el código sin preocuparse por los problemas de compatibilidad.

## ¿Qué es un contenedor?
 
Un **contenedor** en Docker es una unidad ligera y portátil que encapsula una aplicación junto con todas sus dependencias. Cada contenedor es una instancia aislada basada en una **imagen**, con su propio sistema de archivos, variables de entorno y red.

A diferencia de las máquinas virtuales, que requieren un sistema operativo completo para cada instancia, los contenedores comparten el kernel del sistema operativo anfitrión, lo que los hace más eficientes.

## ¿Qué es una imagen?

Una **imagen** Docker es una plantilla que contiene todo lo necesario para ejecutar una aplicación: código, dependencias, configuraciones y un sistema de archivos mínimo.

Las imágenes sirven como base para crear **contenedores**, que son instancias en ejecución de esas imágenes. Podemos pensar en las imagenes como cuando en 
programación utilizamos clases. Una imagen es una clase y un contenedor es una instancia de esa clase. Podemos crear muchos contenedores a partir de una imagen, 
de la misma manera que podemos crear muchos objetos a partir de una clase.

En el caso de que hayas descargado ya alguna imagen, puedes listarlas con:

```bash
docker images
```

Más adelante veremos cómo crear imagenes propias y cómo descargar imagenes creadas por otros.

## Iniciar un contenedor

Imagina que quieres ejecutar un sistema **Ubuntu** y abrir una terminal, bastará con hacer lo siguiente:

```bash
docker run -it ubuntu bash
```

¿Qué es lo que pasa?

En primer lugar, Docker busca en el sistema la **imagen** `ubuntu` y, si la tienes, lo arranca. Si no la encuentra, la tiene
que descargar primero. Estas descargas, Docker las hace desde el **Docker Hub**, que contiene tanto imagenes oficiales que Docker se 
encarga de publicar y mantener como imágenes que publican personas independientes. 

Después, creará un contenedor y lo ejecutará. El flag `-it` se usa para indicar lo siguiente:

- `-i`: *interactive*, mantiene la entrada estándar (`stdin`) abierta para interactuar con el contenedor.
- `-t`: asigna una terminal virtual para mejorar la interacción con el contenedor.

Es decir, que la instrucción anterior inicia un contenedor con la imagen oficial de Ubuntu y abre una terminal dentro de él. Con esto, tengo un contenedor 
ejecutándose. Puedes comprobarlo con el siguiente comando, que te muestra una lista de los contenedores en ejecución:

```bash
docker ps
```

Te dará una salida de este tipo:

```bash
CONTAINER ID   IMAGE    COMMAND       CREATED        STATUS       PORTS    NAMES
a1b2c3d4e5f6   ubuntu   "/bin/bash"   5 minutes ago  Up 5 mins             my_container
```

Si le añades el flag `-a` te mostrará todos los contenedores, incluidos los que ya se han parado.

Para detener el contenedor que acabo de ejecutar, es tan sencillo como hacer:

```bash
docker stop CONTAINER-ID
```

Hasta ahora, sólo hemos instanciado un contenedor, pero una vez que se ha hecho eso, no es necesario repetirlo. Con el comando anterior, el contenedor quedará parado, pero no se eliminará. Puedes volver a arrancarlo, en vez de instanciar uno nuevo, con el comando `start`, pasándole también la flag `-i` para que sea interactivo:

```bash
docker start -i CONTAINER-ID
```

Si quiero ver si ha habido algún problema, necesito consultar los *logs*. Para eso:

```bash
docker logs -f CONTAINER-ID
```

El flag `-f` permite ver los *logs* en continuo, pero es opcional.

Si en algún momento has terminado de trabajar con un contenedor y quieres eliminarlo, tendrás que utilizar el siguiente comando.

```bash
docker rm CONTAINER-ID
```

Esto elimina el contenedor, lo borra completamente. Es importante tener claro la diferencia entre `rm` y `stop`. Cuando se para un contenedor, se  puede volver a arrancar con el comando `start`, pero cuando se borra, se elimina completamente él y toda la información que tiene asociada (si no se  ha creado un volumen, como veremos en otro artículo).

