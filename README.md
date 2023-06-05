# 🗒 prj-gestor-notas
Repositorio utilizado por Equipo LMT para un proyecto de sistema gestor de notas.


## ✏ Descripción del proyecto
Se trata de una aplicación web hecha en Django que cuenta con acceso a un sistema basado en CRUD para la gestión de notas generadas por el usuario, así como también un registro de eventos de calendario generados por el usuario con la ayuda de una base de datos MySQL.

También incluye una pantalla de login y registro de usuarios para administrar el acceso al sistema, así como un manejador de tokens y peticiones para mejorar la seguridad y estabilidad de la aplicación.


## 📦 Stacks de tecnología en uso
- Python 3.11.1
- Django 4.2.1
- MySQL (conectado con mysqlclient 2.1.1)
- Django REST framework (DRF) 3.14.0
- Simple JWT 5.2.2
- Axios 1.4.0 (incluido en el proyecto)
- Bootstrap 5.2.3 (incluido en el proyecto)
- Otros (pylance, pylint, sqlparse, etc.)


## 📁 Recursos estáticos de UI en uso
- [Tema de plantillas "Creative"](https://github.com/startbootstrap/startbootstrap-creative) (startbootstrap-creative 7.0.7)


## 💻 Instrucciones de uso
### Trabajando con stacks en entorno virtual
Para levantar la aplicación desde tu cliente es necesario configurar tu entorno virtual con Python.
Esto es para incluir el framework de trabajo sin invadir la estructura del proyecto en entornos de servidor, así como también para uso compartido entre colaboradores y modificaciones en el repositorio.

La creación de entornos virtuales requieren una instancia de Python instalada directamente en el cliente donde se planea trabajar con el proyecto. Esto es porque el proceso para crear entornos virtuales depende de una serie comandos `pip` bajo la terminal del sistema operativo en uso. 

### Comandos de terminal requeridos **(para sistemas Windows)**
**IMPORTANTE: Tienes que navegar desde terminal hasta el directorio donde se encuentra guardado el proyecto antes de ejecutar estos comandos.**
1. `pip install virtualenv` para instalar el manejador de entornos virtuales de Python.
2. `python -m venv venv` para creación del entorno virtual en ubicación del proyecto.
3. `venv\Scripts\activate.bat` en cmd.exe o `venv\Scripts\Activate.ps1` en Powershell para activar el entorno virtual del proyecto en la terminal.
3. `pip install nombre-stack`, `pip show nombre-stack`, `pip list` para instalación de stacks en el entorno virtual recién creado.
0. `python -m pip install --upgrade pip` es requerido en caso de que los comandos anteriores no funcionen, esto para que 'pip' se actualice a la versión más reciente.

Es posible que el proceso de creación de entorno virtual varíe según el sistema operativo. Consultar documentación externa al repositorio para más información.

### Archivo de requerimientos
El directorio `mis_notes` contiene, además de la aplicación, un archivo denominado `requirements.txt` que proporciona ayuda para el desarrollador que desee utilizar una réplica exacta del entorno virtual que fue utilizado para depurar la aplicación. Algunos editores de texto como Visual Studio Code pueden incluso usarlo para generar el entorno virtual con todos los stacks incluidos para facilitar la instalación de estos.

...

## ℹ Información de colaboradores principales
**En representación del...**  
Tecnológico Nacional de México Campus Tijuana  
[♟ Perfil de GitHub](https://github.com/tectijuana)

**Equipo LMT está conformado por...**  
Estudiantes de la carrera de Ingeniería Informática:
- Erick Abel Lopez Rubio (autor del repositorio)
- Columba Trejo Ortiz
- Pedro Jared Jimenez

**El proyecto se encuentra bajo supervisión de...**  
Docente de la materia "Programación en Ambiente Cliente/Servidor".  
M.C. Ray Brunett Parra Galaviz  
[♟ Perfil de GitLab](https://gitlab.com/RayParra)
...

## 🎯 Información de proyecto (sólo para colaboradores)
### Lista to-do
- [ ] Corregir modelo de negocios y migraciones
- [ ] Hacer funcionar los tokens de JWT
- [x] Incluir Axios de manera local en el proyecto
- [ ] Ajustar nomenclatura entre serializers, views y urls
- [ ] Ajustar direcciones de templates
- [x] Colocar estructura de static (js, css, img)
- [ ] Instalar Bootstrap en static
- [ ] Instalar FullCalendar.js en js
- [ ] Estilizar vistas referenciando css de Bootstrap

### Comentarios adicionales
RAY: Consultar repositorio de clase en caso de dudas.
RAY: Modificar función de login para que no sea del lado cliente (usar POST en vez de GET).
ELR: Actualmente estoy checando como hacer funcionar vista de login y deshacer error credenciales no válidas con la ayuda de modelos. `python manage.py shell` funciona en terminal.