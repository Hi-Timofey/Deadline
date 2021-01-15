# -*- coding: utf-8 -*-
import os


def get_data_path(name, subfolder):
    first_part = os.path.join('data', subfolder)
    fullname = os.path.join(first_part, name)

    if not os.path.isfile(fullname):
        raise ValueError(f"Файл с изображением '{fullname}' не найден")
    return fullname
