import os

from page_loader.logger import get_logger


CREATED_LOADED_RESOURCES_FOLDER = 'Loaded resources folder was created'
CREATING_DIR_PERMISSION_ERROR = (
    "You don't have permission to create dir here: '{}'"
)
NO_SUCH_DIR_ERROR = "No such directory: '{}'"
OS_ERROR = "Some system error occured, path '{}'"
WRITING_PERMISSION_ERROR = "You don't have permission to write file here: '{}'"
WRITTEN_LOADED_PAGE = "Loaded page soup was written to '{}'"


logger = get_logger(__name__)


def create_loaded_local_resources_dir(
    output_path, loaded_local_resources_dir_name
):
    loaded_resources_dir_full_path = os.path.join(
        output_path,
        loaded_local_resources_dir_name
    )

    if not os.path.exists(loaded_resources_dir_full_path):
        try:
            os.mkdir(loaded_resources_dir_full_path)
        except PermissionError:
            raise PermissionError(
                CREATING_DIR_PERMISSION_ERROR.format(output_path)
            )
        except FileNotFoundError:
            raise FileNotFoundError(NO_SUCH_DIR_ERROR.format(output_path))
        except OSError:
            raise OS_ERROR(OS_ERROR.format(output_path))

    logger.info(CREATED_LOADED_RESOURCES_FOLDER)


def write_loaded_local_resource(response, output_path):
    response_chunks = response.iter_content()

    try:
        with open(output_path, 'wb') as loaded_file:
            for response_chunk in response_chunks:
                loaded_file.write(response_chunk)
    except PermissionError:
        raise PermissionError(WRITING_PERMISSION_ERROR.format(output_path))
    except OSError:
        raise OSError(OS_ERROR.format(output_path))


def write_loaded_main_page(loaded_page_full_path, soup):
    try:
        with open(loaded_page_full_path, 'w') as loaded_page:
            loaded_page.write(soup)
    except PermissionError:
        raise PermissionError(
            WRITING_PERMISSION_ERROR.format(loaded_page_full_path)
        )
    except OSError:
        raise OSError(OS_ERROR.format(loaded_page_full_path))
    else:
        logger.info(WRITTEN_LOADED_PAGE.format(loaded_page_full_path))
