import os


def del_img(name, PATH):
    for dirs, folder, files in os.walk(PATH):
        for file in files:
            if name in os.path.join(dirs,file):
                print(os.path.join(dirs,file).replace('\\','/'))
                os.remove(os.path.join(dirs,file).replace('\\','/'))
