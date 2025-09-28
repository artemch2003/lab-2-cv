"""
Конфигурация зависимостей.
"""

from .container import DIContainer
from utils.validators import ParameterValidator


def configure_dependencies(container: DIContainer) -> None:
    """
    Настраивает зависимости в контейнере.
    
    Args:
        container: Контейнер зависимостей
    """
    # Импортируем классы здесь, чтобы избежать циклических импортов
    from image_processing.image_processor import ImageProcessor
    from image_processing.image_manager import ImageManager
    from image_processing.transform_manager import TransformManager
    from image_processing.interfaces.image_processor_interface import ImageProcessorInterface
    from image_processing.interfaces.image_loader_interface import ImageLoaderInterface
    from image_processing.interfaces.image_saver_interface import ImageSaverInterface
    from image_processing.interfaces.image_display_interface import ImageDisplayInterface
    from image_processing.interfaces.image_info_interface import ImageInfoInterface
    from image_processing.interfaces.transform_applier_interface import TransformApplierInterface
    
    # Регистрируем валидатор
    container.register_instance(ParameterValidator, ParameterValidator())
    
    # Регистрируем менеджеры
    container.register_singleton(ImageManager, ImageManager)
    container.register_singleton(TransformManager, TransformManager)
    
    # Регистрируем интерфейсы менеджеров
    container.register_factory(ImageLoaderInterface, lambda: container.get(ImageManager))
    container.register_factory(ImageSaverInterface, lambda: container.get(ImageManager))
    container.register_factory(ImageDisplayInterface, lambda: container.get(ImageManager))
    container.register_factory(ImageInfoInterface, lambda: container.get(ImageManager))
    container.register_factory(TransformApplierInterface, lambda: container.get(TransformManager))
    
    # Регистрируем процессор изображений
    container.register_singleton(ImageProcessorInterface, ImageProcessor)
    
    import logging
    logger = logging.getLogger(__name__)
    logger.info("Зависимости настроены")


def create_container() -> DIContainer:
    """
    Создает и настраивает контейнер зависимостей.
    
    Returns:
        DIContainer: Настроенный контейнер
    """
    container = DIContainer()
    configure_dependencies(container)
    return container
