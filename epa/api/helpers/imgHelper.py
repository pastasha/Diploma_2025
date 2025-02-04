import os
import matplotlib.pyplot as plt
from werkzeug.utils import secure_filename



IMG_EXTENSION = ".png"
STATIC_FOLDER = "static/active_sessions/"


def generateImgFullPath(user_id, img_folder, img_name, modelID):
    img_path = ''
    if modelID :
        img_path = STATIC_FOLDER + user_id + img_folder + modelID
    else:
        img_path = STATIC_FOLDER + user_id + img_folder
    full_path = img_path + "/" + img_name
    return full_path

def saveImageToStaticFolder(user_id, root_folder, img_folder, img_name, modelID):
    img_path = ''
    if modelID :
        img_path = STATIC_FOLDER + user_id + img_folder + modelID
    else:
        img_path = STATIC_FOLDER + user_id + img_folder
    os.makedirs(os.path.join(root_folder, img_path), exist_ok=True)
    filename = secure_filename(img_name)
    plt.savefig(os.path.join(img_path, filename))
    return img_path + "/" + filename

def checkIfImgExists(root_folder, img_path):
    imgExists = False
    if (os.path.isfile(os.path.join(root_folder, img_path))):
        imgExists = True
    return imgExists