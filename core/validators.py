from django.core.exceptions import ValidationError
from django.conf import settings
from PIL import Image
import os


def validate_file_extension(value):
    """Valide l'extension du fichier uploadé"""
    ext = os.path.splitext(value.name)[1][1:].lower()
    allowed_extensions = settings.ALLOWED_EXTENSIONS
    
    if ext not in allowed_extensions:
        raise ValidationError(
            f'Extension de fichier non autorisée. '
            f'Extensions acceptées : {", ".join(allowed_extensions)}'
        )


def validate_file_size(value):
    """Valide la taille du fichier uploadé"""
    filesize = value.size
    max_size = settings.MAX_UPLOAD_SIZE
    
    if filesize > max_size:
        max_size_mb = max_size / (1024 * 1024)
        raise ValidationError(
            f'La taille du fichier ne doit pas dépasser {max_size_mb:.1f} MB'
        )


def validate_image(value):
    """Valide qu'un fichier est bien une image"""
    try:
        img = Image.open(value)
        img.verify()
    except Exception:
        raise ValidationError('Le fichier n\'est pas une image valide')


def compress_image(image_path, quality=85):
    """Compresse une image pour réduire sa taille"""
    try:
        img = Image.open(image_path)
        
        # Convertir en RGB si nécessaire
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')
        
        # Redimensionner si trop grande (max 1920px de largeur)
        max_width = 1920
        if img.width > max_width:
            ratio = max_width / img.width
            new_size = (max_width, int(img.height * ratio))
            img = img.resize(new_size, Image.Resampling.LANCZOS)
        
        # Sauvegarder avec compression
        img.save(image_path, 'JPEG', quality=quality, optimize=True)
        
        return True
    except Exception as e:
        print(f"Erreur lors de la compression: {e}")
        return False


def get_file_info(file):
    """Retourne les informations sur un fichier"""
    return {
        'name': file.name,
        'size': file.size,
        'size_mb': round(file.size / (1024 * 1024), 2),
        'extension': os.path.splitext(file.name)[1][1:].lower(),
    }
