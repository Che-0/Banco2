# 🏦 Banco2 — Sistema Bancario Web

Sistema bancario web desarrollado con **Django** como proyecto de gestión de usuarios, clientes, cuentas bancarias y transferencias.

Banco2 permite administrar la información de clientes y usuarios, crear cuentas bancarias, realizar transferencias entre cuentas, consultar movimientos, gestionar notificaciones y generar reportes administrativos, incluyendo exportación de información a Excel.

El proyecto utiliza una arquitectura basada en aplicaciones Django independientes y está preparado para trabajar tanto en un entorno local como en un entorno desplegado utilizando una base de datos PostgreSQL.

---

## 📋 Tabla de contenidos

* [Descripción](#-descripción)
* [Características](#-características)
* [Roles de usuario](#-roles-de-usuario)
* [Módulos del sistema](#-módulos-del-sistema)
* [Flujo general](#-flujo-general)
* [Modelo de datos](#-modelo-de-datos)
* [Transferencias](#-transferencias)
* [Notificaciones](#-notificaciones)
* [Reportes](#-reportes)
* [Arquitectura del proyecto](#-arquitectura-del-proyecto)
* [Estructura de carpetas](#-estructura-de-carpetas)
* [Tecnologías utilizadas](#-tecnologías-utilizadas)
* [Requisitos](#-requisitos)
* [Instalación](#-instalación)
* [Variables de entorno](#-variables-de-entorno)
* [Migraciones](#-migraciones)
* [Crear un administrador](#-crear-un-administrador)
* [Ejecución](#-ejecución)
* [Configuración de base de datos](#-configuración-de-base-de-datos)
* [Archivos estáticos y multimedia](#-archivos-estáticos-y-multimedia)
* [Seguridad y autenticación](#-seguridad-y-autenticación)
* [Consideraciones](#-consideraciones)
* [Posibles mejoras](#-posibles-mejoras)
* [Autor](#-autor)

---

# 📖 Descripción

Banco2 es una aplicación web bancaria construida utilizando **Django 4.2**.

El sistema está dividido en diferentes aplicaciones que separan las principales responsabilidades del proyecto:

* `accounts`: autenticación y administración de usuarios.
* `clientes`: gestión de clientes, cuentas bancarias y transferencias.
* `notificaciones`: sistema de notificaciones internas.
* `reportes`: generación de estadísticas y reportes.
* `core`: dashboard y funcionalidades generales.
* `config`: configuración principal del proyecto Django.

La aplicación utiliza el sistema de autenticación de Django mediante un **modelo de usuario personalizado**, al cual se agrega un sistema de roles para diferenciar administradores, empleados y clientes.

---

# ✨ Características

## 👤 Gestión de usuarios

Los usuarios pueden tener diferentes roles dentro del sistema:

* Administrador
* Empleado
* Cliente

Los administradores pueden:

* Registrar usuarios.
* Consultar usuarios.
* Editar usuarios.
* Activar o desactivar usuarios.
* Eliminar usuarios.
* Asignar roles.

El sistema utiliza un modelo `User` basado en `AbstractUser` de Django.

---

## 👥 Gestión de clientes

Los administradores y empleados pueden:

* Registrar clientes.
* Consultar clientes.
* Buscar clientes.
* Ver información detallada.
* Editar información.
* Eliminar clientes.
* Consultar el estado del cliente.

La información almacenada incluye, entre otros datos:

* Nombres.
* Apellidos.
* Tipo de documento.
* Número de documento.
* Fecha de nacimiento.
* Teléfono.
* Correo electrónico.
* Dirección.
* Ciudad.
* Departamento.
* Estado.
* Fotografía.

También existe una relación entre el cliente y el usuario que utiliza el sistema para acceder al portal bancario.

---

## 🏦 Gestión de cuentas bancarias

Cada cliente puede tener una o más cuentas bancarias.

El sistema contempla dos tipos de cuenta:

* Cuenta de ahorro.
* Cuenta corriente.

Cada cuenta posee:

* Número de cuenta.
* Tipo de cuenta.
* Saldo.
* Estado.
* Fecha de apertura.
* Cliente propietario.

El número de cuenta se genera automáticamente durante el registro del cliente.

---

## 💸 Transferencias

Los clientes pueden realizar transferencias hacia otras cuentas activas.

Antes de realizar una transferencia se comprueba:

* Que el usuario tenga una cuenta activa.
* Que la cuenta destino exista.
* Que la cuenta destino esté activa.
* Que la cuenta destino no sea la misma cuenta de origen.
* Que exista saldo suficiente.
* Que el monto sea válido.

La operación modifica el saldo de ambas cuentas y registra la transferencia correspondiente.

La actualización de los saldos y la creación del registro de transferencia se realizan dentro de una transacción de base de datos utilizando `transaction.atomic()`.

---

# 👥 Roles de usuario

Banco2 utiliza tres roles principales:

| Rol               | Descripción                                              |
| ----------------- | -------------------------------------------------------- |
| **Administrador** | Administración general del sistema y usuarios.           |
| **Empleado**      | Gestión de clientes y acceso a reportes administrativos. |
| **Cliente**       | Consulta de su cuenta y realización de transferencias.   |

El rol se almacena directamente en el modelo personalizado `User`. Además, los usuarios con permisos de superusuario de Django son tratados como administradores.

### Administrador

Puede gestionar:

* Usuarios.
* Clientes.
* Cuentas.
* Reportes.
* Notificaciones.
* Información administrativa.

### Empleado

Puede gestionar principalmente:

* Clientes.
* Información relacionada con clientes.
* Reportes.

### Cliente

Tiene acceso a su portal personal, donde puede consultar:

* Información personal.
* Cuenta bancaria activa.
* Saldo.
* Transferencias recientes.
* Notificaciones.

También puede realizar transferencias y actualizar su fotografía de perfil.

---

# 🧩 Módulos del sistema

## `accounts`

Responsable de la autenticación y administración de usuarios.

Incluye:

* Login.
* Logout.
* Registro de usuarios.
* Edición de usuarios.
* Eliminación de usuarios.
* Control de permisos.

Archivos principales:

```text
accounts/
├── admin.py
├── apps.py
├── forms.py
├── models.py
├── urls.py
└── views.py
```

El modelo `User` extiende `AbstractUser` y agrega información como:

* Rol.
* Teléfono.
* Fecha de creación.
* Fecha de actualización.

---

## `clientes`

Es uno de los módulos principales del sistema.

Gestiona:

* Clientes.
* Cuentas bancarias.
* Transferencias.
* Portal del cliente.
* Fotografías de perfil.

Sus principales modelos son:

```text
Cliente
CuentaBancaria
Transferencia
```

---

## `core`

Contiene funcionalidades generales del sistema.

Actualmente se utiliza principalmente para el dashboard.

El dashboard muestra información como:

* Total de clientes.
* Total de usuarios.
* Clientes registrados recientemente.
* Notificaciones recientes del usuario.

Los clientes son redirigidos automáticamente a su portal al acceder al dashboard general.

---

## `notificaciones`

Implementa un sistema de notificaciones internas.

Cada notificación contiene:

* Destinatario.
* Título.
* Mensaje.
* Tipo.
* Estado de lectura.
* Fecha de creación.
* Fecha de lectura.
* URL opcional.

Los tipos disponibles son:

* Información.
* Éxito.
* Alerta.
* Error.

Los usuarios pueden:

* Consultar sus notificaciones.
* Marcar una notificación como leída.
* Marcar todas como leídas.

---

## `reportes`

Permite consultar información administrativa y generar reportes.

Actualmente proporciona:

### Dashboard de reportes

Muestra:

* Total de clientes.
* Clientes activos.
* Total de cuentas.
* Saldo total.
* Total de transferencias.
* Transferencias realizadas durante los últimos 30 días.
* Monto transferido durante los últimos 30 días.
* Distribución de usuarios por rol.

### Reporte de clientes

Permite consultar clientes y aplicar filtros por:

* Estado.
* Nombre.
* Apellidos.
* Número de documento.

### Exportación a Excel

La información de clientes puede exportarse a un archivo:

```text
clientes.xlsx
```

La exportación utiliza `openpyxl`.

### Reporte de transferencias

Permite consultar las últimas 100 transferencias registradas.

---

# 🔄 Flujo general

Un flujo típico del sistema es:

```text
                    ┌─────────────────┐
                    │     Usuario     │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  Autenticación  │
                    └────────┬────────┘
                             │
                ┌────────────┴────────────┐
                │                         │
                ▼                         ▼
        ┌───────────────┐         ┌───────────────┐
        │ Administrador │         │    Cliente    │
        │ / Empleado    │         │               │
        └───────┬───────┘         └───────┬───────┘
                │                         │
                ▼                         ▼
        ┌───────────────┐         ┌───────────────┐
        │ Gestión de    │         │ Portal del    │
        │ clientes      │         │ cliente       │
        └───────┬───────┘         └───────┬───────┘
                │                         │
                ▼                         ▼
        ┌───────────────┐         ┌───────────────┐
        │ Cuentas       │         │ Transferencias│
        │ bancarias     │         │               │
        └───────────────┘         └───────┬───────┘
                                          │
                                          ▼
                                  ┌───────────────┐
                                  │ Base de datos │
                                  └───────────────┘
```

---

# 🗃️ Modelo de datos

La estructura principal del sistema está formada por cuatro entidades:

```text
User
 │
 │ 1
 │
 │ 0..1
 ▼
Cliente
 │
 │ 1
 │
 │ N
 ▼
CuentaBancaria
 │
 ├───────────────┐
 │               │
 │               │
 ▼               ▼
Cuenta origen   Cuenta destino
       \         /
        \       /
         ▼     ▼
        Transferencia
```

### `User`

Representa las cuentas de acceso al sistema.

Campos adicionales:

```text
rol
telefono
creado
actualizado
```

### `Cliente`

Representa al cliente bancario.

Se relaciona con:

* Un usuario.
* Una o varias cuentas bancarias.
* El usuario que realizó su registro.

### `CuentaBancaria`

Representa una cuenta bancaria perteneciente a un cliente.

Contiene:

```text
numero_cuenta
tipo_cuenta
saldo
estado
fecha_apertura
```

### `Transferencia`

Registra las operaciones entre cuentas.

Contiene:

```text
cuenta_origen
cuenta_destino
monto
descripcion
estado
fecha
realizado_por
```

---

# 💸 Funcionamiento de una transferencia

El proceso de transferencia sigue aproximadamente este flujo:

```text
Cliente
   │
   ▼
Ingresa cuenta destino
   │
   ▼
Ingresa monto
   │
   ▼
Validación del formulario
   │
   ├── Cuenta inexistente/inactiva ──► Error
   │
   ▼
Comprobar cuenta origen
   │
   ▼
Comprobar saldo
   │
   ├── Saldo insuficiente ──► Error
   │
   ▼
transaction.atomic()
   │
   ├── Restar saldo origen
   │
   ├── Sumar saldo destino
   │
   └── Registrar transferencia
   │
   ▼
Crear notificaciones
   │
   ├── Emisor
   │
   └── Receptor
   │
   ▼
Transferencia completada
```

La utilización de `transaction.atomic()` permite que las modificaciones principales de la transferencia se ejecuten como una única transacción de base de datos.

---

# 🔔 Notificaciones

Banco2 cuenta con dos mecanismos de comunicación:

### Notificaciones internas

Se almacenan en la base de datos y aparecen dentro del sistema.

Por ejemplo:

```text
Transferencia realizada
Transferencia recibida
Cliente registrado
```

### Notificación por correo

El proyecto también implementa una alerta de seguridad cuando un usuario inicia sesión.

Cuando Django detecta el evento `user_logged_in`, se genera un correo dirigido al usuario que acaba de iniciar sesión.

El envío se ejecuta mediante un hilo separado utilizando `threading.Thread`, con el objetivo de evitar realizar el envío directamente dentro del flujo principal de la petición.

---

# 📊 Reportes

El módulo de reportes está restringido a administradores y empleados.

## Indicadores

Se calculan métricas como:

* Clientes registrados.
* Clientes activos.
* Cuentas bancarias.
* Saldo acumulado.
* Transferencias realizadas.
* Transferencias de los últimos 30 días.
* Monto transferido durante los últimos 30 días.
* Usuarios agrupados por rol.

## Exportación a Excel

Los clientes pueden exportarse a un archivo `.xlsx`.

Columnas generadas:

```text
Nombres
Apellidos
Documento
Teléfono
Email
Ciudad
Estado
Fecha Registro
```

La generación del archivo se realiza directamente desde Django utilizando `openpyxl`.

---

# 🏗️ Arquitectura del proyecto

El proyecto utiliza la arquitectura **MVT (Model-View-Template)** proporcionada por Django.

```text
                    ┌─────────────────────┐
                    │      Navegador      │
                    └──────────┬──────────┘
                               │ HTTP/HTTPS
                               ▼
                    ┌─────────────────────┐
                    │       Django        │
                    │       URLs          │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
         accounts          clientes          reportes
              │                │                │
              └────────────────┼────────────────┘
                               │
                               ▼
                         ┌───────────┐
                         │  Models   │
                         └─────┬─────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     Base de datos   │
                    │ PostgreSQL / SQLite │
                    └─────────────────────┘
```

Las aplicaciones se encuentran registradas en la configuración principal de Django:

```text
accounts
clientes
notificaciones
reportes
core
```

---

# 📁 Estructura de carpetas

La estructura principal del proyecto es:

```text
Banco2/
│
├── accounts/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── clientes/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── config/
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── core/
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── notificaciones/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── reportes/
│   ├── admin.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── templates/
│   └── ...
│
├── create_admin.py
├── manage.py
├── requirements.txt
├── .gitignore
└── README.md
```

La raíz del repositorio también contiene el directorio `.venv` actualmente, aunque este tipo de entorno virtual no debería formar parte del control de versiones.

---

# 🛠️ Tecnologías utilizadas

| Tecnología          | Uso                               |
| ------------------- | --------------------------------- |
| **Python**          | Lenguaje principal                |
| **Django 4.2**      | Framework web                     |
| **SQLite**          | Base de datos local por defecto   |
| **PostgreSQL**      | Base de datos para despliegue     |
| **Gunicorn**        | Servidor WSGI                     |
| **WhiteNoise**      | Servir archivos estáticos         |
| **openpyxl**        | Generación de archivos Excel      |
| **Pillow**          | Procesamiento de imágenes         |
| **python-dotenv**   | Variables de entorno              |
| **django-environ**  | Configuración mediante entorno    |
| **dj-database-url** | Configuración de la base de datos |
| **HTML/CSS**        | Interfaz web                      |

Las dependencias y versiones utilizadas se encuentran especificadas en `requirements.txt`.

---

# 📦 Requisitos

Para ejecutar el proyecto localmente se recomienda contar con:

* Python 3.10 o superior.
* Git.
* `pip`.
* Un entorno virtual de Python.

No es necesario instalar PostgreSQL para la configuración local predeterminada, ya que el proyecto utiliza SQLite cuando no existe la variable `DATABASE_URL`.

---

# 🚀 Instalación

## 1. Clonar el repositorio

```bash
git clone https://github.com/Che-0/Banco2.git
cd Banco2
```

---

## 2. Crear el entorno virtual

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Instalar las dependencias

```bash
pip install -r requirements.txt
```

---

# 🔐 Variables de entorno

El proyecto utiliza un archivo `.env` para almacenar configuraciones que no deberían incluirse directamente en el código fuente.

Crea un archivo:

```text
.env
```

en la raíz del proyecto.

Ejemplo:

```env
SECRET_KEY=tu_clave_secreta
DEBUG=True

ALLOWED_HOSTS=127.0.0.1,localhost

CSRF_TRUSTED_ORIGINS=http://127.0.0.1:8000,http://localhost:8000

EMAIL_HOST_USER=tu_correo@gmail.com
EMAIL_HOST_PASSWORD=tu_contraseña_de_aplicacion
```

El archivo `.env` está incluido en `.gitignore`, por lo que no debería subirse al repositorio.

> **Importante:** no utilices la contraseña normal de una cuenta de Gmail para SMTP. Si utilizas Gmail, configura una contraseña de aplicación cuando corresponda.

---

# 🗄️ Migraciones

Después de instalar las dependencias y configurar las variables de entorno:

```bash
python manage.py makemigrations
python manage.py migrate
```

Esto crea y actualiza las tablas necesarias para las aplicaciones del proyecto.

---

# 👨‍💼 Crear un administrador

El proyecto incluye el archivo:

```text
create_admin.py
```

Este script permite crear o actualizar usuarios a partir de variables de entorno.

Entre las variables utilizadas se encuentran:

```env
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PASSWORD=tu_contraseña
DJANGO_SUPERUSER_TELEFONO=
DJANGO_SUPERUSER_ROL=ADMIN
DJANGO_SUPERUSER_IS_SUPERUSER=true
DJANGO_SUPERUSER_IS_ACTIVE=true
```

También permite definir usuarios adicionales mediante `DJANGO_SEED_USERS` utilizando una lista JSON.

Por ejemplo:

```env
DJANGO_SEED_USERS=[{"username":"empleado","email":"empleado@example.com","password":"contraseña","telefono":"","rol":"EMPLEADO"}]
```

El script comprueba si el usuario ya existe y puede actualizar sus datos y contraseña durante el proceso.

**No almacenes contraseñas reales directamente en el repositorio.**

---

# ▶️ Ejecución

Una vez realizadas las migraciones:

```bash
python manage.py runserver
```

El proyecto estará disponible normalmente en:

```text
http://127.0.0.1:8000/
```

---

# 🗄️ Configuración de base de datos

Banco2 puede utilizar diferentes bases de datos dependiendo del entorno.

## Desarrollo local

Si no existe `DATABASE_URL`, Django utiliza SQLite:

```text
db.sqlite3
```

## Producción

Si existe:

```env
DATABASE_URL=...
```

el proyecto utiliza `dj-database-url` para configurar la conexión.

En producción, cuando `DEBUG=False`, la conexión se configura para requerir SSL.

---

# 🌐 Despliegue

La configuración del proyecto incluye soporte para un entorno de despliegue basado en un servidor WSGI.

El archivo:

```text
config/wsgi.py
```

expone la aplicación Django mediante:

```python
application = get_wsgi_application()
```

También existe una configuración ASGI en:

```text
config/asgi.py
```

Para un despliegue basado en Gunicorn puede utilizarse:

```bash
gunicorn config.wsgi:application
```

La dependencia `gunicorn` se encuentra definida en `requirements.txt`.

---

# 🎨 Archivos estáticos y multimedia

El proyecto utiliza:

```text
/static/
```

para los archivos estáticos y:

```text
/media/
```

para archivos multimedia.

La configuración utiliza **WhiteNoise** para servir archivos estáticos.

Las fotografías de los clientes se almacenan mediante el campo `ImageField` en una ruta similar a:

```text
clientes/fotos/
```

Se permiten imágenes con extensiones:

```text
.jpg
.jpeg
.png
.webp
```

---

# 🔒 Seguridad y autenticación

Banco2 aprovecha diferentes mecanismos proporcionados por Django.

### Autenticación

Utiliza el sistema de autenticación de Django con un modelo de usuario personalizado:

```python
AUTH_USER_MODEL = 'accounts.User'
```

### Protección de contraseñas

Las contraseñas son administradas mediante el sistema de autenticación de Django.

El proyecto también utiliza los validadores de contraseña proporcionados por Django, incluyendo:

* Similitud con atributos del usuario.
* Longitud mínima.
* Contraseñas comunes.
* Contraseñas numéricas.

### Control de acceso

Las vistas utilizan mecanismos como:

```python
@login_required
```

y:

```python
@user_passes_test(...)
```

además de `LoginRequiredMixin` y `UserPassesTestMixin`.

Esto permite restringir determinadas operaciones dependiendo del rol del usuario.

### HTTPS

Cuando `DEBUG=False`, la configuración activa:

* Redirección HTTPS.
* Cookies de sesión seguras.
* Cookies CSRF seguras.
* Configuración `SameSite`.

---

# ⚠️ Consideraciones

Este proyecto es una aplicación educativa y de demostración de conceptos de desarrollo web con Django.

Aunque implementa mecanismos como autenticación, control de permisos y transacciones de base de datos, **no debe considerarse un sistema bancario listo para manejar dinero real** sin una revisión de seguridad, arquitectura, auditoría y cumplimiento normativo mucho más exhaustiva.

Entre los aspectos que deberían revisarse antes de utilizar un sistema de este tipo en producción se encuentran:

* Gestión de secretos.
* Auditoría de operaciones.
* Manejo de concurrencia.
* Protección contra ataques.
* Registro de eventos.
* Recuperación ante errores.
* Gestión de sesiones.
* Validaciones financieras.
* Pruebas automatizadas.
* Protección de información sensible.
* Control de acceso más granular.
* Integridad y trazabilidad de transacciones.

---

# 🔧 Posibles mejoras

Algunas mejoras que podrían incorporarse en futuras versiones:

### Pruebas automatizadas

Agregar pruebas unitarias e integrales para:

* Login.
* Registro de usuarios.
* Registro de clientes.
* Creación de cuentas.
* Transferencias.
* Validación de saldo.
* Permisos.
* Reportes.

### API REST

Crear una API utilizando Django REST Framework para permitir que otros clientes consuman el sistema.

### Mejorar el sistema de transferencias

Incorporar controles adicionales para concurrencia y operaciones simultáneas.

### Auditoría

Crear un registro detallado de:

```text
Usuario
Acción
Fecha
IP
Objeto afectado
Resultado
```

### Notificaciones

Separar el envío de correos del proceso web mediante una cola de tareas como:

```text
Celery + Redis
```

en lugar de depender de hilos del proceso web.

### Mejorar el sistema de roles

Implementar permisos específicos por operación en lugar de depender únicamente del rol general.

### Seguridad

Incorporar:

* Rate limiting.
* 2FA/MFA.
* Políticas de sesión.
* Registro de eventos de seguridad.
* Monitoreo.
* Gestión centralizada de secretos.

---

# 📌 Resumen de módulos

| Aplicación       | Responsabilidad                    |
| ---------------- | ---------------------------------- |
| `accounts`       | Usuarios, autenticación y roles    |
| `clientes`       | Clientes, cuentas y transferencias |
| `core`           | Dashboard general                  |
| `notificaciones` | Notificaciones internas            |
| `reportes`       | Estadísticas, reportes y Excel     |
| `config`         | Configuración principal de Django  |

---

# 📚 Comandos útiles

### Crear migraciones

```bash
python manage.py makemigrations
```

### Aplicar migraciones

```bash
python manage.py migrate
```

### Ejecutar servidor

```bash
python manage.py runserver
```

### Crear superusuario

```bash
python manage.py createsuperuser
```

### Comprobar configuración

```bash
python manage.py check
```

---

# 👨‍💻 Autor

**Che-0**

Proyecto disponible en:

https://github.com/Che-0/Banco2

---

## 📄 Licencia

Este proyecto no especifica actualmente una licencia de software en el repositorio.
