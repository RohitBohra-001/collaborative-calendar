SQLALCHEMY_DATABASE_URI = "postgresql://mymac@localhost:5433/calendar_db"
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = "dev-secret-key"
JWT_SECRET_KEY = "jwt-secret-key"
JWT_TOKEN_LOCATION = ["cookies"]
JWT_COOKIE_HTTPONLY = True
JWT_COOKIE_SECURE = False   # True only in HTTPS (prod)
JWT_ACCESS_COOKIE_PATH = "/"
JWT_CSRF_IN_COOKIES = False
JWT_COOKIE_CSRF_PROTECT = False
