import os
import random

from flask import Blueprint, current_app
from flask import Blueprint, render_template, request

from classess.data_manager import DataManager
from .exceptions import OutOfFreeNamesError, PictureFormatNotSupportedError, PictureNotUploadedError

loader_blueprint = Blueprint('loader_blueprint', __name__, template_folder='templates')



def get_free_filename(folder, file_type):

    attemps = 0
    RANGE_OF_IMAGE_NUMBERS = 100
    LIMIT_OF_ATTEMPS = 10000

    while True:
        pic_name = str(random.randint(0, RANGE_OF_IMAGE_NUMBERS))
        filename_to_save = f"{pic_name}.{file_type}"
        os_path = os.path.join(folder, filename_to_save)
        is_filename_occupied = os.path.exists(os_path)

        if not is_filename_occupied:
            return filename_to_save

        attemps += 1

        if attemps > LIMIT_OF_ATTEMPS:
            raise OutOfFreeNamesError("No free names to save Image")


def is_file_type_valid(file_type):

    if file_type.lower() in ["jpg", "jpeg", "gif", "png", "webp", "tiff"]:
        return True
    return False

@loader_blueprint.route('/post', methods=['GET'])
def page_form():
    return render_template('post_form.html')


@loader_blueprint.route('/post', methods=['POST'])
def page_create_posts():
    picture = request.files.get('picture', None)
    content = request.values.get('content', '')

    #работаем с картинкой

    filename = picture.filename
    file_type = filename.split('.')[-1]

    #проверяем валидность файла

    if not is_file_type_valid(file_type):
        raise PictureFormatNotSupportedError(f"Формат {file_type} не поддерживается")

    # получаем свободное имя
    folder = os.path.join(".", "uploads", "images")
    filename_to_save = get_free_filename(folder, file_type)

    #сохраняем под новым именем
    try:
        picture.save(os.path.join(folder, filename_to_save))
    except FileNotFoundError:
        raise PictureNotUploadedError(f"{folder, filename_to_save}")

    # формируем путь для браузера
    web_path = f"/uploads/images/{filename_to_save}"

    #Сохраняем данные

    post = {"pic": web_path, "content": content}

    path = current_app.config.get("POST_PATH")
    data_manager = DataManager(path)
    data_manager.add(post)

    return render_template('post_uploaded.html', pic=web_path, content=content)

@loader_blueprint.errorhandler(OutOfFreeNamesError)
def error_out_of_free_name(e):
    return "Закончились свободные имена для загрузки картинок"

@loader_blueprint.errorhandler(PictureFormatNotSupportedError)
def error_format_not_supported(e):
    return "Формат картинки не поддерживается"

@loader_blueprint.errorhandler(PictureNotUploadedError)
def error_format_not_supported(e):
    return "Не удалось загрузить картинку"
