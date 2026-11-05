# Blog Web con Django

Blog web desarrollado con Django donde los usuarios pueden registrarse, iniciar sesión, publicar posts con imagen, editarlos, eliminarlos y buscarlos. Proyecto final del curso de Python.

## Tecnologías

- Python 3
- Django 6
- SQLite
- Pillow (manejo de imágenes)
- python-decouple (variables de entorno)
- Bootstrap 5 (vía CDN)

## Funcionalidades principales

- **Posts**: listado paginado, detalle, creación, edición y eliminación desde la interfaz web.
- **Imágenes**: cada post puede tener una imagen; si no la tiene, las páginas se muestran igual.
- **Búsqueda**: por título o contenido, con aviso cuando no hay coincidencias.
- **Usuarios**: registro, login y logout.
- **Perfil**: vista de perfil, edición de datos e imagen de perfil.
- **Rutas protegidas**: crear, editar y eliminar posts y editar el perfil requieren sesión iniciada (`LoginRequiredMixin` / `@login_required`). Solo el autor puede editar o eliminar sus posts.
- **Panel de administración** de Django.

## Instalación

1. Clonar el repositorio:

```bash
git clone https://github.com/DamianLeandroF/blog-django.git
cd blog-django
```

2. Crear y activar el entorno virtual:

```bash
python -m venv venv
```

Windows (PowerShell):

```bash
venv\Scripts\Activate.ps1
```

Linux / macOS:

```bash
source venv/bin/activate
```

3. Instalar las dependencias:

```bash
pip install -r requirements.txt
```

4. (Opcional) Configurar variables de entorno copiando el archivo de ejemplo. Si no se crea `.env`, se usan valores de desarrollo por defecto.

```bash
cp .env.example .env
```

5. Aplicar las migraciones (crea `db.sqlite3` desde cero):

```bash
python manage.py migrate
```

6. Crear un superusuario para acceder al panel `/admin/`:

```bash
python manage.py createsuperuser
```

7. Iniciar el servidor:

```bash
python manage.py runserver
```

Abrir <http://127.0.0.1:8000/>.

## Cómo probarlo desde cero

El repositorio no incluye `db.sqlite3` ni la carpeta `media/`; se generan solos al migrar y al subir imágenes.

1. Entrar a **Registrarse** y crear una cuenta (queda con sesión iniciada).
2. Usar **Nuevo post** para crear un post con o sin imagen.
3. Desde el detalle del post, usar **Editar** y **Eliminar**.
4. Cerrar sesión y verificar que `/posts/nuevo/` redirige al login.
5. Usar el buscador del inicio con una palabra inexistente para ver el aviso de sin resultados.

## Tests

```bash
python manage.py test
```

## Estructura

```
config/       Configuración del proyecto (settings, urls)
posts/        App de posts (modelo, vistas, formularios, migraciones)
accounts/     App de usuarios y perfiles
templates/    Plantillas HTML
static/       Archivos estáticos
media/        Imágenes subidas (se crea al usarlo, no se versiona)
```

## Autor

[@DamianLeandroF](https://github.com/DamianLeandroF)
