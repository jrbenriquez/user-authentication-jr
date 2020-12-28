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
    AUTH_USER_MODEL = 'authentication.USER'
  ```
  
  - add authentication class
   ```
   from authentication.utils.token import ExpiringTokenAuthentication
   
   DEFAULT_AUTHENTICATION_CLASSES = [...., 'ExpiringTokenAuthentication']
   REST_FRAMEWORK_TOKEN_SECONDS_EXPIRY = 3600
   ```
