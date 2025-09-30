import os

DEBUG = False
UPDATE_ONLY_BLOG = False

LOCAL_ROOT = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = 'output'
STATIC_DIR = 'static'
CONTENT_DIR = 'content'
CONTENT_DIR_OLD = 'content_old'
TEMPLATES_DIR = 'templates'

configuration = {
    "debug": DEBUG,
    "paths": {
        "base_dir": LOCAL_ROOT,
        "output_dir": os.path.join(LOCAL_ROOT, OUTPUT_DIR),
        "statics_dir": os.path.join(LOCAL_ROOT, STATIC_DIR),
        "content_dir": os.path.join(LOCAL_ROOT, CONTENT_DIR),
    },
    "run": {
        "update_only_blog": UPDATE_ONLY_BLOG,
    },
    "urls": {
        "home": "index.html",
        "blog_home": os.path.join("blog", "index.html"),
        "categorias_home": os.path.join("categorias", "index.html"),
        "contacto": "contacto.html",
        "newsletter": "newsletter.html",
        "registrado": "registrado.html",
        "sobre_mi": "sobre-mi.html",
        "error": "404.html",
        "aviso_legal": "aviso-legal.html",
        "politica_de_cookies": "politica-de-cookies.html",
        "politica_de_privacidad": "politica-de-privacidad.html",
    },
    "static_urls": {
        "static_css": os.path.join("static", "css", "styles.css"),
        "static_js": os.path.join("static", "js", "script.js"),
    },
    "settings":{
        "posts_per_page": 3,
        "categories_per_page": 4,
    },
}
