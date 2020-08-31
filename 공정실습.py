#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import xlrd

def rename_file():
    # 현재 위치(.)의 파일을 모두 가져온다. 
    fileDir = os.path.dirname(os.path.realpath(__file__))
    os.chdir(fileDir)

    for filename in os.listdir("."):
        if filename.endswith("xls"):
            wb = xlrd.open_workbook(filename)
            break

    sheet = wb.sheet_by_index(0)

    for filename in os.listdir("."):

        # 파일 확장자가 (txt)인 것만 처리 
        if filename.endswith("pdf"):
            fn = filename.split('_')
            if len(fn) < 2:
                continue
            fn2 = fn[-1].split('.')
            new_filename = '{0}_{1}.pdf'.format(sheet.cell_value(int(fn2[0]), 1), fn[0])
            os.rename(filename, new_filename)
           


if __name__ == "__main__":

    rename_file()