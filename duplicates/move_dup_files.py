import pandas as pd
import shutil as sh
import os
count = 0
col_list = ["file", "hash"]
dest_folder = '/Users/schadalavada/Documents/dup/moved/'
pd.read_csv('/Users/schadalavada/Documents/dup/duplicates.csv',usecols=col_list)
with open('/Users/schadalavada/Documents/dup/duplicates.csv') as in_file:
    #lines = in_file.readlines()
#with open('/Users/schadalavada/Downloads/dup/duplicates.csv','r') as in_file, open('/Users/schadalavada/Downloads/dup/duplicatesout.csv'','w') as out_file:
    seen = set() # set for fast O(1) amortized lookup
    if count == 0:
        out_file =  open('/Users/schadalavada/Documents/dup/duplisy.csv','w')
        count = count + 1
    for linex in in_file:
        if linex=="":exit
        count = count + 1
        #print(count-1)
        try:
            dumm,line = linex.split(',',2)
        except ValueError:
            print(line)
        if line in seen:
            #sh.copy2(dumm,dest_folder) 
            try:
                #sh.move(dumm,dest_folder)
                os.remove(dumm)
            except (PermissionError,FileNotFoundError) as error:
                print(error)
                continue    
            #sh.rmtree(dumm)
            continue # skip duplicate

        seen.add(line)
        out_file.write(linex)