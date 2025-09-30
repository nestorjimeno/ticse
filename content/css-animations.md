# Curso CSS

<!-- author: Néstor Jimeno -->
<!-- date: 2025-09-20 -->
<!-- tags: CSS -->
<!-- language: spanish -->

En CSS hay dos tipos de animaciones: las animaciones y las transiciones.
Las transiciones son más fáciles.

## Transiciones

La duración de la transición la establece `transition-duration` y se le indica en segundos. Es el propio navegador el que decide cómo se hace la transicón, cómo se calcula. Si la transición la ponemos en el `hover`, sólo se verá al entrar, al hacer realmente hover. Pero si la transición está en el elemento, ocurrirá tanto al entrar al hover como al salir. La primera animación será la del hover, y la final será la del elemento. Es decir, al hacer hover, se utiliza la transición del hover, pero al volver, se utiliza la transición del elemento, porque vuelve del estado "hover" al estado "sin estado".

Por defecto se animan todas las propiedades. Para especificar cuál lo podemos indicar en `transition-property`. Animarlo todo puede generar problemas de rendimiento, por ejemplo el box-shadow consume bastantes recursos. Es mejor especificar qué propiedades tienen que animarse.

Por defecto, la velocidad de la transición es lineal, pero podemos cambiarla con `transition-timing-function`:

- ease-in: al principio lento y al final rápido.
- ease-out: rápido al principio, lento al final.
- ease-in-out: lento, rápido, lento.
- ease: 
- steps(k): la transición en un número de pasos. Divide el tiempo de duración entre `k`.
- cubic-bezier(x1 y1, x2 y2): en las devtools, si ponemos esto y hacemos clic en el icono que aparece, se pueden ver opciones diferentes, permite configurar a más detalle la transición.

Por defecto, la transición empieza automáticamente, pero podemos ponerle un delay con `transition-delay`. 

La forma corta de escribirlo es con `transition`, con este orden:

`transition: propiedad duracion tipo-transicion delay, propiedad duracion tipo-transicion delay`


## Animaciones

En las animaciones podemos decir por qué pasos tiene que pasar al animarse. Antes sólo decíamos estados inicial y final, pero no cómo pasar por ellos. Para eso usaremos los `@keyframes`.

```css
@keyframes nombre-del-keyframe {
    from {
        transform: translateY(0px);
    }
    to {
        transform: translateY(100px);
    }
}
```
Luego, en el elemento a animar, tendremos que añadir `animation-name: nombre-del-keyframe`, `animation-duration: 3s`, `animation-timing-function` , `animation-iteration-count`, `animation-direction` (normal,  reverse, alternate, alternate-reverse), `animation-play-state` (paused ) . 

También se puede indicar, en vez de `from` o `to`, un porcentaje, como `0%`, `25%` o `100%` para el final. También se puede obviar el `from`, ya que tomará el punto inicial del elemento.

Por defecto, al terminar una aminación, el elemento vuelve a su posición de inicio de manera brusca, tiene la propiedad `animation-fill-mode: none`. Se podría poner `animation-fill-mode: forwards` para que el elemento se quede al terminar la animación con el estado final. 

La forma corta de escribirlo es con `animation`, con este orden:

`animation: nombre duracion tipo-animacion fill-mode, nombre duracion tipo-animacion fill-mode`

## Pseudoelementos

Es un elemento invisible que aparece antes (::after o ::before), que hace que aparezca antes o después de un elemento.

## Animaciones de scroll

[https://scroll-driven-animations.style/](https://scroll-driven-animations.style/)


## Selectores combinados

Si simplemente los ordeno, lo entenderá como padres e hijos. Es decir, buscará la clase primera y dentro de ella, la clase segunda. Y sobre esos elementos aplicará los estilos. Esto lo hará a todos los niveles. Por ejemplo, en el siguiente código:

```html
<article>
  <p>Introducción del artículo</p>
  <footer>
    <p>Texto del footer</p>    
  </footer>
</article>
```

Con los estilos:

```css
article p {
    color: red;
}
```

Se verán los `<p>` de color azul. Pero si sólo quiero que aplique a los que son hijos directos de `article`, tendría que hacer esto:

```css
article > p {
    color: red;
}
```

De esta manera sólo los hijos directos, el primer descendiente, le aplicará. Al que es hijo, pero tiene el `footer` por medio, no le afecta.

Otro sería este:

```css
p ~ span {
    color: red;
} 
```

Que afectaría a los `span` que están después de un p, pero a todos. Para que sea justamente el que viene después, el hermano inmediatamente siguiente, sería usando un `+`.

El orden se puede ver en esta página: [https://specificity.keegan.st/](https://specificity.keegan.st/)

## Estados y pseudoclases

- hover: al pasar el cursor por encima.
- active: se produce al hacer clic.
- focus: cuando el elemento tiene el foco, como cuando hacemos clic en una caja de texto.
- :first-child: indica el primer elemento de un tipo, por ejemplo en una lista de `li`. Existen además `last-child` o `nth-child(numero)`.

## Border y outline

Al indicar el borde a un elemento con `border`, estos píxeles se añaden al elemento y "crece", se hace más grande. Si lo que hacemos es utilizar `outline`, el contorno que se pinta se hace sobreescrito, por encima de todo y no afecta a la disposición de los elementos. Sería como pintar en la pantalla sin tocar ni cambiar nada de la maquetación. 

Otra opción para evitar saltos sería tener siempre que queramos aplicar un borde, un borde transparente por defecto con el mismo grosor que queremos aplicar.

## Unidades

- El procentaje es una unidad relativa al contenedor padre.
- Podemos usar el viewport, por ejemplo `50vh` para el 50% de la altura o `50vw` para el 50% del ancho de la pantalla.

## Modelo caja

Los elementos html pueden ser de tipo **bloque** o de tipo **en línea**. Un `div` por defecto tendrá configuración en bloque (`display: block`), mientras que un `span` será por defecto en línea (`display: inline`).

Esto hace además que a los elementos `inline` no les afecten algunas propiedades, como `width` o `height`. 

### Elementos **block**

- Padding: afecta al tamaño del elemento. Width y height tienen la medida del contenido y a eso hay que sumarle el padding.
- Border: lo mismo que para el padding.
- Margin: en este caso, no afecta al tamaño de la "caja", es un espacio que se añade por fuera.

Para evitar esto, podemos utilizar la propiedad `box-sizing`. Por defecto es `content-box`, por lo que se le suman el padding y el border. En cambio, si utilizamos `border-box`, significa que el alto y el ancho de la caja se contará desde el borde, por lo que incluirá el borde y el padding.

### Elementos **inline**

Si ponemos `display: inline`, los elementos se colocarán en línea, como texto, unos al lado de otros y no les afectarán el ancho y alto. 

### Elemetos **flex**

Si colocamos `display: flex` en el padre de unos elementos, los colocará de una manera más eficiente. Por ejemplo, si al padre de unos `div` le ponemos `display: flex`, y tiene sitio para colocarlos en línea, lo hará, aunque esos hijos seguirán siendo `block`, es decir, les afectará el ancho y alto que definamos, pero se colocarán en línea. Podemos cambiar la dirección en la que ordenar con `flex-direction`, que puede ser `row` o `column`. Pero siempre será en **una línea**, fila o columna. Pueden colocarse también al revés con `row-reverse` o `column-reverse`. Por defecto será `flex-direction: flex`.  

Otra propiedad es `flex-wrap`, que por defecto será `nowrap`. Esta propiedad lo que hace es acomodar los hijos al tamaño del padre, aunque tenga que reducir los hijos. Si le ponemos `wrap` hará saltos de línea si no caben.

Por defecto se utiliza `flex-basis: auto` (o `flex: 1`), que significa que los hijos se pueden ampliar y reducir para ajustarse a su contenido. Es decir, tiene `flex-grow: 1` y `flex-shrink: 1`. Si tuviéramos `flex-basis: 0`, no tendrá en cuenta el contenido de los hijos y todos tendrán el mismo tamaño.

## Overflow

Por defecto cuando un contendio desborda, utiliza `overflow: visible`. El contenido no se recorta y lo muestra por encima de la caja. Podríamos utilizar `overflow: hidden`, y quedará por detrás, oculto, recortado por la caja, pero no podremos verlo. Si utilizamos `overflow: scroll`, visulamente será igual que `hidden`, pero colocará unas barras de scroll y te podrás mover por dentro de la caja haciendo scroll, por lo que podrás acceder a todo el contenido. Para este último caso, es recomendable utilizar `overflow: auto`, porque algunos navegadores o sistemas operativos con `scroll` colocan las barras por defecto, aunque el contenido quepa perfectamente, dando una imagen poco elegante. Así, con `auto`, si el contenido no cabe, colocará las barras y podrás hacer scroll, pero si cabe, no las colocará, quedando mejor. 

Otra propiedad es `text-overflow`, que se encarga de que si es texto y tienes `overflow: hidden`, coloca unos puntos suspensivos cuando tiene que cortar el texto. Por dfecto el valor es `clip`, que corta de golpe.

También podemos indicar el orden de cada hijo con `order: K` dentro de cada hijo.

Una vez que tenemos claro cuál es el eje principal (row o column), podremos ubicar los hijos en él con `justify-contet`. Esta propiedad puede tener los valores:
- center: centrado.
- space-around: espaciado igual de cada elemento por ambos lados, icluyendo espacios con el borde.
- space-between: sin espacio en los bordes, espaciados igual los elementos.
- space-evenly: mismo espacio entre el borde y el primer (o último) elemento que entre elementos.

Además, puedes añadir `gap`, que afectará al espacio entre elementos, no afecta al espacio con los bordes.

En el eje cruzado, el que no es principal, se puede utilizar `align-items` para centrar o `flex-start` y `flex-end` para colocar al principio o final de la dimensión, que funcionará a cada línea.

Para ubicarlo a nivel del coontenedor completo, todas las líneas, se utilizaría `align-content`, con `center`, 

Después de esta ordenación, dentro de cada elemento hijo podríamos utilizar `align-self` y cambiarles la alineación. El padre es el que indica cómo se alinean sus hijos, pero un hijo, con esta propiedad, puede salirse de ese ordenamiento, para excepciones.

## Position

Los elementos se posicionan por defecto de manera estática, se van apilando: `position: static`.

Con `position: absolute`, el elemento podrá posicionarse utilizando coordenadas (top, right, bottom, left). Lo posiciona con respecto al documento completo. Si queremos que la referencia sea un subelemento del documento, tendríamos que utilizar `position: relative` en algún padre. Es decir, cuando un elemento tiene `position: absolute`, buscará un padre que tenga un `position: relative` para utilizarlo como referencia y desde él usar top, bottom, left, right. Si no encontrara ninguno, llegará a arriba del todo, al documento general y tomará las medidas desde él.

`position: fixed` es parecido al absolute, pero las coordenadas serán relativas al viewport, a la pantalla.

`position: sticky` se queda dentro de la panta  lla, pero dentro del contenedor, de su relative. A veces puede parecerse al fixed, pero no es lo mismo.

## Grid

 

 