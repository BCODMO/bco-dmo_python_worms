# BCO-DMO Worms Tool

Used to run scientific names found in a tabular dataset against the WORMS database via the API. 

The program deduplicates scientific names found in a specific column and queries these against the API to minimize API hits. 


Prompts the user for 
- input file name (with the file path included - the file path is relative to where the program is run)

Program outputs 
- 1 csv file containing the deduplicated match results (if no match is found, there is a mostly blank row that still contains the PI_entered_name and an error message
- optional: the user can choose to merge 'PI_entered_name', 'AphiaID', 'scientificname', 'status', 'rank', 'valid_name', 'LSID', 'match_type' to the original data file's columns in a new dataframe


  

                          
