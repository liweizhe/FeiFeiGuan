# with open('Data\\pig_info.csv', 'r') as fi, open('Data\\pig_info.csv', 'w') as fo:
#     for l in fi:
#         fo.writelines('{},否\n'.format(l.strip()))
import os

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


if __name__ == '__main__':
    # gbk2utf8('pig_file.csv', 'pig_file_utf8.csv')
    # gbk2utf8('pig_info.csv', 'pig_info_utf8.csv')
    # gbk2utf8('gem_info.jl', 'gem_info_utf8.jl')
    rename()
    # if '-' == '-':
    #     print('equal')
    print('-*-' * 10)
