# User Authentication with Token and/or Cookie Support

This is an initial readme.
Check out PYPI: https://pypi.org/project/user-authentication-jr/

Add this to your settings:
 
  - add to `INSTALLED_APPS`
  ```
     INSTALLED_APPS = [
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
