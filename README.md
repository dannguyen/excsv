# excsv

A command-line utility for converting CSV files into Excel sheets. 

(Other utilities included)


Install this tool using `pip`:



```bash
pip install excsv
```


Basic usage:

```bash
excsv mydata.csv > mysheet.xlsx

# or if you dislike unix redirect operator
excsv mydata.csv -o mysheet.xlsx

# or full unix style
cat mydata.csv | excsv > mysheet.xlsx
```


## Notes and TODOS

### 2024-03-15

- Rudimentary functionality as I decide whether or not to implement features that are already done best in xsv and csvkit.

- Change focus to tools/functions that are most needed when populating a spreadsheet, such as removing bad characters/control characters, unintended excess whitespace, renaming headers, etc.

Things to add:
- `excel` option flags to configure frozen header, filters (yes/no), font formatting, and setting every field to the width of its longest values
    - let user name sheet name
    - maybe allow for multiple input CSVs, creating tabs for each one
    - if `-o` points to an existing excel file, then append? 
- `infer` make this actually useful. Infer most likely datatypes. Indicate cardinality and common values
- `flatten` like `xsv flatten` but copy-pasteable as tab-delimited output. a flattened version of the inference report could optionally be a "meta" tab in `excel`
- `litmus` a utility for some basic data integrity checks
    - given a column and datatype, e.g. int,float,datetiime spit out all values that aren't able to be typecast
    - allow testing against regex pattern
    - count null values

- `validate` not all data files that can be converted to Excel necessarily need to be valid data dables, but for CSVs that are meant to be valid data tables, give users ability to enforce/check that
    - require first row to be headers
    - make sure headers are unique (how does sqlite-utils do it?)

- `cleanspace`
    - clean up header names, strip whitespace from headers/values, etc.
    - allow user to specify when data starts and ends (i.e. to ignore first/final few rows of metadata)

- `head/tail`:
    - quickly inspect the first/last few rows



## Dev and Testing


```sh
# install locally
$ pip install -e .


# run all tests
$ pytest

# run just alpha tests
$ pytest -m 'alpha'


# skip alpha tests
$ pytest -m 'not alpha'
```


