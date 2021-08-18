# main parser code

# importing required libraries
import subprocess
import re

def xml_parser(paths):
    """
    xml_parser is a function that get paths of files in
    an array and return all the parsed files in a dictionary
    
    Ex: 
    paths = ['/home/user/filename1.xml', '/home/user/filename1.xml']
    result_dictionary = xml_parser(paths)
    """
    # creating a dictionary for saving all documents tags values
    main_dictionary = {}    

    # document id starts from 1
    DocID = 1
    error_counter = 0

    # for each file in the given paths to the parser
    # it will do the following steps.
    for P in paths:
        path = P

        # open file with windows unicode
        file = open(path, 'r', encoding='windows-1252')#, errors='ignore')

        # get file name from gived path
        doc_name = re.findall('.*/(.*$)', path)
        
        print('parsing file: ', doc_name[0])
        
        # in_doc_flag help us to notify if we are 
        # inside a <Doc> tag.
        in_doc_flag = False

        for l in file.readlines():
            
            # crating a key and value for the comment that
            # we are in.
            if l == '<DOC>\n':
                in_doc_flag = True
                main_dictionary[DocID] = {}
                main_dictionary[DocID]['file_name'] = doc_name[0]
                continue

            # increase Documnet id by 1 for the next comment
            elif l == '</DOC>\n' or l == '</DOC>':
                in_doc_flag = False
                DocID += 1
                continue
            
            # we use try except for loss of informatin in tags
            try:
                # get tag name and it's value in each comment
                if in_doc_flag:
                    tag = re.findall('\<(\w*)\>', l)[0]
                    tag_string = re.findall('\>(.*)\<', l)[0]
                    main_dictionary[DocID][tag] = tag_string
                    # print(tag,': ', tag_string)
            except:
                print('error')
                error_counter += 1
        
    print('error_counter: ', error_counter)
    # finally it return a dictionary for all of the given file
    return main_dictionary

