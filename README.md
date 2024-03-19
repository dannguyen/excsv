# excsv

A command-line utility for converting CSV files into Excel sheets. 

(Other utilities included)


Install this tool using `pip`:



```bash
pip install excsv
```


Basic usage:

```bash
# input file as argument, output file as -o
excsv mydata.csv -o mysheet.xlsx


cat mydata.csv | excsv -o mysheet.xlsx
```


## Notes and TODOS

### 2024-03-19

- consider switching openpyxl to xlswriter for creating excel files: https://xlsxwriter.readthedocs.io/working_with_memory.html
    - use openpyxl for testing only



### 2024-03-15

### Similar libraries

- [deztec/csv2excel](https://github.com/deztec/csv2excel): 

    > .NET command line tool to convert delimited files to Microsoft Excel format (xls/xlsx) without Microsoft Excel having to be installed.

    `$ csv2excel.exe -i input.csv`

- [mentax/csv2xlsx](https://github.com/mentax/csv2xlsx):
    ~~~sh
    $ csv2xlsx --template example/template.xlsx \
        --sheet Sheet_1 --sheet Sheet_2 \
        --row 2 \
        --output result.xlsx data.csv data2.csv`
    ~~~

### TODOS 2024-03-15

- Use write_only mode for faster performance: https://openpyxl.readthedocs.io/en/latest/optimized.html
>>>>>>> 9a8c8b5 (f)

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


- `probe`:
    - add min, max, most common value, longest value (chars)
    - detect file size, if large, use count-min-sketch and hyperloglog


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


