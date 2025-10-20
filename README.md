# 🏢 Inventory Management API

> Prueba Técnica - Sistema de gestión de inventarios con autenticación JWT, arquitectura modular y PostgreSQL

[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-009688.svg?style=flat&logo=FastAPI)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB.svg?style=flat&logo=python)](https://www.python.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-336791.svg?style=flat&logo=postgresql)](https://www.postgresql.org)

## 📋 Tabla de Contenidos

- [Descripción](#-descripción)
- [Características](#-características)
- [Arquitectura](#-arquitectura)
- [Tecnologías](#-tecnologías)
- [Requisitos Previos](#-requisitos-previos)
- [Instalación](#-instalación)
- [Configuración](#-configuración)
- [Uso](#-uso)
- [Endpoints API](#-endpoints-api)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Base de Datos](#-base-de-datos)
- [Seguridad](#-seguridad)

---

## ✨ Características

### Funcionalidades Principales

- ✅ **Autenticación JWT** - Sistema completo de registro e inicio de sesión con tokens seguros
- ✅ **Gestión de Usuarios** - CRUD completo con validación de emails y hash de contraseñas
- ✅ **Gestión de Productos** - Control total del inventario con categorías y stock
- ✅ **Sistema de Logs** - Registro de acciones de usuarios para auditoría
- ✅ **Estadísticas** - Reportes y métricas del inventario en tiempo real
- ✅ **Documentación Interactiva** - Swagger UI y ReDoc integrados
- ✅ **Validación de Datos** - Esquemas Pydantic para entrada/salida segura
- ✅ **Respuestas Consistentes** - Formato JSON estandarizado con códigos HTTP apropiados

### Características Técnicas

- 🏗️ **Arquitectura Modular** - Separación por dominios (users, products, logs)
- 🔒 **Seguridad Robusta** - Bcrypt para contraseñas, JWT para sesiones
- 🗄️ **ORM SQLAlchemy** - Abstracción de base de datos con migraciones automáticas
- 🚀 **Alto Rendimiento** - Servidor ASGI con Uvicorn
- 📦 **Escalable** - Diseño preparado para crecimiento horizontal
- 🔧 **Configurable** - Variables de entorno para diferentes ambientes
- 📝 **Código Limpio** - Separación de responsabilidades (MVC + Repository Pattern)

---

## 🏛️ Arquitectura

### Patrón de Capas

```
┌─────────────────────────────────────┐
│         Controller Layer            │  ← Rutas FastAPI, validación HTTP
├─────────────────────────────────────┤
│          Service Layer              │  ← Lógica de negocio
├─────────────────────────────────────┤
│        Repository Layer             │  ← Acceso a datos, queries
├─────────────────────────────────────┤
│          Model Layer                │  ← Definición de tablas SQLAlchemy
├─────────────────────────────────────┤
│         Database (PostgreSQL)       │  ← Persistencia
└─────────────────────────────────────┘
```

### Principios de Diseño

- **Separation of Concerns**: Cada capa tiene una responsabilidad única
- **Dependency Injection**: Inyección de dependencias con FastAPI Depends
- **Repository Pattern**: Abstracción del acceso a datos
- **DTO Pattern**: Uso de schemas Pydantic para transferencia de datos
- **Single Responsibility**: Cada módulo maneja un dominio específico

---

## 🛠️ Tecnologías

### Backend Framework

- **FastAPI 0.109.0** - Framework web moderno y de alto rendimiento
- **Uvicorn 0.27.0** - Servidor ASGI para Python

### Base de Datos

- **PostgreSQL 13+** - Sistema de gestión de bases de datos relacional
- **SQLAlchemy 2.0.25** - ORM Python
- **psycopg2-binary 2.9.9** - Adaptador PostgreSQL para Python

### Autenticación y Seguridad

- **python-jose 3.3.0** - Implementación JWT
- **passlib 1.7.4** - Hashing de contraseñas con bcrypt
- **python-multipart 0.0.6** - Manejo de formularios multipart

### Validación y Configuración

- **Pydantic 2.5.3** - Validación de datos y configuración
- **pydantic-settings 2.1.0** - Gestión de configuración
- **email-validator 2.1.0** - Validación de emails
- **python-dotenv 1.0.0** - Carga de variables de entorno

---

## 📦 Requisitos Previos

### Sistema Operativo

- **Debian 12** / Ubuntu 20.04+ / Linux compatible
- Acceso a terminal con permisos sudo

### Software Base

```bash
- Python 3.11 o superior
- PostgreSQL 13 o superior
- pip (gestor de paquetes Python)
- venv (entorno virtual Python)
- Git (opcional, para control de versiones)
```

---

## 🚀 Instalación

### 1. Instalar Dependencias del Sistema

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3.11 python3.11-venv python3-pip postgresql postgresql-contrib
```

### 2. Clonar o Crear el Proyecto

```bash
mkdir -p ~/Documents/inventory-management-api
cd ~/Documents/inventory-management-api
```

### 3. Crear Estructura del Proyecto

```bash
mkdir -p app/core app/modules/users app/modules/products app/modules/logs
touch app/__init__.py \
      app/main.py \
      app/core/__init__.py \
      app/core/config.py \
      app/core/database.py \
      app/core/security.py \
      app/core/utils.py \
      app/modules/__init__.py \
      app/modules/users/__init__.py \
      app/modules/users/models.py \
      app/modules/users/schemas.py \
      app/modules/users/repository.py \
      app/modules/users/service.py \
      app/modules/users/controller.py \
      app/modules/products/__init__.py \
      app/modules/products/models.py \
      app/modules/products/schemas.py \
      app/modules/products/repository.py \
      app/modules/products/service.py \
      app/modules/products/controller.py \
      app/modules/logs/__init__.py \
      app/modules/logs/models.py \
      app/modules/logs/schemas.py \
      app/modules/logs/repository.py \
      app/modules/logs/service.py \
      app/modules/logs/controller.py \
      requirements.txt \
      .env \
      .gitignore
```

### 4. Crear Entorno Virtual

```bash
python3.11 -m venv venv
source venv/bin/activate
```

### 5. Crear requirements.txt

```bash
cat > requirements.txt << 'EOF'
fastapi==0.109.0
uvicorn[standard]==0.27.0
sqlalchemy==2.0.25
psycopg2-binary==2.9.9
python-dotenv==1.0.0
passlib[bcrypt]==1.7.4
python-jose[cryptography]==3.3.0
pydantic==2.5.3
pydantic-settings==2.1.0
python-multipart==0.0.6
email-validator==2.1.0
EOF
```

### 6. Instalar Dependencias Python

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 7. Configurar PostgreSQL

```bash
sudo systemctl start postgresql
sudo systemctl enable postgresql
sudo -u postgres psql -c "CREATE DATABASE inventory_db;"
sudo -u postgres psql -c "ALTER USER postgres WITH PASSWORD 'postgres';"
```

### 8. Configurar Variables de Entorno

```bash
cat > .env << 'EOF'
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/inventory_db
SECRET_KEY=your-super-secret-key-change-this-in-production-min-32-chars-123456
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
PROJECT_NAME=Inventory Management API
VERSION=1.0.0
API_PREFIX=/api/v1
EOF
```

**⚠️ IMPORTANTE**: Cambia `SECRET_KEY` en producción por una clave segura única.

### 9. Copiar el Código Fuente

Copia todos los archivos Python generados anteriormente en sus respectivas ubicaciones dentro de la estructura `app/`.

### 10. Ejecutar el Servidor

```bash
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

El servidor estará disponible en: **http://localhost:8000**

---

## ⚙️ Configuración

### Variables de Entorno (.env)

| Variable                      | Descripción                                 | Valor por Defecto                                            |
| ----------------------------- | ------------------------------------------- | ------------------------------------------------------------ |
| `DATABASE_URL`                | URL de conexión a PostgreSQL                | `postgresql://postgres:postgres@localhost:5432/inventory_db` |
| `SECRET_KEY`                  | Clave secreta para JWT (mín. 32 caracteres) | `your-super-secret-key...`                                   |
| `ALGORITHM`                   | Algoritmo de encriptación JWT               | `HS256`                                                      |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Tiempo de expiración del token en minutos   | `30`                                                         |
| `PROJECT_NAME`                | Nombre del proyecto                         | `Inventory Management API`                                   |
| `VERSION`                     | Versión de la API                           | `1.0.0`                                                      |
| `API_PREFIX`                  | Prefijo para todas las rutas                | `/api/v1`                                                    |

### Generar SECRET_KEY Segura

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

## 💻 Uso

### Acceder a la Documentación Interactiva

#### Swagger UI

```
http://localhost:8000/docs
```

Interfaz interactiva para probar todos los endpoints.

#### ReDoc

```
http://localhost:8000/redoc
```

Documentación alternativa en formato ReDoc.

### Verificar Estado del Servidor

```bash
curl http://localhost:8000/health
```

**Respuesta esperada:**

```json
{
	"status": "healthy"
}
```

### Ejemplo de Flujo Completo

#### 1. Registrar Usuario

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "securepass123"
  }'
```

#### 2. Iniciar Sesión (Obtener Token)

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "securepass123"
  }'
```

**Respuesta:**

```json
{
	"success": true,
	"message": "Login successful",
	"data": {
		"access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
		"token_type": "bearer"
	}
}
```

#### 3. Crear Producto (Con Token)

```bash
curl -X POST "http://localhost:8000/api/v1/products/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TU_TOKEN_AQUI>" \
  -d '{
    "name": "Laptop HP",
    "category": "Electronics",
    "price": 899.99,
    "stock": 15
  }'
```

#### 4. Obtener Estadísticas

```bash
curl -X GET "http://localhost:8000/api/v1/products/statistics" \
  -H "Authorization: Bearer <TU_TOKEN_AQUI>"
```

---

## 🔌 Endpoints API

### Autenticación (`/api/v1/auth`)

| Método | Endpoint    | Descripción                  | Auth Requerida |
| ------ | ----------- | ---------------------------- | -------------- |
| `POST` | `/register` | Registrar nuevo usuario      | ❌             |
| `POST` | `/login`    | Iniciar sesión y obtener JWT | ❌             |

### Usuarios (`/api/v1/users`)

| Método   | Endpoint     | Descripción                      | Auth Requerida |
| -------- | ------------ | -------------------------------- | -------------- |
| `GET`    | `/me`        | Obtener datos del usuario actual | ✅             |
| `GET`    | `/`          | Listar todos los usuarios        | ✅             |
| `GET`    | `/{user_id}` | Obtener usuario por ID           | ✅             |
| `PUT`    | `/{user_id}` | Actualizar usuario               | ✅             |
| `DELETE` | `/{user_id}` | Eliminar usuario                 | ✅             |

### Productos (`/api/v1/products`)

| Método   | Endpoint        | Descripción                                | Auth Requerida |
| -------- | --------------- | ------------------------------------------ | -------------- |
| `POST`   | `/`             | Crear nuevo producto                       | ✅             |
| `GET`    | `/`             | Listar productos (filtrable por categoría) | ✅             |
| `GET`    | `/statistics`   | Obtener estadísticas de productos          | ✅             |
| `GET`    | `/{product_id}` | Obtener producto por ID                    | ✅             |
| `PUT`    | `/{product_id}` | Actualizar producto                        | ✅             |
| `DELETE` | `/{product_id}` | Eliminar producto                          | ✅             |

### Logs (`/api/v1/logs`)

| Método   | Endpoint          | Descripción                  | Auth Requerida |
| -------- | ----------------- | ---------------------------- | -------------- |
| `POST`   | `/`               | Crear registro de log        | ✅             |
| `GET`    | `/`               | Listar todos los logs        | ✅             |
| `GET`    | `/user/{user_id}` | Obtener logs de un usuario   | ✅             |
| `GET`    | `/statistics`     | Obtener estadísticas de logs | ✅             |
| `GET`    | `/{log_id}`       | Obtener log por ID           | ✅             |
| `DELETE` | `/{log_id}`       | Eliminar log                 | ✅             |

### Formato de Respuesta Estándar

#### Respuesta Exitosa

```json
{
  "success": true,
  "message": "Operation completed successfully",
  "data": { ... },
  "timestamp": "2025-10-20T10:30:00.000000"
}
```

#### Respuesta de Error

```json
{
  "success": false,
  "message": "Error description",
  "timestamp": "2025-10-20T10:30:00.000000",
  "details": { ... }
}
```

### Códigos de Estado HTTP

| Código | Descripción                               |
| ------ | ----------------------------------------- |
| `200`  | Operación exitosa                         |
| `201`  | Recurso creado exitosamente               |
| `400`  | Petición incorrecta (validación fallida)  |
| `401`  | No autenticado (token inválido o ausente) |
| `404`  | Recurso no encontrado                     |
| `500`  | Error interno del servidor                |

---

## 📁 Estructura del Proyecto

```
inventory-management-api/
│
├── app/
│   ├── __init__.py
│   ├── main.py                      # Punto de entrada FastAPI
│   │
│   ├── core/                        # Núcleo del sistema
│   │   ├── __init__.py
│   │   ├── config.py                # Configuración y variables de entorno
│   │   ├── database.py              # Conexión SQLAlchemy + sesión DB
│   │   ├── security.py              # Hashing passwords + JWT utils
│   │   └── utils.py                 # Funciones auxiliares comunes
│   │
│   └── modules/                     # Módulos por dominio
│       │
│       ├── users/                   # Dominio: Usuarios
│       │   ├── __init__.py
│       │   ├── models.py            # Tabla User (SQLAlchemy)
│       │   ├── schemas.py           # DTOs Pydantic (request/response)
│       │   ├── repository.py        # Acceso a datos (queries)
│       │   ├── service.py           # Lógica de negocio
│       │   └── controller.py        # Rutas FastAPI (endpoints)
│       │
│       ├── products/                # Dominio: Productos
│       │   ├── __init__.py
│       │   ├── models.py            # Tabla Product
│       │   ├── schemas.py           # DTOs Pydantic
│       │   ├── repository.py        # Queries de productos
│       │   ├── service.py           # Lógica de negocio
│       │   └── controller.py        # Endpoints de productos
│       │
│       └── logs/                    # Dominio: Logs
│           ├── __init__.py
│           ├── models.py            # Tabla Log
│           ├── schemas.py           # DTOs Pydantic
│           ├── repository.py        # Queries de logs
│           ├── service.py           # Lógica de negocio
│           └── controller.py        # Endpoints de logs
│
├── venv/                            # Entorno virtual Python
├── .env                             # Variables de entorno (NO subir a Git)
├── .gitignore                       # Archivos ignorados por Git
├── requirements.txt                 # Dependencias Python
└── README.md                        # Documentación del proyecto
```

### Descripción de Capas

#### **Controller (controller.py)**

- Define las rutas y endpoints de FastAPI
- Maneja la validación HTTP
- Orquesta las llamadas al Service Layer
- Retorna respuestas HTTP formateadas

#### **Service (service.py)**

- Contiene la lógica de negocio
- Coordina operaciones complejas
- Valida reglas de negocio
- Transforma datos entre capas

#### **Repository (repository.py)**

- Abstrae el acceso a la base de datos
- Ejecuta queries SQL mediante SQLAlchemy
- No contiene lógica de negocio
- Retorna modelos de dominio

#### **Models (models.py)**

- Define las tablas de la base de datos
- Usa SQLAlchemy ORM
- Representa la estructura persistente

#### **Schemas (schemas.py)**

- Define DTOs con Pydantic
- Valida datos de entrada/salida
- Serializa/deserializa JSON

---

## 🗄️ Base de Datos

### Diagrama de Entidades

```
┌─────────────────────┐
│       users         │
├─────────────────────┤
│ id         (PK)     │
│ name                │
│ email      (UNIQUE) │
│ password            │
│ created             │
│ updated             │
└──────────┬──────────┘
           │
           │ 1:N
           │
┌──────────▼──────────┐
│       logs          │
├─────────────────────┤
│ id         (PK)     │
│ user_id    (FK)     │
│ action              │
│ created             │
│ updated             │
└─────────────────────┘

┌─────────────────────┐
│     products        │
├─────────────────────┤
│ id         (PK)     │
│ name                │
│ category            │
│ price               │
│ stock               │
│ created             │
│ updated             │
└─────────────────────┘
```

### Tablas

#### **users**

| Campo      | Tipo      | Restricciones               |
| ---------- | --------- | --------------------------- |
| `id`       | INTEGER   | PRIMARY KEY, AUTO_INCREMENT |
| `name`     | TEXT      | NOT NULL                    |
| `email`    | TEXT      | UNIQUE, NOT NULL            |
| `password` | TEXT      | NOT NULL (hash bcrypt)      |
| `created`  | TIMESTAMP | DEFAULT NOW()               |
| `updated`  | TIMESTAMP | ON UPDATE NOW()             |

#### **products**

| Campo      | Tipo          | Restricciones               |
| ---------- | ------------- | --------------------------- |
| `id`       | INTEGER       | PRIMARY KEY, AUTO_INCREMENT |
| `name`     | TEXT          | NOT NULL                    |
| `category` | TEXT          | NOT NULL                    |
| `price`    | NUMERIC(10,2) | NOT NULL, > 0               |
| `stock`    | INTEGER       | NOT NULL, >= 0              |
| `created`  | TIMESTAMP     | DEFAULT NOW()               |
| `updated`  | TIMESTAMP     | ON UPDATE NOW()             |

#### **logs**

| Campo     | Tipo      | Restricciones                           |
| --------- | --------- | --------------------------------------- |
| `id`      | INTEGER   | PRIMARY KEY, AUTO_INCREMENT             |
| `user_id` | INTEGER   | FOREIGN KEY → users(id), CASCADE DELETE |
| `action`  | TEXT      | NOT NULL                                |
| `created` | TIMESTAMP | DEFAULT NOW()                           |
| `updated` | TIMESTAMP | ON UPDATE NOW()                         |

### Migraciones

Las tablas se crean automáticamente al iniciar el servidor por primera vez gracias a SQLAlchemy:

```python
Base.metadata.create_all(bind=engine)
```

Para recrear la base de datos desde cero:

```bash
sudo -u postgres psql -c "DROP DATABASE IF EXISTS inventory_db;"
sudo -u postgres psql -c "CREATE DATABASE inventory_db;"
```

---

## 🔒 Seguridad

### Autenticación JWT

#### Flujo de Autenticación

1. Usuario se registra con email y contraseña
2. Contraseña se hashea con bcrypt (10 rounds)
3. Usuario inicia sesión con credenciales
4. Sistema valida credenciales y genera JWT
5. Cliente incluye JWT en header `Authorization: Bearer <token>`
6. Sistema valida JWT en cada petición protegida

#### Estructura del Token JWT

```json
{
	"sub": "user@example.com",
	"exp": 1729512000
}
```

- `sub`: Email del usuario (subject)
- `exp`: Timestamp de expiración (30 minutos por defecto)

### Hashing de Contraseñas

- **Algoritmo**: Bcrypt con 10 rounds
- **Librería**: passlib[bcrypt]
- **Formato**: `$2b$10$...` (60 caracteres)

### Protección de Endpoints

```python
@router.get("/protected")
def protected_route(current_user: UserResponse = Depends(get_current_user)):
    return {"message": f"Hello {current_user.name}"}
```

### Mejores Prácticas Implementadas

✅ Contraseñas hasheadas (nunca en texto plano)
✅ Tokens JWT con expiración
✅ Validación de entrada con Pydantic
✅ Variables sensibles en `.env`
✅ CORS configurado (ajustar en producción)
✅ Validación de email con email-validator
✅ Cascade delete en relaciones FK

### Recomendaciones para Producción

⚠️ Cambiar `SECRET_KEY` por una clave única y segura
⚠️ Configurar CORS con orígenes específicos
⚠️ Usar HTTPS (TLS/SSL)
⚠️ Implementar rate limiting
⚠️ Agregar logging y monitoreo
⚠️ Usar PostgreSQL en servidor dedicado
⚠️ Implementar refresh tokens
⚠️ Agregar validación 2FA (opcional)

---

## 🧪 Testing

### Probar con cURL

#### Registro de Usuario

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "password": "testpass123"
  }'
```

#### Login

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpass123"
  }'
```

#### Crear Producto

```bash
TOKEN="tu_token_aqui"

curl -X POST "http://localhost:8000/api/v1/products/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "name": "iPhone 15",
    "category": "Electronics",
    "price": 999.99,
    "stock": 50
  }'
```

### Probar con Swagger UI

1. Abrir http://localhost:8000/docs
2. Clic en endpoint `/auth/register`
3. Clic en "Try it out"
4. Ingresar datos de prueba
5. Clic en "Execute"
6. Repetir con `/auth/login` para obtener token
7. Clic en botón "Authorize" (candado verde)
8. Pegar token y confirmar
9. Probar endpoints protegidos

---

## 🤝 Contribución

### Guía de Contribución

1. Fork el proyecto
2. Crear rama de feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

### Estándares de Código

- Usar **PEP 8** para estilo Python
- Documentar funciones con docstrings
- Agregar type hints cuando sea posible
- Mantener separación de capas
- Escribir tests unitarios (futuro)

---

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo `LICENSE` para más detalles.

---

## 👨‍💻 Autor

**Tu Nombre**

- GitHub: [@tuusuario](https://github.com/tuusuario)
- Email: tu@email.com

---

## 🙏 Agradecimientos

- [FastAPI](https://fastapi.tiangolo.com/) - Framework web moderno
- [SQLAlchemy](https://www.sqlalchemy.org/) - ORM robusto
- [Pydantic](https://pydantic-docs.helpmanual.io/) - Validación de datos
- [PostgreSQL](https://www.postgresql.org/) - Base de datos confiable

---

## 📞 Soporte

Si encuentras algún problema o tienes preguntas:

1. Revisar la documentación en `/docs`
2. Buscar en [Issues](https://github.com/tuusuario/inventory-api/issues)
3. Crear un nuevo Issue
4. Contactar al equipo de desarrollo

---

## 🗺️ Roadmap

### Versión 1.1 (Próxima)

- [ ] Implementar refresh tokens
- [ ] Agregar paginación avanzada
- [ ] Sistema de roles y permisos
- [ ] Búsqueda y filtros avanzados
- [ ] Exportación de reportes (PDF/Excel)

### Versión 1.2

- [ ] Tests unitarios con pytest
- [ ] CI/CD con GitHub Actions
- [ ] Containerización con Docker
- [ ] Documentación adicional con MkDocs

### Versión 2.0

- [ ] WebSockets para notificaciones en tiempo real
- [ ] Dashboard administrativo
- [ ] API GraphQL alternativa
- [ ] Integración con servicios externos

---

## 📊 Estado del Proyecto

✅ **Funcional** - El proyecto está completo y operativo para desarrollo.

**Última actualización**: Octubre 2025

---

<div align="center">

**¿Te resultó útil este proyecto? ¡Dale una ⭐ en GitHub!**

</div>
