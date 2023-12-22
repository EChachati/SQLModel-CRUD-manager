# Python Base Project

Repositorio prácticamente vacio, solo con configuraciones, úsalo para hacer cualquier proyecto que quieras 

# **Instalación de Proyecto Base en Python**

  

Este tutorial te guiará a través de los pasos para hacer un fork del proyecto base en Python con configuraciones básicas y configurarlo en tu entorno local.

  

### **Dale a la opción de arriba a la derecha 'Use this template'**

  
Al darle click a ese botón te permitirá usar este repositoria como base para que inicies el tuyo. luego lo clonarás a tu máquina local

  

```bash

git  clone  https://github.com/TU_USUARIO/NOMBRE_DEL_REPOSITORIO.git

cd  NOMBRE_DEL_REPOSITORIO

```

  

### **Configurar el Entorno Virtual**

  

Para trabajar en un entorno virtual, utilizaremos **`venv`**.

  

```bash

python  -m  venv  venv

## Linux
source  venv/bin/activate

## Windows
venv/Scripts/activate
```

  

### **Instalar Dependencias**

  

Este proyecto utiliza Poetry para manejar las dependencias. Al utilizar `poetry install --no-root`, se evita la instalación del proyecto en modo editable, lo que significa que no se instalará el proyecto actual como una dependencia.

  

El uso de `--no-root` es útil cuando estás desarrollando un proyecto, ya que evita agregar el proyecto actual como una dependencia editable, lo que podría causar problemas de versión o conflictos con las dependencias instaladas.

  

```bash

poetry  install  --no-root

```
# Archivos en el Proyecto
## .github/workflows/linter.yml
El archivo `.github/workflows/linter.yml` contiene la configuración de un flujo de trabajo de GitHub Actions. Este flujo de trabajo se ejecutará en eventos de `push` y `pull_request`.

### Propósito del Archivo:

-   **Nombre del Flujo de Trabajo:** `Ruff`
-   **Eventos Activadores:** `push` y `pull_request`

### Descripción del Flujo de Trabajo:

-   **jobs:** Define un trabajo llamado `ruff`.
-   **runs-on:** Especifica el entorno de ejecución como `ubuntu-latest`.
-   **steps:** Son los pasos que se deben seguir en este trabajo.
    -   `actions/checkout@v3`: Esta acción es usada para clonar el repositorio en el entorno de ejecución.
    -   `chartboost/ruff-action@v1`: Utiliza una acción llamada `ruff-action` proporcionada por el repositorio `chartboost`. Esta acción ejecuta un linter para revisar el código en busca de problemas y aplicar correcciones si es posible.
        -   **Argumentos utilizados:**
            -   `check`: Indica al linter que realice un chequeo del código.
            -   `--fix-only`: Aplica correcciones solo cuando sea seguro hacerlo automáticamente.
            -   `--unsafe-fixes`: Realiza correcciones no completamente seguras pero consideradas apropiadas.
            -   `--show-fixes`: Muestra las correcciones que se aplican.

### Propósito del Flujo de Trabajo:

Este flujo de trabajo utiliza la acción `ruff-action` para ejecutar un linter en el código. El linter revisa el código en busca de problemas y aplica correcciones automáticas cuando sea posible. Esto ayuda a mantener un código limpio y uniforme en el repositorio.

## .vscode/extension.json
El archivo `.vscode/extension.json` contiene recomendaciones de extensiones para Visual Studio Code que se consideran útiles para este proyecto en particular.
### Descripción del Archivo:

-   `recommendations`: Es una lista de extensiones recomendadas para Visual Studio Code.
    -   Cada elemento en la lista es el nombre único de una extensión disponible en el marketplace de VS Code.

### Propósito del Archivo:
Este archivo proporciona recomendaciones de extensiones para ayudar a los desarrolladores que trabajan en este proyecto a mejorar su experiencia con Visual Studio Code. Las extensiones listadas pueden ser útiles para tareas como formateo de código, revisión ortográfica, soporte para diferentes lenguajes y otras funcionalidades que podrían ser relevantes para el desarrollo del proyecto.

## .vscode/settings.json
El archivo `.vscode/settings.json` contiene configuraciones específicas para Visual Studio Code que se aplican al trabajar con proyectos en Python y algunas herramientas asociadas.

### Propósito del Archivo:

Este archivo define las preferencias de configuración específicas de Python para Visual Studio Code. Las configuraciones incluyen ajustes para el formateo automático, el uso de herramientas de linting y corrección ortográfica, así como ajustes específicos para el análisis de código y documentación. Estas configuraciones pueden ayudar a mantener un código limpio y mejorar la eficiencia durante el desarrollo del proyecto.

## .env.example
El archivo `.env.example` muestra un ejemplo de cómo podrían estructurarse las variables de entorno para el proyecto, aunque en este momento no se estén utilizando activamente. Sirve como una guía para mostrar cómo se podrían configurar las variables de entorno en un proyecto Python.

Como buena práctica de seguridad, los valores sensibles, como contraseñas o rutas de acceso a bases de datos, **no deben incluirse directamente en el código fuente o en el repositorio**. En su lugar, se recomienda utilizar un archivo llamado `.env` para almacenar estas variables de entorno de manera segura.

Este archivo `.env` se omite en el control de versiones (como agregarlo al archivo `.gitignore`) para evitar la exposición de información sensible en el repositorio público.

### Propósito del Archivo `.env.example`:
Aunque actualmente el proyecto no requiera el uso de variables de entorno, este archivo sirve como una guía para futuros desarrollos. Los estudiantes podrían utilizar este ejemplo como referencia para configurar variables de entorno necesarias para diferentes entornos (desarrollo, pruebas, producción) en futuras etapas del proyecto. Esto promueve buenas prácticas de seguridad y separación de configuraciones sensibles del código fuente.
## .gitignore
El archivo `.gitignore` es fundamental en cualquier proyecto controlado por Git. Permite especificar archivos y directorios que deben ser ignorados por Git y no deben ser rastreados ni incluidos en el repositorio.
### Propósito del Archivo `.gitignore`:

El archivo `.gitignore` asegura que ciertos archivos y directorios no se incluyan accidentalmente en el control de versiones, lo que ayuda a mantener limpio y organizado el repositorio. Esto es especialmente útil para archivos generados automáticamente, dependencias de entorno local y otros archivos que no son esenciales para el repositorio en sí.

## License
La licencia determina cómo otros pueden utilizar, modificar y compartir tu trabajo. La licencia MIT es una de las opciones populares en el mundo del código abierto.

### Propósito de las Licencias en Open Source:

Las licencias en proyectos de código abierto establecen los términos y condiciones bajo los cuales el software puede ser utilizado, modificado, redistribuido o incluso sublicenciado por otros desarrolladores. Definen los derechos y restricciones que se aplican al software.

La licencia MIT, en particular, es conocida por su permisividad. Permite a los usuarios modificar, distribuir y utilizar el software para cualquier propósito, incluso para proyectos comerciales, siempre y cuando se incluya el aviso de copyright y la declaración de la licencia original en el código.

### Recomendación y Recursos:

El sitio web [Choose a License](https://choosealicense.com/) es una excelente fuente para explorar y comprender las licencias de código abierto disponibles. Ofrece información detallada sobre diversas licencias, incluyendo sus términos, restricciones y recomendaciones sobre cuándo y cómo usarlas.

La página de la licencia MIT en Choose a License ofrece una visión clara de lo que permite esta licencia y cómo puede afectar tu proyecto.

Recomendar la licencia MIT es una decisión común para aquellos que desean que su código sea ampliamente utilizado y modificado por otros desarrolladores, manteniendo una flexibilidad considerable en términos de uso y distribución.

## pyproject.toml
El archivo `pyproject.toml` contiene la configuración del proyecto, incluyendo las dependencias, herramientas de desarrollo y configuraciones específicas para el linter, el formateador de código y el tipo de verificación estática.

### Descripción del Archivo:

-   `tool.poetry`: Configuración de dependencias del proyecto utilizando Poetry.
-   `tool.ruff`: Configuración del linter Ruff para comprobar y mantener el código.
-   `tool.black`: Configuración para el formateador de código Black.
-   `tool.mypy`: Configuración para el verificador estático de tipos MyPy.

### Propósito del Archivo:

Este archivo es esencial para la configuración del proyecto. Define las dependencias, las herramientas de desarrollo y las configuraciones específicas para el linter, el formateador de código y la verificación estática. Ayuda a mantener un código limpio, consistente y libre de errores.

# Configuraciones actuales en pyproject.toml
Analicemos algunas secciones específicas del archivo `pyproject.toml` para comprender mejor su funcionalidad:


### Sección `[tool.poetry]`:
Poetry es una herramienta de gestión de dependencias y empaquetado para proyectos de Python. El archivo `pyproject.toml` es fundamental para su funcionamiento, ya que contiene la información necesaria para gestionar las dependencias y configuraciones del proyecto. Su [documentación oficial](https://python-poetry.org/docs/) 

```toml
[tool.poetry]
name = "python-base-project"
version = "0.1.0"
description = "Proyecto casi vacío con configuraciones, para empezar lo que quieras"
authors = ["Edkar Chachati <chachati28@gmail.com>"]
license = "MIT"
readme = "README.md"
repository = "https://github.com/EChachati/python-base-project"
documentation = "https://github.com/EChachati/python-base-project/blob/master/README.md"
```
- `name`: Nombre del proyecto.
- `version`: Versión actual del proyecto.
- `description`: Descripción breve del proyecto.
- `authors`: Lista de autores del proyecto.
- `license`: Licencia bajo la cual se distribuye el proyecto.
- `readme`: Nombre del archivo README asociado.
- `repository`: URL del repositorio del proyecto.
- `documentation`: URL de la documentación asociada al proyecto.

### Secciones `[tool.poetry.dependencies]` y `[tool.poetry.group.dev.dependencies]`:
Estas secciones contienen las dependencias del proyecto clasificadas por categorías.

- `[tool.poetry.dependencies]`: Contiene las dependencias principales del proyecto.
- `[tool.poetry.group.dev.dependencies]`: Contiene las dependencias de desarrollo utilizadas durante el desarrollo del proyecto.

### Sección `[build-system]`:
```toml
[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```
- `requires`: Lista de dependencias requeridas por el sistema de construcción (Poetry en este caso).
- `build-backend`: Backend utilizado por Poetry para construir el proyecto.

### Propósito de Poetry en `pyproject.toml`:
- **Gestión de dependencias**: Administra las dependencias del proyecto (bibliotecas de terceros, herramientas de desarrollo, etc.) especificadas en las secciones `dependencies` y `group.dev.dependencies`.
- **Gestión del Proyecto**: Ofrece información relevante del proyecto, como nombre, versión, descripción, autores, licencia, entre otros.
- **Empaquetado del Proyecto**: Ayuda a empaquetar el proyecto para distribución y publicación.

Poetry simplifica la gestión de dependencias y la administración de proyectos Python, proporcionando un enfoque unificado y eficiente.

#### Sección `[tool.ruff]`:
Ruff es una herramienta de linting para Python que ayuda a mantener un código limpio, consistente y libre de errores. Se utiliza para identificar y corregir problemas de estilo, convenciones de codificación, errores comunes y posibles mejoras en el código Python. Su [documentación oficial](https://docs.astral.sh/ruff/linter/) 
```toml
[tool.ruff]
ignore = ["B008", "RUF012"]
line-length = 100
select = [
    "E",   # Errores pycodestyle
    "W",   # Advertencias pycodestyle
    "F",   # pyflakes
    "I",   # isort
    "C",   # flake8-comprehensions
    "B",   # flake8-bugbear
    "SIM", # flake8-simplify
    "TCH", # flake8-type-checking
    "TID", # flake8-tidy-imports
    "Q",   # flake8-quotes
    "UP",  # pyupgrade
    "PT",  # flake8-pytest-style
    "RUF", # Reglas específicas de Ruff
]
```
- `ignore`: Lista de reglas a ignorar por el linter Ruff durante la verificación del código.
- `line-length`: Longitud máxima de línea permitida.
- `select`: Conjunto de reglas o categorías de verificación que se activarán para Ruff.

#### Sección `[tool.black]`:
Black es un formateador de código para Python. Su principal objetivo es garantizar la consistencia en el estilo de código Python. Se utiliza para formatear automáticamente el código siguiendo un conjunto de reglas predefinidas, lo que ayuda a mantener un estilo uniforme y legible en todo el proyecto. Su [documentación oficial](https://black.readthedocs.io/en/stable/)
```toml
[tool.black]
line-length = 100
target-version = ['py311']
```
- `line-length`: Establece la longitud máxima de línea permitida por Black.
- `target-version`: Define la versión de Python a la que se dirige el formateador Black.

#### Sección `[tool.mypy]`:
MyPy es una herramienta de verificación estática de tipos para Python. Permite agregar anotaciones de tipo al código y verificar si las variables y funciones se usan correctamente según esos tipos. Ayuda a identificar errores de tipado antes de la ejecución del código. Su [documentación oficial](https://mypy.readthedocs.io/en/stable/)
```toml
[tool.mypy]
python_version = "3.11"
strict = true
check_untyped_defs = false
explicit_package_bases = true
warn_unused_ignores = false
exclude = ["tests"]
```
- `python_version`: Especifica la versión de Python para la cual se realizan las comprobaciones de tipos con MyPy.
- `strict`: Activa el modo estricto de MyPy, donde las comprobaciones de tipos son más rigurosas.
- `check_untyped_defs`: Define si se deben comprobar las definiciones sin tipos.
- `explicit_package_bases`: Obliga a especificar bases de paquete en las clases.
- `warn_unused_ignores`: Controla si se deben mostrar advertencias sobre los ignorados de tipos.
- `exclude`: Lista de directorios o archivos excluidos de las comprobaciones de tipos de MyPy.

Estas secciones son cruciales para configurar las herramientas de desarrollo como Ruff, Black y MyPy. Cada una define reglas, comportamientos y ajustes específicos para asegurar la consistencia y la calidad del código. 


# Modificar Dependencias con Poetry:
Para añadir nuevas dependencias al proyecto, puedes usar el comando `poetry add`. Esto agregará la dependencia al archivo `pyproject.toml`.

#### Dependencia Principal:
```bash
poetry add nombre_paquete
```
Esto agregará `nombre_paquete` como una dependencia principal en el bloque `[tool.poetry.dependencies]` en `pyproject.toml`.

#### Dependencia de Desarrollo:
```bash
poetry add --dev nombre_paquete
```
Esto agregará `nombre_paquete` como una dependencia de desarrollo en el bloque `[tool.poetry.group.dev.dependencies]` en `pyproject.toml`.

### Quitar Dependencias:
Para quitar dependencias del proyecto, puedes usar el comando `poetry remove`.

#### Quitar Dependencia Principal:
```bash
poetry remove nombre_paquete
```
Esto eliminará `nombre_paquete` de las dependencias principales en `pyproject.toml`.

#### Quitar Dependencia de Desarrollo:
```bash
poetry remove --dev nombre_paquete
```
Esto eliminará `nombre_paquete` de las dependencias de desarrollo en `pyproject.toml`.

### Actualizar Dependencias:
Para actualizar dependencias, puedes usar el comando `poetry update`.

#### Actualizar Todas las Dependencias:
```bash
poetry update
```
Esto actualizará todas las dependencias a sus últimas versiones compatibles y ajustará el archivo `pyproject.toml` en consecuencia.

Estos comandos te permiten gestionar las dependencias de tu proyecto de manera eficiente, ya sea añadiendo nuevas, quitando las que ya no son necesarias o actualizando a las últimas versiones compatibles.
