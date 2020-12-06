import pandas as pd
import os


# Location of file with checksums
csv_file = 'D:/Google Drive/Python/remove_duplicate_files/bruni_overview.csv'

# Load csv file
df = pd.read_csv(csv_file)

# Select only duplicate files
duplicates = df[df.duplicated(subset='hash', keep=False)]

# Create list of unique checksums
duplicate_hash = pd.unique(duplicates['hash'])

# Iterate through checksums and remove duplicates, file with shortest path will be kept
for dup in duplicate_hash:
    dup_paths = duplicates[duplicates['hash'] == dup]
    sorted = dup_paths.path.str.len().sort_values().index
    df_sorted = dup_paths.reindex(sorted)
    df_sorted.index = range(len(df_sorted))

    #try:
    if pd.unique([os.path.getsize(x) for x in df_sorted['path']]).shape[0]  == 1:
        remove =  df_sorted[1:]
        for x in remove['path']:
            print('Removing file: {}'.format(x))
            os.remove(x)
    #except:
        #print('Problem, file might already be deleted')
