# Inventory Management API

Sistema de gestión de inventarios con autenticación JWT y arquitectura modular construido con FastAPI y PostgreSQL.

## Descripción del Sistema

API RESTful para la administración de inventarios que implementa un sistema completo de autenticación mediante tokens JWT, gestión de usuarios, control de productos y registro de actividades. El sistema está diseñado con una arquitectura en capas que facilita el mantenimiento y escalabilidad.

### Funcionalidades Principales

**Autenticación y Usuarios**

- Registro de usuarios con validación de email
- Sistema de login con generación de tokens JWT
- Gestión completa de perfiles de usuario (CRUD)
- Hash seguro de contraseñas con bcrypt

**Gestión de Productos**

- Creación y administración de productos
- Categorización y control de stock
- Consulta de productos con filtros por categoría
- Generación de estadísticas de inventario

**Sistema de Auditoría**

- Registro automático de acciones de usuarios
- Consulta de logs por usuario
- Estadísticas de actividad del sistema

**Características Técnicas**

- Validación de datos con Pydantic
- Documentación interactiva con Swagger UI
- Respuestas JSON estandarizadas
- Código de estado HTTP apropiados

## Arquitectura

El sistema implementa un patrón de capas claramente definido:

```
Controller → Service → Repository → Model → Database
```

**Controller**: Maneja las peticiones HTTP y valida los datos de entrada  
**Service**: Contiene la lógica de negocio  
**Repository**: Gestiona el acceso a la base de datos  
**Model**: Define la estructura de las tablas

Este diseño permite la separación de responsabilidades y facilita el testing y mantenimiento del código.

## Stack Tecnológico

**Framework y Servidor**

- FastAPI 0.109.0
- Uvicorn 0.27.0

**Base de Datos**

- PostgreSQL 13+
- SQLAlchemy 2.0.25
- psycopg2-binary 2.9.9

**Seguridad**

- python-jose 3.3.0 (JWT)
- passlib 1.7.4 (Bcrypt)

**Validación**

- Pydantic 2.5.3
- email-validator 2.1.0

## Requisitos Previos

- Python 3.11 o superior
- PostgreSQL 13 o superior
- pip y venv
- Sistema operativo Linux (Debian/Ubuntu)

## Instalación

### 1. Preparar el entorno

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3.11 python3.11-venv python3-pip postgresql postgresql-contrib
```

### 2. Configurar el proyecto

```bash
# Crear directorio del proyecto
mkdir inventory-management-api && cd inventory-management-api

# Crear entorno virtual
python3.11 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install --upgrade pip
pip install fastapi==0.109.0 uvicorn[standard]==0.27.0 sqlalchemy==2.0.25 \
            psycopg2-binary==2.9.9 python-dotenv==1.0.0 passlib[bcrypt]==1.7.4 \
            python-jose[cryptography]==3.3.0 pydantic==2.5.3 \
            pydantic-settings==2.1.0 python-multipart==0.0.6 email-validator==2.1.0
```

### 3. Configurar PostgreSQL

```bash
sudo systemctl start postgresql
sudo systemctl enable postgresql
sudo -u postgres psql -c "CREATE DATABASE inventory_db;"
sudo -u postgres psql -c "ALTER USER postgres WITH PASSWORD 'postgres';"
```

### 4. Configurar variables de entorno

Crear archivo `.env` en la raíz del proyecto:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/inventory_db
SECRET_KEY=generate-a-secure-key-here-minimum-32-characters
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
PROJECT_NAME=Inventory Management API
VERSION=1.0.0
API_PREFIX=/api/v1
```

**Importante**: Generar una clave segura para producción:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 5. Iniciar el servidor

```bash
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

El servidor estará disponible en `http://localhost:8000`

## Documentación de la API

### Endpoints de Autenticación

**POST** `/api/v1/auth/register` - Registrar nuevo usuario  
**POST** `/api/v1/auth/login` - Iniciar sesión

### Endpoints de Usuarios

**GET** `/api/v1/users/me` - Obtener usuario actual  
**GET** `/api/v1/users/` - Listar usuarios  
**GET** `/api/v1/users/{id}` - Obtener usuario específico  
**PUT** `/api/v1/users/{id}` - Actualizar usuario  
**DELETE** `/api/v1/users/{id}` - Eliminar usuario

### Endpoints de Productos

**POST** `/api/v1/products/` - Crear producto  
**GET** `/api/v1/products/` - Listar productos (filtrable por categoría)  
**GET** `/api/v1/products/statistics` - Estadísticas de inventario  
**GET** `/api/v1/products/{id}` - Obtener producto específico  
**PUT** `/api/v1/products/{id}` - Actualizar producto  
**DELETE** `/api/v1/products/{id}` - Eliminar producto

### Endpoints de Logs

**POST** `/api/v1/logs/` - Crear registro de log  
**GET** `/api/v1/logs/` - Listar logs  
**GET** `/api/v1/logs/user/{user_id}` - Logs por usuario  
**GET** `/api/v1/logs/statistics` - Estadísticas de logs  
**GET** `/api/v1/logs/{id}` - Obtener log específico  
**DELETE** `/api/v1/logs/{id}` - Eliminar log

Todos los endpoints excepto registro e inicio de sesión requieren autenticación JWT mediante el header `Authorization: Bearer {token}`.

## Documentación Interactiva

Acceder a la documentación Swagger UI en: `http://localhost:8000/docs`

## Estructura del Proyecto

```
inventory-management-api/
├── app/
│   ├── main.py
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── security.py
│   │   └── utils.py
│   └── modules/
│       ├── users/
│       │   ├── models.py
│       │   ├── schemas.py
│       │   ├── repository.py
│       │   ├── service.py
│       │   └── controller.py
│       ├── products/
│       │   └── [misma estructura]
│       └── logs/
│           └── [misma estructura]
├── venv/
├── .env
└── requirements.txt
```

## Modelo de Datos

**users**

- id, name, email (unique), password (hash), created, updated

**products**

- id, name, category, price, stock, created, updated

**logs**

- id, user_id (FK), action, created, updated

## Seguridad

El sistema implementa:

- Autenticación JWT con tokens que expiran en 30 minutos
- Hashing de contraseñas con bcrypt (10 rounds)
- Validación de datos de entrada con Pydantic
- Variables sensibles almacenadas en archivo .env

### Recomendaciones para producción:

- Generar SECRET_KEY único y seguro
- Configurar CORS con orígenes específicos
- Implementar HTTPS
- Considerar rate limiting
- Usar base de datos en servidor dedicado

## Uso Básico

### Registrar usuario

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "email": "john@example.com", "password": "secure123"}'
```

### Iniciar sesión

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "john@example.com", "password": "secure123"}'
```

### Crear producto

```bash
curl -X POST "http://localhost:8000/api/v1/products/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {tu_token}" \
  -d '{"name": "Laptop", "category": "Electronics", "price": 899.99, "stock": 15}'
```
