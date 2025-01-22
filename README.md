# Instrucciones de Instalación

¡Bienvenido a la aplicación Marketplace! Sigue estos pasos para configurar y ejecutar la aplicación en tu máquina local.

## Requisitos Previos

- **Node.js y npm:**  Necesitarás Node.js y npm (Node Package Manager) instalados para gestionar dependencias de frontend. Puedes descargarlos desde la [página oficial de Node.js](https://nodejs.org/). Asegúrate de instalar Node.js antes de Docker y Docker Compose.

- **Docker y Docker Compose:** Asegúrate de tener Docker y Docker Compose instalados en tu sistema. Puedes seguir las instrucciones de instalación para tu sistema operativo en la documentación oficial de Docker.

## Instalación Paso a Paso (Docker)

1. **Navegar al directorio del proyecto:**
   Abre tu terminal y navega al directorio raíz del proyecto Marketplace:

   ```bash
   cd c:/tu/ruta/marketplace
   ```

2. **Iniciar la aplicación con Docker Compose (primera vez o con cambios):**
   Para la primera vez que ejecutas la aplicación o si has realizado cambios en el `Dockerfile` o en la configuración de Docker Compose, utiliza el siguiente comando para construir la imagen de Docker, crear y iniciar el contenedor:

   ```bash
   docker-compose up --build
   ```

   Este comando hará lo siguiente:
   - **--build:**  Construye la imagen Docker si hay cambios en el Dockerfile o si la imagen no existe.
   - **up:** Crea y arranca los contenedores definidos en el archivo `docker-compose.yml`.

   Docker Compose utilizará el `Dockerfile` para construir la imagen y el `docker-compose.yml` para configurar y ejecutar el contenedor.

3. **Iniciar la aplicación con Docker Compose (si la imagen ya existe):**
   Si ya has construido la imagen Docker previamente y no has realizado cambios en la configuración de Docker, puedes iniciar la aplicación más rápidamente utilizando solo el siguiente comando:

   ```bash
   docker-compose up
   ```

   Este comando simplemente creará y arrancará los contenedores definidos en `docker-compose.yml` utilizando la imagen ya construida.

4. **Acceder a la aplicación:**
   Una vez que Docker Compose haya terminado de levantar el contenedor (esto puede tardar la primera vez mientras se descarga la imagen y se instalan las dependencias), la aplicación estará accesible en `http://127.0.0.1:8000/` en tu navegador web.

## Detener la aplicación Dockerizada

Para detener la aplicación que se está ejecutando en Docker, puedes volver a tu terminal y presionar `Ctrl+C` para detener los logs, y luego ejecutar el siguiente comando en el mismo directorio del proyecto:

```bash
docker-compose down
```

Este comando detendrá y eliminará los contenedores y redes creados por `docker-compose up`.

para crear un usuario debes usar esta url: http://127.0.0.1:8000/accounts/register/?token=invitacion

## Endpoints de la API

### Módulo Accounts

#### Registro
- **URL:** `/accounts/register/?token=invitacion`
- **Método HTTP:** POST
- **Descripción:** Permite registrar un nuevo usuario en la plataforma. Requiere un token de invitación válido.
- **Parámetros de entrada:**
    - `username` (body): Nombre de usuario.
    - `email` (body): Correo electrónico del usuario.
    - `password` (body): Contraseña del usuario.
- **Ejemplo de solicitud:**
  ```json
  {
      "username": "nuevoUsuario",
      "email": "usuario@example.com",
      "password": "password123"
  }
  ```
- **Ejemplo de respuesta:**
  ```json
  // Redirección a la página principal tras registro exitoso.
  ```
- **Errores posibles:**
    - `400 Bad Request`: Si el token de invitación no es válido o si el formulario de registro contiene errores.

#### Login
- **URL:** `/accounts/login/`
- **Método HTTP:** POST
- **Descripción:** Permite a un usuario registrado iniciar sesión en la plataforma.
- **Parámetros de entrada:**
    - `username` (body): Nombre de usuario.
    - `password` (body): Contraseña del usuario.
- **Ejemplo de solicitud:**
  ```json
  {
      "username": "usuario",
      "password": "password123"
  }
  ```
- **Ejemplo de respuesta:**
  ```json
  // Redirección a la página principal tras inicio de sesión exitoso.
  ```
- **Errores posibles:**
    - `400 Bad Request`: Si las credenciales son incorrectas.

#### Perfil de usuario
- **URL:** `/accounts/profile/`
- **Método HTTP:** GET
- **Descripción:** Muestra el perfil del usuario actualmente autenticado.
- **Ejemplo de respuesta:**
  ```json
  {
      "active_tab": "info",
      "is_admin": false,
      "user_profile": {
          // ... datos del perfil del usuario
      },
      "editing": false
  }
  ```

#### Editar perfil de usuario
- **URL:** `/accounts/profile/?tab=info&action=edit`
- **Método HTTP:** POST
- **Descripción:** Permite editar el perfil del usuario autenticado.
- **Parámetros de entrada:**
    - Formulario con los campos del perfil a editar (nombre, imagen de perfil, etc.).
- **Ejemplo de solicitud:**
  ```form-data
  // Formulario con los datos a actualizar.
  ```
- **Ejemplo de respuesta:**
  ```json
  // Redirección al perfil del usuario tras la actualización exitosa.
  ```

#### Historial de compras
- **URL:** `/accounts/profile/purchase-history/`
- **Método HTTP:** GET
- **Descripción:** Muestra el historial de compras del usuario autenticado.
- **Ejemplo de respuesta:**
  ```json
  {
      "purchases": [
          // ... lista de productos comprados
      ]
  }
  ```

#### Productos vendidos
- **URL:** `/accounts/profile/sold-products/`
- **Método HTTP:** GET
- **Descripción:** Muestra los productos vendidos por el usuario autenticado.
- **Ejemplo de respuesta:**
  ```json
  {
      "products": [
          // ... lista de productos vendidos
      ]
  }
  ```

#### Detalle de perfil de usuario (público)
- **URL:** `/accounts/user/<int:user_id>/`
- **Método HTTP:** GET
- **Descripción:** Muestra el perfil público de un usuario específico por su ID.
- **Parámetros de entrada:**
    - `user_id` (URL): ID del usuario a consultar.
- **Ejemplo de respuesta:**
  ```json
  {
      "profile_user": {
          // ... datos del perfil público del usuario
      },
      "sold_products": [
          // ... lista de productos vendidos por el usuario
      ],
      "ratings": [
          // ... lista de valoraciones recibidas por el usuario
      ],
      "average_rating": 4.5
  }
  ```

#### Resolver reporte de usuario (Admin)
- **URL:** `/accounts/report/<int:report_id>/resolve/`
- **Método HTTP:** POST
- **Descripción:** Permite a un administrador resolver o descartar un reporte de usuario.
- **Parámetros de entrada:**
    - `report_id` (URL): ID del reporte a resolver.
    - `action` (body): Acción a realizar (`resolve` o `dismiss`).
- **Ejemplo de solicitud:**
  ```form-data
  action=resolve
  ```
- **Ejemplo de respuesta:**
  ```json
  // Redirección al panel de administración tras resolver el reporte.
  ```
- **Errores posibles:**
    - `403 Forbidden`: Si el usuario no es administrador.

### Módulo Chat

#### Lista de conversaciones
- **URL:** `/chat/`
- **Método HTTP:** GET
- **Descripción:** Lista todas las conversaciones del usuario autenticado.
- **Ejemplo de respuesta:**
  ```json
  {
      "conversations": [
          {
              "conversation": {
                  // ... datos de la conversación
              },
              "unread_count": 2
          },
          // ... más conversaciones
      ]
  }
  ```

#### Detalle de conversación
- **URL:** `/chat/<uuid:pk>/`
- **Método HTTP:** GET
- **Descripción:** Muestra el detalle de una conversación específica, incluyendo los mensajes.
- **Parámetros de entrada:**
    - `pk` (URL): UUID de la conversación.
- **Ejemplo de respuesta:**
  ```json
  {
      "conversation": {
          // ... datos de la conversación
      },
      "messages": [
          // ... lista de mensajes
      ],
      "product": {
          // ... datos del producto asociado
      },
      "has_received_ratings": false,
      "buyer": {
          // ... datos del comprador si existe
      }
  }
  ```

#### Enviar mensaje
- **URL:** `/chat/<uuid:pk>/send/`
- **Método HTTP:** POST
- **Descripción:** Permite enviar un nuevo mensaje en una conversación.
- **Parámetros de entrada:**
    - `pk` (URL): UUID de la conversación.
    - `content` (body): Contenido del mensaje.
- **Ejemplo de solicitud:**
  ```form-data
  content=Hola, ¿está todavía disponible?
  ```
- **Ejemplo de respuesta:**
  ```json
  // Redirección al detalle de la conversación tras enviar el mensaje.
  ```
- **Errores posibles:**
    - `400 Bad Request`: Si la solicitud no es válida.
    - `403 Forbidden`: Si la conversación está cerrada o el producto retirado.

#### Iniciar conversación
- **URL:** `/chat/start/<int:product_id>/`
- **Método HTTP:** GET
- **Descripción:** Inicia una nueva conversación con el vendedor de un producto específico.
- **Parámetros de entrada:**
    - `product_id` (URL): ID del producto.
- **Ejemplo de respuesta:**
  ```json
  // Redirección al detalle de la conversación iniciada.
  ```
- **Errores posibles:**
    - `400 Bad Request`: Si el usuario intenta chatear consigo mismo.

#### Valorar vendedor
- **URL:** `/chat/<uuid:pk>/rate_seller/`
- **Método HTTP:** GET, POST
- **Descripción:** Permite al comprador valorar al vendedor tras la compra de un producto.
- **Parámetros de entrada (POST):**
    - `pk` (URL): UUID de la conversación.
    - `score` (body): Puntuación otorgada al vendedor.
    - `comment` (body): Comentario opcional sobre la valoración.
- **Ejemplo de solicitud (POST):**
  ```form-data
  score=5
  comment=Excelente vendedor, muy recomendado.
  ```
- **Ejemplo de respuesta:**
  ```json
  // Redirección al detalle de la conversación tras realizar la valoración.
  ```
- **Errores posibles:**
    - `403 Forbidden`: Si el usuario no es el comprador o el producto no está vendido.

### Módulo Products

#### Detalle de producto
- **URL:** `/products/<int:pk>/`
- **Método HTTP:** GET
- **Descripción:** Muestra el detalle de un producto específico por su ID.
- **Parámetros de entrada:**
    - `pk` (URL): ID del producto.
- **Ejemplo de respuesta:**
  ```json
  {
      "product": {
          // ... datos del producto
      },
      "images": [
          // ... lista de imágenes del producto
      ],
      "user": {
          // ... datos del usuario actual
      },
      "buyers": [
          // ... lista de compradores potenciales
      ]
  }
  ```

#### Añadir producto
- **URL:** `/products/add/`
- **Método HTTP:** GET, POST
- **Descripción:** Permite a un usuario autenticado añadir un nuevo producto a la venta.
- **Parámetros de entrada (POST):**
    - Formulario con los campos del producto (título, descripción, precio, imágenes, etc.).
- **Ejemplo de solicitud (POST):**
  ```form-data
  // Formulario con los datos del producto a añadir.
  ```
- **Ejemplo de respuesta:**
  ```json
  // Redirección a la página principal tras añadir el producto exitosamente.
  ```

#### Chatear con el vendedor (producto)
- **URL:** `/products/<int:product_id>/chat/`
- **Método HTTP:** GET
- **Descripción:** Inicia una conversación con el vendedor desde la página de detalle del producto.
- **Parámetros de entrada:**
    - `product_id` (URL): ID del producto.
- **Ejemplo de respuesta:**
  ```json
  // Redirección al detalle de la conversación iniciada.
  ```

#### Reportar producto
- **URL:** `/products/report/<int:product_id>/`
- **Método HTTP:** GET, POST
- **Descripción:** Permite a un usuario reportar un producto por contenido inapropiado u otras razones.
- **Parámetros de entrada (POST):**
    - `product_id` (URL): ID del producto a reportar.
    - Formulario `ReportForm` con el motivo del reporte.
- **Ejemplo de solicitud (POST):**
  ```form-data
  // Formulario con el motivo del reporte.
  ```
- **Ejemplo de respuesta:**
  ```json
  // Redirección al detalle del producto tras enviar el reporte.
  ```

#### Marcar como vendido o retirar producto
- **URL:** `/products/products/<int:pk>/manage/`
- **Método HTTP:** POST
- **Descripción:** Permite al vendedor marcar un producto como vendido o retirarlo de la venta.
- **Parámetros de entrada:**
    - `pk` (URL): ID del producto.
    - `action` (body): Acción a realizar (`sell` o `withdraw`).
    - `buyer` (body, opcional si action=sell): ID del comprador (solo si se marca como vendido).
- **Ejemplo de solicitud (POST - vender):**
  ```form-data
  action=sell&buyer=3
  ```
- **Ejemplo de solicitud (POST - retirar):**
  ```form-data
  action=withdraw
  ```
- **Ejemplo de respuesta:**
  ```json
  // Redirección al detalle del producto tras realizar la acción.
  ```

### Módulo Marketplace

#### Home (Listado de productos)
- **URL:** `/`
- **Método HTTP:** GET
- **Descripción:** Muestra la página principal con un listado de productos disponibles en el marketplace.
- **Ejemplo de respuesta:**
  ```json
  {
      "products": [
          // ... lista de productos disponibles
      ]
  }
