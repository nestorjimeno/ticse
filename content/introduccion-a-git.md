# Introducción a Git

<!-- author: Néstor Jimeno -->
<!-- date: 2025-09-30 -->
<!-- tags: Git, Desarrollo de software -->
<!-- language: spanish -->

**Git** es una herramienta que cambió por completo la forma en que trabajamos con código. Si alguna vez has hecho un trabajo en grupo, seguro que has tenido que hacer cambios en archivos y has tenido esa sensación de miedo a borrar algo que no debías. Para evitar esto es para lo que se concibe Git. 

Git es un **sistema de control de versiones**, lo que significa que te ayuda a gestionar los cambios en el código a lo largo del tiempo, sin preocuparte por perder trabajo o pisar el de otros.

Este software nació en 2005, de la mano de **Linus Torvalds**, el creador de **Linux**, que lo desarrolló porque el sistema de control de versiones que usaba para desarrollar Linux, llamado BitKeeper, dejó de ser gratuito. Torvalds necesitaba algo robusto, rápido y, sobre todo, gratis. 

En pocas palabras y como la mayoría de las aplicaciones que terminan siendo grandes, **Git nació como una necesidad**.

## El impacto de Git en la industria del software

Git no solo transformó el desarrollo de Linux, sino que rápidamente se convirtió en el estándar para proyectos de cualquier tamaño. Antes de su nacimiento, las herramientas de control de versiones tenían limitaciones a la hora de manejar proyectos distribuidos o gestionar cambios de manera eficiente. Con Git, los desarrolladores podían trabajar de forma más autónoma, sin depender de un servidor central. Esto permitió que equipos de desarrollo de todo el mundo pudieran colaborar de manera más eficiente, incluso sin estar conectados todo el tiempo a la misma red.

Git es una herramienta distribuida. Esto significa que **cada desarrollador tiene una copia completa del repositorio** en su propia máquina, con todo el historial de cambios. No depende de un servidor central para saber qué ha pasado en el proyecto, lo que lo hace ideal para trabajar de forma remota o cuando la conexión a internet no es estable. Además, la estructura distribuida **permite trabajar de manera mucho más segura**: si un servidor central se cae, todos los colaboradores aún tienen acceso completo al proyecto en sus máquinas locales.

## El crecimiento de Git gracias a plataformas como GitHub

Las plataformas como **GitHub**, **GitLab** y **Bitbucket** jugaron un papel clave en la popularización de Git. Estas plataformas no solo permitieron almacenar repositorios remotos de forma segura, sino que también agregaron funcionalidades que facilitaron la colaboración, como *pull requests*, revisiones de código y gestión de proyectos. GitHub, en particular, impulsó el software de código abierto a otro nivel al centralizar la colaboración y simplificar la contribución de miles de desarrolladores en todo el mundo.

## Git y la cultura de código abierto

Uno de los mayores logros de Git ha sido su impacto en el **software de código abierto**. Gracias a plataformas como GitHub, miles de desarrolladores han podido colaborar en proyectos globales sin estar físicamente presentes en el mismo lugar. Git permitió que el código abierto creciera a una velocidad nunca antes vista, con contribuciones de miles de personas alrededor del mundo. Esto cambió la forma en que las aplicaciones se desarrollan, distribuyen y mantienen.

## Principales conceptos de Git

Git está lleno de términos que a primera vista pueden sonar complicados, pero en realidad son bastante fáciles de entender una vez te acostumbras a ellos. Aquí te dejo algunos de los más importantes:

- **Commit**: Es el acto de **registrar** los cambios que has hecho en tu código. Cuando haces un *commit*, Git guarda una instantánea de tu proyecto en ese momento, creando un registro permanente en el historial de cambios.

- **Branch**: Una rama es como una "copia paralela" del proyecto. Permite trabajar en nuevas características o correcciones sin afectar al código principal. Las ramas son fáciles de crear y eliminar, lo que facilita la experimentación y el trabajo en equipo.

- **Merge**: Es el proceso de **fusionar los cambios de una rama con otra**. Si dos desarrolladores han trabajado en diferentes ramas y ahora quieren combinar sus cambios, hacen un *merge* para integrar ambos conjuntos de cambios.

- **Remote**: Aunque tu repositorio local tiene todo el historial de cambios, en equipos grandes es común tener un **repositorio remoto** (en GitHub, GitLab, etc.) donde se almacena el código y se sincronizan los cambios entre varios desarrolladores.

## Flujo de trabajo básico en Git

Un flujo de trabajo típico en Git sigue algunos pasos básicos. Supongamos que estás trabajando en una nueva característica de un proyecto. Primero, **clonas el repositorio remoto** en tu máquina local con el comando `clone`:

```bash
git clone <url-del-repo>
```

Luego, creas una nueva rama y te colocas en ella para trabajar en tu característica sin tocar el código principal. Para eso, se utiliza el comando `checkout -b`:

```bash
git checkout -b feature-nueva
```

Cuando haces cambios en el código, los añades al área de preparación (*staging area*) con:

```bash
git add <nombre-del-fichero>
```

También puedes utilizar un punto en vez de un nombre de fichero para añadir todos los archivos modificados:

```bash
git add .
```

Y luego los registras con un mensaje explicativo:

```bash
git commit -m "Agregada nueva característica"
```

Finalmente, subes tus cambios al repositorio remoto para compartirlos con los demás:

```bash
git push origin feature-nueva
```

Donde *origin* es el nombre del repositorio remoto, que se suele llamar *origin*, pero no es un nombre cerrado.

## Algunas limitaciones o desafíos de Git

Aunque Git es increíblemente poderoso, tiene una curva de aprendizaje. Algunos conceptos, como el **rebase** o la **resolución de conflictos**, pueden resultar confusos para quienes se inician. Además, si no se usan bien las herramientas de Git, se pueden generar conflictos difíciles de resolver, especialmente cuando se trabaja en equipos grandes. A pesar de esto, la flexibilidad y el control que Git ofrece a los desarrolladores supera ampliamente estas dificultades.

Git no solo cambió la forma en que desarrollamos software, sino que también creó una nueva manera de pensar sobre la colaboración y el control de versiones. Lo que comenzó como una herramienta para el desarrollo de Linux se convirtió rápidamente en el estándar de facto para cualquier tipo de proyecto de software.

Los detalles, los dejo para el siguiente artículo...







