import os
import pandas as pd
import argparse

def merge_csv_files(dir_paths, output_dir):
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Dictionary to store merged dataframes
    merged_dataframes = {}

    # Loop through each directory
    for dir_path in dir_paths:
        # Get the list of files in the directory
        files = os.listdir(dir_path)

        # Loop through each CSV file in the directory
        for file in files:
            # Check if the file is a CSV file
            if file.lower().endswith('.csv'):
                file_path = os.path.join(dir_path, file)

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
        df.to_csv(output_path, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Merge CSV files with the same name from different directories.")
    parser.add_argument("directories", nargs="+", help="List of directories containing CSV files")
    parser.add_argument("output_directory", help="Output directory to save the merged CSV files")
    args = parser.parse_args()

    # Call the merge_csv_files function with the provided directories and output directory
    merge_csv_files(args.directories, args.output_directory)
