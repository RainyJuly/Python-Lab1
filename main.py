import requests
import re
import os
import zipfile
import hashlib

directory_to_extract_to =r'C:\Users\tsvet\OneDrive\Документы\test'
arch_file = r'C:\Users\tsvet\Downloads\tiff-4.2.0_lab1.zip' #префикс r для того, чтобы адрес читался и некоторые сочетания символов не вызывали особые функции через \
test_zip = zipfile.ZipFile(arch_file)
test_zip.extractall(directory_to_extract_to)
test_zip.close()

txt_files=[]
for root,dir,files in os.walk (directory_to_extract_to):
    for f in files:
        if f.endswith('.txt'):
            txt_files.append(os.path.join(root, f))
print(txt_files)
for f in txt_files:
    target_file=f
    target_file_data=open(target_file, 'rb').read()
    result=hashlib.md5(target_file_data).hexdigest()
    print(result)

target_hash="4636f9ae9fef12ebd56cd39586d33cfb"
for root, dirs, files in os.walk(directory_to_extract_to):
    for file in files:
        file_path = os.path.join(root, file)
        if hashlib.md5(open(file_path, 'rb').read()).hexdigest() == target_hash:
            target_file = os.path.join(root, file)
            target_file_data = open(target_file, 'r').read()
            break
print(target_file)
print(target_file_data)

r = requests.get(target_file_data)
result_dct = {}
counter = 0
lines = re.findall(r'<div class="Table-module_row__3TH83">.*?</div>.*?</div>.*?</div>.*?</div>.*?</div>', r.text)
for line in lines:
    if counter == 0:
        headers = re.sub(r'(\<(/?[^>]+)>)', ';', line)
        headers = re.findall(r'[А-ЯЁа-яё]+\s?', headers)
        headers[3] = headers[3]+headers[4]
        headers.pop(4)
        counter += 1
        continue
    temp = re.sub(r'(\<(/?[^>]+)>)', ';', line)
    temp = re.sub(r'\([^)]*\)', '', temp)
    temp = temp[4:].strip()
    temp = re.sub(r'\;+', ';', temp)
    temp = re.sub(r'^;', '', temp)
    temp = re.sub(r';$', '', temp)
    temp = re.sub(r'\s+(?=(?:[,.?!:;…]))', '', temp)
    temp = re.sub(r'\*', '', temp)
    temp = re.sub(r'_', '-1', temp)
    temp = re.sub(r'\xa0', '', temp)
    tmp_split = re.split(r';', temp)
    country_name = tmp_split[0]
    col1_val = tmp_split[1]
    col2_val = tmp_split[2]
    col3_val = tmp_split[3]
    col4_val = tmp_split[4]
    result_dct[country_name] = {}
    result_dct[country_name][headers[0]] = col1_val
    result_dct[country_name][headers[1]] = col2_val
    result_dct[country_name][headers[2]] = col3_val
    result_dct[country_name][headers[3]] = col4_val
    counter += 1

output = open('data.csv', 'w')
counter = 0
for key in result_dct.keys():
    if counter == 0:
        output.write('Страна' + ';' + ';'.join(headers) + '\n')
        counter += 1
    output.write(key + ';')
    for i in range(0, 4):
        output.write(result_dct[key][headers[i]] + ';')
    output.write('\n')
output.close()

try:
    target_country = input("Введите название страны: ")
    print(result_dct[target_country])
except KeyError:
    print("Введенная вами страна не найдена:(")



