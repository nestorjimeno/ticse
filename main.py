import locale
import os
import shutil
import sys

from time import sleep

from config import configuration, STATIC_DIR
from logger import setup_logger
from template_manager import TemplateManager

def clean_output_dir(folder):
    """Elimina el contenido de la carpeta de salida."""
    if os.path.exists(folder):
        shutil.rmtree(folder)
        logger.debug(f"Carpeta de salida '{folder}' limpiada.")
    sleep(0.5)
    os.makedirs(folder, exist_ok=True)

def copy_static_files(src_folder, dest_folder):
    """Copia los archivos estáticos a la carpeta de salida."""
    if not os.path.exists(src_folder):
        logger.error(f"La carpeta de estáticos de origen '{src_folder}' no existe.")
        sys.exit(1)
        return
    
    # Crear la carpeta de destino si no existe
    os.makedirs(dest_folder, exist_ok=True)
    
    # Copiar archivos y carpetas recursivamente
    for item in os.listdir(src_folder):
        src_path = os.path.join(src_folder, item)
        dest_path = os.path.join(dest_folder, item)
        
        if os.path.isdir(src_path):
            shutil.copytree(src_path, dest_path, dirs_exist_ok=True)
        else:
            shutil.copy2(src_path, dest_path)
    
    logger.debug(f"Archivos estáticos copiados de a '{dest_folder}'.")

def main(debug=True, update_only_blog=False):
    configuration['debug'] = debug

    # If debug=False, the output_dir is output/web/ 
    if not debug:
        output_dir = os.path.join(configuration['paths']['output_dir'], 'web')
    # If debug=True, the output_dir is output/
    else:
        output_dir = configuration['paths']['output_dir']

    statics_dir = configuration['paths']['statics_dir']

    manager = TemplateManager(config=configuration)
    
    clean_output_dir(output_dir)
    copy_static_files(statics_dir, os.path.join(output_dir, STATIC_DIR))
    shutil.copy2(os.path.join(configuration['paths']['base_dir'], 'robots.txt'), os.path.join(output_dir, 'robots.txt'))
    
    if not update_only_blog:
        # Generate or update general pages.
        for page in configuration['urls'].values():
            manager.generate_page(page)
    
    tags = set()

    # Generate or update blog posts.
    for post in manager.posts.values():
        manager.generate_page(template_name='blog/post.html', post=post)
        for tag in post.tags:
            tags.add(tag)

    for tag in tags:
        manager.generate_page(template_name='categorias.html', tag=tag)

    # Generate .js file.
    manager.generate_page(template_name='static/js/script.js')
    
    
if __name__ == '__main__':

    logger = setup_logger(__name__)
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

    main(debug=False)