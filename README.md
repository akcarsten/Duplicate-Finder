# About Duplicates Finder

Duplicates Finder is a simple Python package that identifies duplicate files in and across folders. 
There are three ways to search for identical files:
1. List all duplicate files in a folder of interest.
2. Pick a file and find all duplications in a folder.
3. Directly compare two folders against each other.

The results are saved as a Pandas Dataframe or can be exported as .csv files.

---
## Installation

You can either clone the repository directly from the Github webpage or run the following command(s) in your terminal:

Pip Installation:
```
pip install duplicate-finder
```

Alternatively you can clone the Git repository:
```
git clone https://github.com/akcarsten/duplicates.git
```

Then go to the folder to which you cloned the repository and run:

```
python setup.py install
```

Now you can run Python and import the Bitfinex client.

---
## Examples of how to use the package

#### Example 1: List all duplicate files in a folder of interest.
```python
import duplicates as dup


folder_of_interest = 'C:/manyDuplicatesHere/'
dup.list_all_duplicates(folder_of_interest, to_csv=True, csv_path='C:/csvWithAllDuplicates/')
```
If only a specific type of files is of interest this can be further defined by the 'ext' parameter. For example:
```python
df = dup.list_all_duplicates(folder_of_interest, to_csv=True, csv_path='C:/csvWithAllDuplicates/', ext='.jpg')
```

#### Example 2: Pick a file and find all duplications in a folder.
```python
import duplicates as dup


file_of_interest = 'C:/manyDuplicatesHere/thisFileExistsManyTimes.jpg'
folder_of_interest = 'C:/manyDuplicatesHere/'
df = dup.find_duplicates(file_of_interest, folder_of_interest)
```

#### Example 3: Directly compare two folders against each other.
```python
import duplicates as dup


folder_of_interest_1 = 'C:/noDuplicatesHere/'
folder_of_interest_2 = 'C:/noDuplicatesHereAsWell/'
df = dup.compare_folders(folder_of_interest_1, folder_of_interest_2)
```

As in *Example 1* above a specific filetype can be selected and the results can be written to a .csv file.
