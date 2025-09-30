import os
import re

from datetime import datetime
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
from logger import setup_logger
from operator import attrgetter

from config import TEMPLATES_DIR
from post import Post


# Crear un logger para este archivo específico
logger = setup_logger(__name__)

class TemplateManager():
    def __init__(self, config):
        """.
        """
        self.config = config
        self.env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
        self.env.globals['static_url'] = self.static_url
        self.env.globals['url'] = self.url
        self.env.globals['remove_filename_from_url'] = self.remove_filename_from_url
        self.env.globals['get_page_blog'] = self.get_page_blog
        self.env.globals['get_page_categorias'] = self.get_page_categorias
        self.posts = self.create_posts_from_markdown()
        self.config['posts'] = self.posts
    
    def generate_page(self, template_name, **context):
        """Genera las páginas HTML a partir de las plantillas."""
        try:
            template_name = template_name.replace('\\', '/')
            template = self.env.get_template(template_name)
            
            if not self.config['debug']:
                output_dir = os.path.join(self.config['paths']['output_dir'], 'web')
            else:
                output_dir = self.config['paths']['output_dir']
            
            # Para los post, la url será su título, no el nombre de la plantilla.
            if context.get('post'):
                output_dir = os.path.join(output_dir, 'blog', context.get('post').slug + '.html')
            elif context.get('tag'):
                output_dir = os.path.join(output_dir, 'categorias', context.get('tag').slug + '.html')
            else:    
                output_dir = os.path.join(output_dir, template_name)
            
            os.makedirs(os.path.dirname(output_dir), exist_ok=True)

            if template_name == 'blog/index.html':
                posts_per_page = self.config['settings']['posts_per_page']
                pages = (len(self.posts) + posts_per_page - 1) // posts_per_page
                posts = sorted(self.posts.values(), key=attrgetter('date'), reverse=True)
                for page in range(1, pages + 1):
                    if page == 1:
                        output_dir = os.path.join(os.path.dirname(output_dir), "index.html" )
                    else:
                        output_dir = os.path.join(os.path.dirname(output_dir), f"page-{page}.html" )
                    with open(output_dir, 'w', encoding='utf-8') as f:
                        t = template.render(
                            **context, 
                            **self.config['urls'], 
                            **self.config['static_urls'], 
                            template_name=template_name, 
                            posts=posts[ (page - 1) * posts_per_page : (page - 1) * posts_per_page + posts_per_page ],
                            page=page,
                            posts_per_page = posts_per_page,
                            total_pages=pages,
                        )
                        f.write(t)
                    logger.debug(f"Página generada: {output_dir}")
            elif template_name == 'categorias/index.html':
                categories_per_page = self.config['settings']['categories_per_page']
                pages = (len(self.posts) + categories_per_page - 1) // categories_per_page
                posts = sorted(self.posts.values(), key=attrgetter('date'), reverse=True)
                for page in range(1, pages + 1):
                    if page == 1:
                        output_dir = os.path.join(os.path.dirname(output_dir), "index.html" )
                    else:
                        output_dir = os.path.join(os.path.dirname(output_dir), f"page-{page}.html" )
                    with open(output_dir, 'w', encoding='utf-8') as f:
                        t = template.render(
                            **context, 
                            **self.config['urls'], 
                            **self.config['static_urls'], 
                            template_name=template_name, 
                            posts=posts[ (page - 1) * categories_per_page : (page - 1) * categories_per_page + categories_per_page ],
                            page=page,
                            categories_per_page = categories_per_page,
                            total_pages=pages,
                        )
                        f.write(t)
                    logger.debug(f"Página generada: {output_dir}")

            else:    
                with open(output_dir, 'w', encoding='utf-8') as f:
                    t = template.render(**context, **self.config['urls'], **self.config['static_urls'], template_name=template_name, posts=self.posts)
                    f.write(t)
                logger.debug(f"Página generada: {output_dir}")

        except TemplateNotFound:
            logger.error(f'No se ha encontrado la plantilla {template_name}.')
            

    def create_posts_from_markdown(self):
        """
        Lee todos los archivos Markdown en la carpeta content_dir y crea objetos Post.
        Pasa los .md a la carpeta de archivos ya creados.
        
        :return: Lista de objetos Post.
        """
        posts = {}
        
        try:
            # os.makedirs(
            #     self.config['paths']['content_dir_old'],
            #     exist_ok=True)
            for filename in os.listdir(self.config['paths']['content_dir']):
                if filename.endswith('.md'):
                    filepath = os.path.join(self.config['paths']['content_dir'], filename)
                    with open(filepath, 'r', encoding='utf-8') as file:
                        lines = file.readlines()

                    # Primera línea como título
                    title = lines[0].strip("# ").strip() if lines else "Sin título"
                    
                    # Obtener metadatos de los comentarios
                    author = None
                    date = None
                    tags = []
                    language = None
                    
                    for line in lines:
                        if line.startswith("<!--"):
                            clean_line = line[4:-4].strip()
                            match_author = re.search(r'author:\s*(.+)', clean_line)
                            match_date = re.search(r'date:\s*(.+)', clean_line)
                            match_tags = re.search(r'tags:\s*(.+)', clean_line)
                            match_language = re.search(r'language:\s*(.+)', clean_line)

                            if match_author:
                                author = match_author.group(1).strip()
                            if match_date:
                                date = match_date.group(1).strip()
                                try:
                                    date = datetime.strptime(date, "%Y-%m-%d").date()
                                except ValueError as e:
                                    logger.error(f"Error al convertir la fecha del post {title}: {e}")
                            if match_tags:
                                tags = [tag.strip() for tag in match_tags.group(1).split(",")]
                            if match_language:
                                language = match_language.group(1).strip()

                    # Contenido del artículo
                    content = "".join(lines[1:])

                    # Crear objeto Post
                    post = Post(title=title, content=content, author=author, date=date, tags=tags, language=language)
                    posts[post.slug] = post
                    # os.rename(
                    #     os.path.join(self.config['paths']['content_dir'], filename),
                    #     os.path.join(self.config['paths']['content_dir_old'], filename)
                    # )
        except FileNotFoundError:
            logger.error(f"No se han encontrado posts en {self.config['paths']['content_dir']}.")
            quit()
            
        except Exception as e:
            logger.error(f'Error inesperado en create_posts_from_markdown(): {type(e).__name__} - {e}')
        
        return posts
    

    def static_url(self, template_name, filename=""):
        """
        Generates a relative static URL based on the template name and filename.

        Args:
            template_name (str): The name of the template used to determine the directory depth.
            filename (str): The name of the file for which the URL is generated. Defaults to an empty string.

        Returns:
            str: The generated relative URL for the static file.
        """
        if "/" in template_name:
            number = len(template_name.split("/")) - 1
            url = f"{'../'*number + filename}".replace("\\", "/")
            return url
        if template_name == "categorias.html":
            url = f"{'../../' + filename}".replace("\\", "/")
            return url
        return filename
    

    def url(self, filename):
        if not self.config['debug']:
            return f'/{filename}'
        return os.path.join(self.config['paths']['output_dir'], filename)
    

    def remove_filename_from_url(self, url):
        if not self.config['debug']:
            directory = os.path.dirname(url).replace(os.sep, '/')
            return re.sub(r'/{2,}', '/', directory)
        return os.path.dirname(url) 
    
    
    def get_page_blog(self, page):
        if not self.config['debug']:
            if page == 1:
                return '/blog/index.html'
            else:
                return f'/blog/page-{page}.html'
        if page == 1:
            return os.path.join(self.config['paths']['output_dir'], 'blog', 'index.html')
        else:
            return os.path.join(self.config['paths']['output_dir'], 'blog', f'page-{page}.html')
        
    def get_page_categorias(self, page):
        if not self.config['debug']:
            if page == 1:
                return '/categorias/index.html'
            else:
                return f'/categorias/page-{page}.html'
        if page == 1:
            return os.path.join(self.config['paths']['output_dir'], 'categorias', 'index.html')
        else:
            return os.path.join(self.config['paths']['output_dir'], 'categorias', f'page-{page}.html')