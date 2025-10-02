from bs4 import BeautifulSoup
from datetime import datetime
from markdown import Markdown
from markdown.extensions import Extension
from markdown.extensions.toc import TocExtension
from markdown.treeprocessors import Treeprocessor
import re
import unicodedata
from slugify import slugify
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from tag import Tag

class ExternalLinksTreeprocessor(Treeprocessor):
    def run(self, root):
        for el in root.iter("a"):
            href = el.get("href", "")
            # Solo para links externos
            if href.startswith("http://") or href.startswith("https://"):
                el.set("target", "_blank")
                el.set("rel", "noreferrer")


class ExternalLinksExtension(Extension):
    def extendMarkdown(self, md):
        md.treeprocessors.register(ExternalLinksTreeprocessor(md), "extlinks", 15)


def myslugify(value, sep):
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", sep, value.lower()).strip(sep)


class Post:
    def __init__(self, title, content, author, date=None, tags=None, language=None):
        """
        Inicializa un objeto Post.
        :param title: Título del post.
        :param content: Contenido del post (puede ser HTML o Markdown).
        :param author: Autor del post.
        :param date: Fecha del post (opcional, por defecto será la fecha actual).
        :param tags: Lista de etiquetas asociadas al post (opcional).
        """
        self.title = title
        self.content = content
        self.content_html, self.toc = self.markdown_with_syntax_highlight(self.content)
        self.author = author
        self.date = date or datetime.now().strftime('%Y-%m-%d')
        self.language = language
        self.summary = self.generate_summary(self.content_html)
        self.slug = self.generate_slug()

        if tags is None:
            self.tags = []
        elif isinstance(tags, str):
            self.tags = [Tag(tags)]
        elif isinstance(tags, list) and all(isinstance(t, str) for t in tags):
            self.tags = [Tag(t) for t in tags]
        else:
            raise TypeError("tags debe ser un string o una lista de strings")

    def generate_slug(self):
        """
        Genera un slug basado en el título del post.
        :return: Slug generado.
        """
        return slugify(self.title)
    
    def generate_summary(self, content_html):
        """
        Genera un resumen del post.
        :return: Resumen generado.
        """
        soup = BeautifulSoup(content_html, 'html.parser')
        text = soup.get_text()
        max_length = 200
        
        # Tomar el primer párrafo o limitar a max_length caracteres
        summary = text.strip().split('\n')
        for paragraph in summary:
            if len(paragraph) > 20:
                summary = paragraph
                break
        if len(summary) > max_length:
            summary = summary[:max_length].rsplit(' ', 1)[0] + '...'  # Truncar y añadir '...'
        
        return summary

    def to_dict(self):
        """
        Convierte el objeto Post en un diccionario para pasarlo al contexto de las plantillas.
        :return: Diccionario con los datos del post.
        """
        return {
            'title': self.title,
            'content': self.content,
            'author': self.author,
            'date': self.date,
            'tags': self.tags,
            'language': self.language,
            'slug': self.slug
        }

    def __repr__(self):
        return f"Post(title='{self.title}', author='{self.author}', date='{self.date}', tags='{self.tags}')"

    def markdown_with_syntax_highlight(self, markdown_text, theme="one-dark"):

        md = Markdown(extensions=['fenced_code', TocExtension(slugify=myslugify, permalink=True, title="Índice"), ExternalLinksExtension()])

        # Convertir Markdown a HTML con fenced_code habilitado
        html_output = md.convert(markdown_text)

        # Aplicar resaltado de sintaxis con Pygments
        soup = BeautifulSoup(html_output, 'html.parser')
        
        for code_tag in soup.find_all('code'):
            language_class = code_tag.get('class', [None])[0]  # Obtener la clase del lenguaje (e.g., "language-python")
            if language_class:
                language = language_class.replace('language-', '')  # Limpiar el nombre del lenguaje
                lexer = get_lexer_by_name(language, stripall=True)
                formatter = HtmlFormatter(style=theme)  # Estilo de Pygments
                new_code = highlight(code_tag.decode_contents(), lexer, formatter)
                code_tag.replace_with(BeautifulSoup(new_code, 'html.parser'))
        
        # Generar CSS para el resaltado de sintaxis
        css_styles = HtmlFormatter(style=theme).get_style_defs('.highlight')

        # Agregar estilos personalizados para div.highlight
        custom_css = """
            div.highlight {
                padding: 20px;
                border-radius: 10px;
                margin: 20px 0 0 0;
            }
            pre {
                word-wrap: break-word;       /* Divide palabras largas si es necesario */
                overflow-x: auto;            /* Añade desplazamiento horizontal si el contenido es demasiado ancho */
                max-width: 100%;             /* Limita el ancho del bloque al contenedor */
                border-radius: 5px;          /* Bordes redondeados */
            }
            code {
                color: #eb5757;
                border-width: 0px;
                padding: 2px 5px;
                font-size: .9em;
                font-weight: 600;
                margin-left: .125rem;
                margin-right: .125rem;
                border-radius: .375rem;
                --tw-bg-opacity: 1;
                background-color: rgb(236 236 236 / var(--tw-bg-opacity, 1));
            }
            """
        
        # Combinar los estilos generados por Pygments con los estilos personalizados
        full_css = f"<style>{css_styles}\n{custom_css}</style>"

        #Corregir caracteres reemplazados sin necesidad:
        soup = str(soup).replace('&amp;gt;', '>')
        
        # Devolver CSS y HTML final
        return f"{full_css}\n{soup}", md.toc