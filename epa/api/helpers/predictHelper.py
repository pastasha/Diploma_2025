import zipfile
import os



ZIP_EXTENSION = '.zip'
KERAS_MODELS = ['dnn', 'lstm', 'mlp']


def isKerasModel(modelID):
        if modelID in KERAS_MODELS:
            return True;
        else:
            return False;

def zipDirectory(folder_path):
    """
    Creates a ZIP archive with all files in the specified directory.
    :param folder_path: Path to the directory whose files you want to archive
    :param zip_name: Name of the output ZIP file (with the extension .zip)
    """
    try:
        with zipfile.ZipFile(folder_path + ZIP_EXTENSION, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, start=folder_path)
                    zipf.write(file_path, arcname)
        print(f"Archive {folder_path} is created.")
    except Exception as error:
                print("- zipDirectory error:")
                print(f"- {type(error).__name__}: {error}")