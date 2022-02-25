import duplicates as dup


folder_of_interest = '/Users/schadalavada/Downloads/'
#dup.list_all_duplicates(folder='/Users/schadalavada/Downloads/',to_csv=TRUE,csv_path='/Users/schadalavada/Downloads/dup',fastscan=True)
dup.list_all_duplicates(folder_of_interest, to_csv=True, csv_path='/Users/schadalavada/Documents/dup/', fastscan=True)

