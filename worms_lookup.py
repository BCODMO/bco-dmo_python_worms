import pandas as pd
import requests
from urllib.parse import quote_plus
import os


def read_csv(file_path):
    """Read a CSV file and return the DataFrame."""
    return pd.read_csv(file_path)


def get_unique_values(df, column_name):
    """Get unique values from a specified DataFrame column."""
    return df[column_name].unique()


def fetch_api_data(unique_values):
    """Fetch data from the WoRMS API for a list of unique scientific names."""
    base_url = 'https://www.marinespecies.org/rest/AphiaRecordsByMatchNames?scientificnames%5B%5D='
    api_results = []

    for each in unique_values:
        try:
            url_sp = quote_plus(each)
            url = f'{base_url}{url_sp}&marine_only=true'
            print("Next api query to run:")
            print(url)

            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad responses
            data = response.json()

            for i in data:
                for y in i:
                    y['PI_entered_name'] = each  # Add the scientific name to the result
                    api_results.append(y)

        except requests.exceptions.HTTPError as e:
            print(f"HTTP error: {e}")
            api_results.append({'PI_entered_name': each, 'error_message': 'HTTP error'})
        except Exception as e:
            print(f"Error fetching data: {e}. Likely this means no close match was found.")
            api_results.append({'PI_entered_name': each, 'error_message': 'Error fetching data'})

    return api_results


def save_results_to_csv(results, output_file):
    """Save the results to a CSV file."""
    resulting_df = pd.DataFrame(results)
    resulting_df.to_csv(output_file, index=False)  # Set index=False to avoid writing row numbers


def merge_dataframes(original_df, api_results):
    """Merge the original DataFrame with API results based on PI_entered_name."""
    results_df = pd.DataFrame(api_results)

    # Specify columns to keep after merging
    merge_columns = [
        'PI_entered_name', 'AphiaID', 'scientificname',
        'status', 'rank', 'valid_name', 'LSID', 'match_type'
    ]

    # Perform the merge
    merged_df = original_df.merge(results_df[merge_columns],
                                  left_on='Prey_Taxa',
                                  right_on='PI_entered_name',
                                  how='left')
    return merged_df



def main():
    """Main function to orchestrate the reading, fetching, and saving processes."""
    # Step 1: Get user input for the original file name, output file name, and column name
    original_file = input("Enter the original CSV file name (with extension). The file path is relative from where this program is run: ")
    output_file_name = input("Enter the new file name to save (without an extension)(all files will be created with suffix '_deduplicated_worms_taxa_results': ")
    column_name = input("Enter the name of the column that contains the scientific names in the original file: ")

    # Create the output directory if it doesn't exist
    output_dir = 'output_archive'
    os.makedirs(output_dir, exist_ok=True)

    # Step 2: Read the input CSV
    df = read_csv(original_file)

    # Step 3: Loop to ensure a valid column name is provided
    while True:
        column_name = input("Enter the name of the column that contains the scientific names: ")
        if column_name in df.columns:
            break  # Exit the loop if the column name is valid
        else:
            print(f"Column '{column_name}' not found. Please try again.")

    # Step 4: Get unique values from the specified column
    unique_values = get_unique_values(df, column_name)
    print(f"Unique values in column '{column_name}':\n{unique_values}")

    # Step 5: Fetch data from the API
    api_results = fetch_api_data(unique_values)

    # Step 6: Define the output file path
    output_file = os.path.join(os.path.dirname(original_file), f'{output_file_name}_deduplicated_worms_taxa_results.csv')

    # Step 7: Save the results to a new CSV
    save_results_to_csv(api_results, output_file)
    print(output_file_name + ".csv was saved in the same folder as the input file (relative path = " + os.path.dirname(original_file) + ")")

    # Step 8: Ask the user if they want to merge results onto the original DataFrame
    merge_choice = input("Do you want to merge key results with the original data columns? (yes/no): ").strip().lower()

    if merge_choice == 'yes':
        merged_output_name = input("What do you want to call the merged output file (without extension)? ")
        merged_df = merge_dataframes(df, api_results)

        # Define the merged output file path
        merged_output_file = os.path.join(os.getcwd(), f'{merged_output_name}.csv')
        merged_df.to_csv(merged_output_file, index=False)  # Save the merged DataFrame
        print('Merged results saved to:', merged_output_file)

if __name__ == "__main__":
    main()
