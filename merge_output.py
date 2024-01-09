import os
import pandas as pd
import argparse

def merge_csv_files(parent_dir, output_dir, verbose=False):
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Dictionary to store merged dataframes
    merged_dataframes = {}

    # List to store directories without CSV files
    directories_without_csv = []

    # Loop through each directory inside the parent directory
    for dir_name in sorted(os.listdir(parent_dir)):
        dir_path = os.path.join(parent_dir, dir_name)
        
        if os.path.isdir(dir_path):
            if verbose:
                print(f"Processing directory: {dir_path}")

            # Get the list of files in the directory
            files = os.listdir(dir_path)

            # Check if the directory contains any CSV files
            csv_files = [file for file in files if file.lower().endswith('.csv') and file != "Experiment.csv"]
            if not csv_files:
                directories_without_csv.append(dir_name)
                if verbose:
                    print(f"Warning: No CSV files found in directory: {dir_path}")
                continue

            # Loop through each CSV file in the directory
            for file in csv_files:
                file_path = os.path.join(dir_path, file)
                if verbose:
                    print(f"Reading file: {file_path}")

                # Read the CSV file into a pandas DataFrame
                df = pd.read_csv(file_path)

                # Get the filename without extension as the key for the dictionary
                filename_without_ext = os.path.splitext(file)[0]

                # Merge dataframes with the same filename in the merged_dataframes dictionary
                if filename_without_ext in merged_dataframes:
                    merged_dataframes[filename_without_ext] = pd.concat([merged_dataframes[filename_without_ext], df])
                else:
                    merged_dataframes[filename_without_ext] = df

    # Save the merged dataframes as separate CSV files in the output directory
    for filename, df in merged_dataframes.items():
        output_path = os.path.join(output_dir, f"{filename}.csv")
        if verbose:
            print(f"Saving merged dataframe to: {output_path}")
        df.to_csv(output_path, index=False)

    # Display an error message if there are directories without CSV files
    if directories_without_csv:
        print("\nError: Some directories do not contain any CSV files:")
        for dir_name in directories_without_csv:
            print(f"- {dir_name}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Merge CSV files with the same name from different batches into one.")
    parser.add_argument("parent_directory", help="Parent directory containing batch directories with CSV files")
    parser.add_argument("output_directory", help="Output directory to save the merged CSV files")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose mode")
    args = parser.parse_args()

    # Call the merge_csv_files function with the provided parent directory, output directory, and verbosity setting
    merge_csv_files(args.parent_directory, args.output_directory, args.verbose)