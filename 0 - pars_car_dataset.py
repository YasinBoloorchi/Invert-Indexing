# importing required libraries.
from json import dump
import subprocess
from my_parser import xml_parser

# create a file path list for saving all founded paths.
all_path = []
file_count = 0

# for each year that we need in the main datase path
# it will do the follwing things.
for year in range(2007,2010):
    path = f'/home/hakim/Documents/semester 8/IR/HW_3/data/{year}' #2008 . 2009
    
    # with subprocess library we find all the files.
    files_names = subprocess.check_output('ls', cwd=path)
    files_names = files_names.decode('utf-8').split('\n')
    files_names.pop()
    
    # for each file in the year folders we add it
    # to the paths list.
    for fn in files_names:
        file_path = path+'/'+fn
        all_path.append(file_path)
        file_count += 1
        
# get the paresd dictionary from xml_parser.
md = xml_parser(all_path)

# create a parsed_data file to save the dictionary.
md_file = open('./parsed_data.json', 'w')

# convert dictionary to json file.
dump(md, md_file)
md_file.close()

# finally show the number of parsed files.
print('File count: ',file_count)



