# with open('Data\\pig_info.csv', 'r') as fi, open('Data\\pig_info.csv', 'w') as fo:
#     for l in fi:
#         fo.writelines('{},否\n'.format(l.strip()))
import os
from PIL import Image
data_folder = './Data/'
tmp = './tmp/'


def gbk2utf8(infile, outfile, working_folder=data_folder, tmp_folder=tmp):
    os.chdir(working_folder)
    print(os.getcwd())
    with open(infile, 'r') as fi, open(outfile, 'w', encoding='UTF-8') as fo:
        for l in fi:
            fo.writelines(l)
    # os.rename(infile, '{}{}'.format(tmp_folder, infile))
    # os.rename(outfile, infile)
    os.chdir('../')


def rename(folder='./Data/Map'):
    os.chdir(folder)
    try:
        for l in os.listdir(os.getcwd()):
            os.rename(l, '{}.jpg'.format(l.split('-')[1]))
    except IndexError:
        print('already renamed')
    os.chdir('../../')


def mod_pic_size(width=275, height=163):
    pics_folder = './Data/Map/'
    # tmp_folder = './Data/tmp/'
    for pic_name in os.listdir(pics_folder):
        pic = Image.open('{}{}'.format(pics_folder, pic_name))
        try:
            new_img = pic.resize((width, height), Image.BILINEAR)
            new_img.save(os.path.join(pics_folder, os.path.basename(pic_name)))
        except Exception as e:
            print(e)


if __name__ == '__main__':
    # gbk2utf8('pig_file.csv', 'pig_file_utf8.csv')
    # gbk2utf8('pig_info.csv', 'pig_info_utf8.csv')
    # gbk2utf8('gem_info.jl', 'gem_info_utf8.jl')
    # rename()
    # if '-' == '-':
    #     print('equal')
    mod_pic_size()
    print('-*-' * 10)
