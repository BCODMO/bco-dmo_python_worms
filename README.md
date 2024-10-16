# BCO-DMO WoRMs Tool

This program can be used to check and validate scientific names found in a tabular dataset against the WoRMS database via the API. This program is an alternative to the web based WoRMS interface (which has ~1000 row limits). The fuzzy match logic used in the API leveraged in this program is the same that's applied in the web interface. 

Taxa checks are performed once per column of interest.The program deduplicates scientific names found in a specific column, then queries these against the API to minimize API hits. After the results are pulled from the WoRMS, the user is given the option to create a new file that contains all of the original data merged with the key data from the WoRMs database that allows for comparison/validation. 

**The Program prompts the user for** 
- input file name (with the file path included - the file path is relative to where the program is run)
- the column name in the input file containing scientific names

**Program outputs**
1)  1 csv file containing the deduplicated match results showing all possile API output and the original "PI_entered_name". If no match is found in WoRMS, there is a mostly blank row that still contains the "PI_entered_name" and an error message in an "error_message" column. 
2) optional: the user can choose to merge 'PI_entered_name', 'AphiaID', 'scientificname', 'status', 'rank', 'valid_name', 'LSID', 'match_type' to the original data file's columns in a new dataframe.

Match Types output by the API (and into the resulting spreadsheet)
exact - all characters match exactly
exact_subgenus - an exact match, but including the subgenus
phonetic - sounds similar as, despite minor differences in spelling (soundex algorithm)
near_1 - perfect match, except for one character. This is a quite reliable match
near_2 - good match, except for two characters. This needs an extra check
near_3 - good match, except for three characters. This definitely needs an extra check
match_quarantine - match with a name that is currently in quarantine. Any name that has been used in the literature should in principle not be quarantined. So best to contact the WoRMS DMT about this
match_deleted - this is a match with a name that has been deleted and no alternative is available. Please contact the WoRMS DMT when you come across this. 

**Refs**
WoRMS API info: https://www.marinespecies.org/rest/
WoRMS Web interface: https://www.marinespecies.org/aphia.php?p=match 
