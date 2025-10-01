# Introducción a TLS

<!-- author: Néstor Jimeno -->
<!-- date: 2025-10-01 -->
<!-- tags: Seguridad, Desarrollo de software -->
<!-- language: spanish -->

TLS, siglas de Transport Layer Security (Seguridad en la Capa de Transporte), es un protocolo de seguridad, es decir, un conjunto de reglas, que define cómo se cifran las comunicaciones en internet para proteger la privacidad y asegurar la integridad de los datos entre un cliente (generalmente un navegador) y un servidor.

Vamos a verlo con un ejemplo. 

## Conexión inicial o *handshake*

Cuando un navegador accede a una web, por ejemplo https://nestorjimeno.com, se produce lo siguiente:

1. El navegador abre una conexión TCP con el servidor, por ejemplo a través del puerto 443 para HTTPS y envía un mensaje inicial llamado ***ClientHello***, que contiene:

    - Las versiones de TLS que soporta (por ejemplo TLS 1.2, TLS 1.3).
    - Una lista de algoritmos de cifrado y firmas que puede utilizar (**ciphersuite**).
    - Un número aleatorio que servirá para generar la clave de sesión (más adelante vemos qué es).
    - Opcionalmente, extensiones como SNI (Server Name Indication) que indica a qué dominio quiere conectarse. 

2. El servidor responde con un ***ServerHello***, indicando:

    - La versión TLS que eligió (la más alta que ambos soportan).
    - La **ciphersuite** que se usará para cifrar la sesión.
    - Otro número aleatorio del servidor.

    Con esto, ambos lados tienen suficiente información para generar claves de sesión seguras.

3. El servidor envía su **certificado digital**, que contiene el nombre de la web, la **clave pública del servidor** y la firma digital de una **Autoridad de Certificadora (CA)** confiable. 
    
    Cuando una CA firma un certificado, aplica un hash sobre él y lo cifra con su clave privada. El navegador utiliza la clave pública de la CA que está almacenada en su lista de CAs raíz confiables y descifra la firma. Compara el hash que estaba cifrado con el hash del certificado y, si coinciden, se demuestra que no ha sido modificado y que se puede confiar en que proviene de la CA que se dice.
    
    El navegador también verifica que el certificado no haya expirado y que el dominio que contiene coincida con el de la web a la que está intentando acceder. 
    
    Si todo es correcto, el navegador sabe que está hablando con el servidor legítimo, aunque en algunos casos el servidor también puede pedir un certificado del cliente para una autenticación mutua.

4. El navegador genera una **clave de sesión** para evitar usar la clave pública para todo. La cifra con la clave pública del servidor y se la envía. De esta manera el servidor puede descifrarla con su clave privada y así ambos tienen la misma clave secreta para cifrado simétrico y que sirve sólo para esa sesión.

5. Finalmente ambos lados envían un mensaje indicando que todas las futuras comunicaciones irán cifradas con la clave de sesión. Se intercambian hashes de verificación para asegurar que el handshake no fue modificado por un atacante y, a partir de aquí, la comunicación es cifrada y segura, y todo el tráfico (HTTP, datos, formularios, etc.) se protege mediante TLS.

6. Cuando cierras la web o se termina la sesión, la clave de sesión se descarta y, la próxima vez que se acceda a la web, se repite el proceso.

## ¿Qué es una Autoridad Certificadora?

Una Autoridad Certificadora (CA, por sus siglas en inglés) es una entidad de confianza que emite certificados digitales. Estos certificados se usan para probar la identidad de un sitio web, persona o dispositivo en Internet y aseguran que, cuando te conectas a un servidor, puedes confiar en que realmente es quien dice ser y que la comunicación será segura. Por ejemplo, cuando entras a https://google.com, tu navegador confía en Google porque su certificado está firmado por una CA reconocida como DigiCert o Let’s Encrypt.

Las CAs funcionan en un modelo jerárquico:

1. CA raíz: Es la autoridad más importante y de confianza máxima. Su certificado está preinstalado en todos los sistemas operativos y navegadores. Firma las CA intermedias, no directamente los sitios webs.

2. CA intermedia: Firma certificados de los sitios webs o servidores en nombre de la raíz. Se usa para proteger la CA raíz, evitando que se comprometa directamente, mejorando la seguridad: si se compromete una intermedia, la raíz sigue segura.

3. Certificados finales: Son los que usan los servidores, páginas web o dispositivos. Están firmados por la CA intermedia o raíz, por lo que el navegador los acepta.

Cuando visitas https://miempresa.com:

1. El navegador recibe el certificado del servidor.

2. Comprueba quién lo firmó → encuentra la CA intermedia.

3. Comprueba quién firmó la CA intermedia → encuentra la CA raíz.

4. Si la CA raíz está en la lista de confianza del navegador, entonces confía en todo el certificado y muestra el candado verde.

Esto se llama cadena de confianza o **“chain of trust”**.

### Autoridad Certificadora raíz

En octubre de 2025, existen más de 85 Autoridades Certificadoras (CAs) reconocidas por navegadores y sistemas operativos. Sin embargo, solo una pequeña fracción de ellas emite la gran mayoría de los certificados digitales utilizados en Internet. Las seis principales CAs que emiten el 90% de los certificados SSL/TLS son:

- Let’s Encrypt – 64% del mercado
- GlobalSign – 22.4%
- Sectigo – 5.9%
- DigiCert – 3.6%
- Entrust – 2.1%
- IdenTrust – 1.1%

Cada sistema operativo y navegador mantiene su propia lista de CAs raíz confiables. Puedes consultar estas listas en:

- Microsoft Trusted Root Program: Lista oficial de CAs reconocidas por Microsoft.
- Mozilla Root Store: Lista de CAs confiables para Firefox y otros productos de Mozilla.
- Apple Root Certificate Program: Lista de CAs confiables para macOS y iOS.
- Common CA Database (CCADB): Base de datos pública mantenida por Mozilla y otras organizaciones.

Las CAs raíz son fundamentales para la seguridad en línea. Si una CA raíz es comprometida, todos los certificados emitidos por ella también lo estarán. Por ello, los navegadores y sistemas operativos actualizan regularmente sus listas de CAs confiables para garantizar la seguridad de los usuarios.

### Cómo ver tus certificados

En Windows, `certmgr.msc` es una herramienta que sirve para administrar certificados digitales en tu sistema. Permite ver, instalar, exportar, eliminar o inspeccionar certificados que usa tu Windows y los programas que dependen de él, desde navegadores a correo o VPN.

Cuando lo abres (Win + R → `certmgr.msc` → Enter), verás varias carpetas organizadas por tipo de certificado:

- Personal: Certificados asociados a tu usuario que se usan para autenticación de correo, VPNs o firma de documentos digitales.
- Entidades de certificación raíz de confianza: Contiene los certificados de las CAs raíz que Windows y tus navegadores confían automáticamente. Todo certificado firmado por estas CAs será aceptado como válido.
- Entidades de certificación intermedias: Contiene CAs que firman certificados de servidores o usuarios en nombre de la raíz. Permite que Windows valide certificados que no son de la raíz directa.
- Otras carpetas: 
    - Revocados: certificados que han sido invalidados.
    - Terceros: certificados de confianza que no son raíz ni intermedia.
    - Autoridades de certificación raíz confiables de empresa: usados en redes corporativas.
