# -*- coding: utf-8 -*-
import os


def get_data_path(name, subfolder):
    first_part = os.path.join('data', subfolder)
    fullname = os.path.join(first_part, name)

    if not os.path.isfile(fullname):
        raise ValueError(f"Source file '{name}' not found ({fullname})")
    return fullname

def get_font_path(name):
    fullname = os.path.join(os.path.join('data', 'font'), name)

    if not os.path.isfile(fullname):
        raise ValueError(f"File with font '{name}' not found ({fullname})")
    return fullname

def get_img_path(name):
    fullname = os.path.join(os.path.join('data', 'img'), name)

    if not os.path.isfile(fullname):
        raise ValueError(f"File with imgae '{name}' not found ({fullname})")
    return fullname
