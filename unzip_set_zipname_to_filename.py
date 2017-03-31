import argparse
import os
import re
import zipfile
from datetime import datetime

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--dir_input', action='store', required=True, help='Diretorio com os arquivos zipados')
parser.add_argument('-o', '--dir_output', action='store', help='Diretorio pra salvar os arquivos extraidos')
args = parser.parse_args()

dir_input = args.dir_input

if args.dir_output:
    dir_output = args.dir_output
else:
    dir_output = os.path.join(dir_input, 'output')

files = [f for f in os.listdir(dir_input) if f.endswith('.zip')]

len_files = len(files)

print(f'Extraindo {len_files} arquivos da pasta: {dir_input}')

for n, file in enumerate(files, start=1):

    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + f' {file}: {n} de {len_files}')

    with zipfile.ZipFile(os.path.join(dir_input, file), "r") as z:
        if len(z.namelist()) == 1:
            member = z.namelist()[0]
            member = z.getinfo(member)
            member.filename = re.sub('.*\.', file[:-3], member.filename)
            z._extract_member(member, dir_output, None)

        elif len(z.namelist()) >= 2:
            members = z.namelist()
            for i, member in enumerate(members, start=1):
                member = z.getinfo(member)
                member.filename = re.sub('.*\.', file[:-4] + '_%s.' % str(i).zfill(4), member.filename)
                z._extract_member(member, os.path.join(dir_output, file[:-4]), None)
        else:
            print(f'{file} está vazio')

print(f'Foram salvos os arquivos extraidos na pasta: {dir_output}')
