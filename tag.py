from slugify import slugify

from logger import setup_logger

logger = setup_logger(__name__)

class Tag:
    def __init__(self, name):
        """
        Inicializa un objeto Tag.
        :param name: Título de la categoría.
        :param slug: Slug de la categoría.
        """
        self.name = name
        self.slug = self.generate_slug()


    def generate_slug(self):
        """
        Genera un slug basado en el nombre de la categoría.
        :return: Slug generado.
        """
        return slugify(self.name)


    def to_dict(self):
        """
        Convierte el objeto Tag en un diccionario para pasarlo al contexto de las plantillas.
        :return: Diccionario con los datos de la categoría.
        """
        return {
            'title': self.title,
            'slug': self.slug
        }
    

    def __repr__(self):
        return f"Tag(name='{self.name}')"
    

    def __eq__(self, other):
        return isinstance(other, Tag) and self.name == other.name

    def __hash__(self):
        return hash(self.name)
