# Installation

Create `.env` file from `.env.example`.

Build and run:
```
docker compose up --build
```

To run migrations
```
docker compose run --rm django-web python manage.py migrate
```

To get static
```
docker compose run --rm django-web python manage.py collecstatic
````

To create superuser

```
docker compose run --rm django-web python manage.py shell
```
```
from filetransfer.models import User, Organization
from django.contrib.auth import get_user_model
Organization(name="Company A").save()
org = Organization.objects.get()
User = get_user_model()
User.objects.create_superuser(username='Admin', email='admin@example.com', password='custom_pass', organization=org)
```

To test application

```
docker compose run --rm django-web python manage.py test
```
