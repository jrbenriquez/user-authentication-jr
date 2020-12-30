# User Authentication with Token and/or Cookie Support

'authentication.models.User' has the following basic fields

`username, email, first_name, last_name, is_staff, is_active, date_joined, last_login`


Add this to your settings:
 
   - make sure admin app gets rollbacked to zero first
   ```
    python manage.py migrate admin zero
   ```

  - add to `INSTALLED_APPS` after admin, auth and contenttypes
  ```
     INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
     ...,
     'authentication',
     ]
  ```

  - to use the User model
  
  ```
    AUTH_USER_MODEL = 'authentication.User'
  ```
  
  - add authentication class
   ```
   
   DEFAULT_AUTHENTICATION_CLASSES = [...., 'authentication.utils.token.ExpiringTokenAuthentication']
   REST_FRAMEWORK_TOKEN_SECONDS_EXPIRY = 3600
   ```
   - add url entry for module to your urls.py
   ```
    path('auth/', include('authentication.urls')),
   ```

   - do migrations
   ```
    python manage.py migrate
   ```
