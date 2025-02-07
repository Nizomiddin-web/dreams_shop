"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 5.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
from decouple import config
from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = config('SECRET_KEY',default="hjg^&%**%%^*GHVGJHGKJGKH")
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG',default=False,cast=bool)
ALLOWED_HOSTS = ['*'] #config('ALLOWED_HOSTS','').split(',')


# Application definition

INSTALLED_APPS = [
    "unfold",  # before django.contrib.admin
    "unfold.contrib.filters",  # optional, if special filters are needed
    "unfold.contrib.forms",  # optional, if special form elements are needed
    "unfold.contrib.inlines",  # optional, if special inlines are needed
    "unfold.contrib.import_export",  # optional, if django-import-export package is used
    "unfold.contrib.guardian",  # optional, if django-guardian package is used
    # "unfold.contrib.simple_history"
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'import_export',
    'django_extensions',
    'customer',
    'product',
    'order',
    'payment',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": config("DB_ENGINE",default="django.db.backends.sqlite3"),
        "NAME": config("DB_NAME",default=BASE_DIR / "db.sqlite3"),
        "USER":config("DB_USER",default=''),
        "PASSWORD":config("DB_PASSWORD",default=''),
        "HOST":config("DB_HOST",default=''),
        "PORT":config("DB_PORT",default='')
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tashkent'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "static"

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# UNFOLD_ADMIN_THEME = 'light'
UNFOLD = {
    "SITE_TITLE":"Dreams Shop",
    "SITE_HEADER": "Dreams Shop",
    # "SITE_ICON": {
    #     "light": lambda request: static("icon-light.svg"),  # light mode
    #     "dark": lambda request: static("icon-dark.svg"),  # dark mode
    # },
# "   SITE_LOGO": {
#         "light": lambda request: static("logo-light.svg"),  # light mode
#         "dark": lambda request: static("logo-dark.svg"),  # dark mode
#     },
    "SITE_SYMBOL": "speed",  # symbol from icon set
    "SITE_FAVICONS": [
        {
            "rel": "icon",
            "sizes": "32x32",
            "type": "image/svg+xml",
            "href": lambda request: static("favicon.svg"),
        },
    ],
    "SHOW_HISTORY": False,
    "COLORS": {
        "font": {
            "subtle-light": "107 114 128",
            "subtle-dark": "156 163 175",
            "default-light": "75 85 99",
            "default-dark": "209 213 219",
            "important-light": "17 24 39",
            "important-dark": "243 244 246",
        },
        "primary": {
            "50": "250 245 255",
            "100": "243 232 255",
            "200": "233 213 255",
            "300": "216 180 254",
            "400": "192 132 252",
            "500": "168 85 247",
            "600": "147 51 234",
            "700": "126 34 206",
            "800": "107 33 168",
            "900": "88 28 135",
            "950": "59 7 100",
        },
    },
    "SIDEBAR":{
        "show_search":False,
        "show_all_applications":True,
        "navigation":[
            {
                "title":"Customer",
                "collapsible":True,
                "items":[
                    {
                        "title":"Mijozlar",
                        "icon": "person",
                        "link":reverse_lazy("admin:customer_customer_changelist")
                    },
                    {
                        "title":"Manzillar",
                        "icon": "home",
                        "link":reverse_lazy("admin:customer_address_changelist")
                    }
                ]
            },
            {
                "title":"Buyurtma Bo'limi",
                "collapsible":True,
                "items":[
                    {
                        "title":"Buyurtmalar",
                        "icon": "shopping_cart",
                        "link":reverse_lazy("admin:order_order_changelist")
                    },
                    {
                        "title":"Buyurtma mahsulotlari",
                        "icon": "circle",
                        "link":reverse_lazy("admin:order_orderitem_changelist")
                    }
                ]
            },
            {
                "title":"Mahsulot Bo'limi",
                "collapsible":True,
                "items":[
                    {
                        "title":"Mahsulotlar",
                        "icon": "shopping_cart",
                        "link":reverse_lazy("admin:product_product_changelist")
                    },
                    {
                        "title":"Kategoriyalar",
                        "icon": "category",
                        "link":reverse_lazy("admin:product_category_changelist")
                    },
                    {
                        "title":"Ranglar",
                        "icon": "settings",
                        "link":reverse_lazy("admin:product_color_changelist")
                    },
                    {
                        "title":"O'lchamlar",
                        "icon": "grade",
                        "link":reverse_lazy("admin:product_size_changelist")
                    }
                ]
            },
            {
                "title":"To'lovlar Bo'limi",
                "collapsible":True,
                "items":[
                    {
                        "title":"To'lovlar",
                        "icon":"attach_money",
                        "link":reverse_lazy("admin:payment_payment_changelist")
                    },
                    {
                        "title":"To'lov statistikasi",
                        "icon":"grade",
                        "link":reverse_lazy("admin:payment_payment_stat")
                    }
                ]
            }
        ]
    },
    "DASHBOARD_CALLBACK": "customer.views.dashboard_callback",

}
