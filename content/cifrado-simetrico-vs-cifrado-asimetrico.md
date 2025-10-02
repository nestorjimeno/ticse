# Cifrado simétrico vs cifrado asimétrico

<!-- author: Néstor Jimeno -->
<!-- date: 2025-10-02 -->
<!-- tags: Criptografía -->
<!-- language: spanish -->

## Cifrado simétrico

El **cifrado simétrico** es un método de criptografía en el que **la misma clave secreta** se utiliza tanto para cifrar, convertir el mensaje en un formato ilegible, como para descifrar, para volverlo a su forma original.

- La **clave secreta** es una secuencia de bits conocida sólo por los participantes autorizados.
- El mensaje original o **plaintext** es el texto, la información, que se quiere proteger.
- El mensaje cifrado o **ciphertext** es el resultado ilegible que se obtiene tras aplicar la clave y el algoritmo de cifrado.

### ¿Cómo funciona el cifrado simétrico?

En primer lugar se genera la clave secreta segura. Por ejemplo en AES (Advanced Encryption Standard), un algoritmo ampliamente usado en la actualidad, se pueden utilizar claves de 128, 192 o 256 bits. La clave debe ser aleatoria y única y su tamaño se debe elegir en función de cada aplicación, ya que cada bit añade complejidad y resistencia frente a ataques de fuerza bruta, pero hace más lentos los cálculos.

Una vez se tiene la clave secreta, se aplica un algoritmo que la combina con el mensaje, convirtiéndolo en datos ilegibles. Este *ciphertext* puede transmitirse incluso por canales inseguros.

Cuando el mensaje llega al receptor, éste aplica **la misma clave** y el **algoritmo inverso** para recuperar el mensaje original.

### Ventajas

El cifrado simétrico es muy rápido, lo que lo hace adecuado cuando se trabaja con grandes volúmenes de datos. Además, sus algoritmos están probados y se consideran eficientes y su consumo de recursos es bajo.

### Desventajas

Todos los participantes deben conocer la clave que se utiliza para encriptar, por lo que hay que compartirla, con el riesgo que eso implica si se intercepta por un agente ajeno. 

Además, la escalabilidad es limitada, ya que para `n` usuarios, se necesitan `n * (n - 1) / 2` claves diferentes.

En la práctica, la desventaja de la "distribución de la clave" se resuelve mediante un **cifrado híbrido**. Se utiliza el [cifrado asimétrico](#cifrado-asimétrico) (como RSA, ECC o Diffie-Hellman) para intercambiar la clave secreta de forma segura. Una vez que la clave simétrica (por ejemplo, para AES) llega de forma segura al destinatario, se utiliza la rapidez del cifrado simétrico para cifrar y descifrar el gran volumen de datos

### AES (Advanced Encryption Standard)

AES es un cifrado por bloques, lo que significa que divide el mensaje en bloques de 128 bits (16 bytes). Cada bloque se cifra de forma independiente aplicando una serie de transformaciones matemáticas usando la clave secreta.

AES puede usar claves de 128 bits (lo más habitual), 192 bits o 256 bits y la longitud de la clave determina el número de rondas de cifrado: 10, 12 o 14 respectivamente.

A partir de la clave original se generan varias subclaves, una para cada ronda, mediante un proceso llamado *Key Expansion*. Este proceso genera tantas claves como se necesiten aplicando una serie de operaciones matemáticas a la subclave anterior.

Cada subclave tiene el mismo tamaño que un bloque (128 bits) y en cada ronda se mezcla con él mediante la operación *AddRoundKey*, combinando la clave con los datos y asegurando que el mensaje cifrado dependa totalmente de la clave secreta.

Los pasos principales para cada ronda son:
- ***SubBytes***: sustitución de cada byte usando una tabla *S-box* para introducir confusión.
- ***ShiftRows***: desplazamiento de las filas de la matriz de bytes para mezclar los datos.
- ***MixColumns***: combinación de columnas mediante operaciones matemáticas para difusión.
- ***AddRoundKey***: aplicación de la subclave mediante XOR.

La última ronda omite *MixColumns*, pero sigue aplicando *AddRoundKey* para garantizar la seguridad.

Por otro lado, como AES es un cifrado simétrico, la misma clave se utiliza para cifrar y descifrar. Por ello, el proceso de desencriptación invierte cada paso del cifrado. Aunque los pasos se aplican “al revés”, la seguridad se mantiene porque cada subclave y operación fue diseñada para ser reversible solo con la clave correcta.

El detalle del proceso de encriptación con AES se ha simplificado en este artículo y no es exacto, simplemente se pretende dar una visión general que sirva como aproximación al mismo.


## Cifrado asimétrico

El **cifrado asimétrico** es un método de cifrado en el que se usan **dos claves diferentes** pero matemáticamente relacionadas:

- **Clave pública** (public key): se puede compartir libremente. Sirve para cifrar información que solo el propietario de la clave privada puede descifrar.

- **Clave privada** (private key): se mantiene en secreto. Sirve para descifrar mensajes que se cifraron con la clave pública correspondiente o para firmar digitalmente.

A diferencia del cifrado simétrico, donde la misma clave se usa para cifrar y descifrar, aquí hay un par de claves con funciones complementarias. El cifrado asimétrico se basa en problemas matemáticos difíciles de resolver que garantizan que, aunque alguien conozca la clave pública, no pueda derivar la clave privada fácilmente, es decir, operaciones fáciles de hacer en una dirección, pero muy difíciles de invertir sin la clave privada.

### ¿Cómo funciona el cifrado asimétrico?

El cifrado asimétrico se puede utilizar para dos procesos diferentes: cifrado de mensajes o firma digital.

El objetivo del cifrado de mensajes es garantizar la confidencialidad de los datos. Para eso, una persona genera un par de claves: clave pública (Kpub) que puede compartir libremente y clave privada (Kpriv), que mantiene en secreto.

Para enviar un mensaje seguro a esta persona, se cifra el mensaje usando su clave pública (Kpub). Esto genera un *ciphertext* ilegible para cualquiera que lo intercepte.

Cuando esta persona recibe el mensaje, usa su clave privada (Kpriv) para descifrarlo. Solo él puede recuperar el mensaje original, ya que sólo él conoce la clave privada.


El objetivo de la firma digital es garantizar autenticidad e integridad, es decir, demostrar que el mensaje proviene realmente del remitente y no ha sido modificado.

Para eso, un emisor genera un resumen (hash) del mensaje usando un algoritmo hash seguro (SHA-256, por ejemplo) y cifra el hash con su clave privada (Kpriv). Este resultado es la firma digital.

Luego, envía tanto el mensaje original como la firma.

El receptor, cuando recibe estos datos, descifra la firma usando la clave pública de del emisor (Kpub), obteniendo el hash original y calcula el hash del mensaje recibido. Si los dos hash son iguales, el mensaje es auténtico y no ha sufrido alteraciones.


# Conclusión

El cifrado simétrico y el cifrado asimétrico son dos pilares fundamentales de la criptografía moderna, cada uno con sus fortalezas y limitaciones.

El cifrado simétrico es rápido y eficiente, ideal para proteger grandes volúmenes de datos, pero requiere que todos los participantes compartan previamente la misma clave secreta, lo que complica la escalabilidad en sistemas con muchos usuarios. Algoritmos como AES permiten cifrar y descifrar de forma segura mediante subclaves generadas a partir de la clave original.

El cifrado asimétrico, en cambio, resuelve el problema de la distribución de claves gracias a su par de claves pública y privada. Permite cifrar mensajes sin necesidad de compartir secretos y garantiza autenticidad mediante firmas digitales, aunque su rendimiento es menor en comparación con los algoritmos simétricos.

En la práctica, la mayoría de los sistemas seguros combinan ambos métodos mediante cifrado híbrido: se utiliza el cifrado asimétrico para intercambiar de forma segura una clave simétrica, y luego se emplea el cifrado simétrico para proteger eficientemente los datos. Esta combinación aprovecha lo mejor de ambos mundos: la seguridad y autenticidad del cifrado asimétrico junto con la velocidad y eficiencia del cifrado simétrico.