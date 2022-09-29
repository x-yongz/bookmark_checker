#!python3

import argparse
import os.path
import requests
from bs4 import BeautifulSoup

def main():
    parser = argparse.ArgumentParser(description='Check for bad URLs in your bookmarks')
    parser.add_argument('-f', '--file', type=str, help='Name of the bookmarks file, including .html')
    args = parser.parse_args()
    
    if os.path.exists(args.file):
        bad_url = []
        
        with open(args.file, 'r', encoding='utf-8') as f:
            file = BeautifulSoup(f, features='html.parser')
    
        for link in file.find_all('a'):
            if link.text == '':
                name = link['href']
            else:
                name = link.text
                
            try: 
                http_code = requests.get(link['href'], timeout=10).status_code
            except Exception:
                http_code = 0
                
            if http_code == 0: 
                out_0 = name + ' | MANUAL CHECK REQUIRED'
                bad_url.append(out_0)
                print(out_0)
            elif http_code != 200:
                out_1 = name + ' | ' + str(http_code) + ' ERROR'
                bad_url.append(out_1)
                print(out_1)
            else:
                print(name + ' | OK')
        
        with open('bad_url.txt', 'w', encoding='utf-8') as w:
            for each in bad_url:
                w.write(each + '\n')
    
        print('**************************************************************')
        print('It is done, please find "bad_url.txt" for the list of bad URLs')
        print('**************************************************************')
    else:
        print('Bookmark file does not exist!')

if __name__ == '__main__':
    main()