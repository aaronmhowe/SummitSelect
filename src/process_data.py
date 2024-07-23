import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, StandardScaler
import os

"""
This class performs data pre-processing on the three ski resort datasets, where we are
managing reading and loading the data into memory, and merging the three key features (run count, prices, elevation).
The resulting data will then be used to construct rankings based on the results of the ranking algorithm.
@author Aaron Howe
@version Python 3.10.12
"""
class PreProcessing:


    """
    Constructor
    @param run_count_data: path to data for each ski resorts' run counts
    @param price_data: path to data for each ski resorts' adult lift ticket price
    @param elevation_data: path to data for each ski resorts' peak elevation
    """
    def __init__(self, run_count_data, price_data, elevation_data):

        self.run_count_data = run_count_data
        self.price_data = price_data
        self.elevation_data = elevation_data
        self.run_count_dataframe = None
        self.price_dataframe = None
        self.elevation_dataframe = None

    """
    Reads the data from each input file and loads them into memory
    """
    def read_data(self):

        try:
            self.run_count_dataframe = pd.read_csv(self.run_count_data)
            self.price_dataframe = pd.read_csv(self.price_data)
            self.elevation_dataframe = pd.read_csv(self.elevation_data)
        except FileNotFoundError as e:
            print(f"Ran into an Error: One of the input files could not be found. {e}")
            raise
        except pd.errors.EmptyDataError:
            print("Ran into an Error: One of the input files does not contain data.")
            raise
        except pd.errors.ParserError as e:
            print(f"Ran into an Error: A problem occurred while parsing one of the input files: {e}")
            raise
        except Exception as e:
            print(f"Ran into an Error: Failed to load input data into memory: {e}")
            raise


    """
    Organizes each frame of data
    @param data: a single frame of data
    """
    def organize_data(self, data: pd.DataFrame, name: str) -> pd.DataFrame:

        data = data.drop(columns=[col for col in data.columns if 'Unnamed:' in col])

        # dumping duplicated rows
        rows = len(data)
        data.drop_duplicates(inplace=True)
        print(f"Removed {rows - len(data)} Duplicates...")

        # dumping non-numerical vals
        data.dropna(how='all', inplace=True)
        print(f"Removed non-numerical values from the data.")

        # ignoring white space
        for col in data.select_dtypes(include=['object']).columns:
            data[col] = data[col].str.strip()

        for col in data.columns:
            if data[col].dtype == 'object':
                try:
                    # type conversion
                    data[col] = pd.to_numeric(data[col])
                except ValueError:
                    pass

        # organizing the data-frames of each key feature
        if name == 'runs':
            if 'Run Count' in data.columns:
                data['Run Count'] = data['Run Count'].fillna(0).abs().astype(int)
        elif name == 'prices':
            if 'Price (USD)' in data.columns:
                data['Price (USD)'] = data['Price (USD)'].astype(float)
        elif name == 'elevation':
            if 'Peak Elevation (m)' in data.columns:
                data['Peak Elevation (m)'] = data['Peak Elevation (m)'].fillna(data['Peak Elevation (m)'].mean()).abs()

        print(f"Data Organized")
        return data


    """
    Method to merge all three datasets into a single frame of data
    """
    def merge_data(self) -> pd.DataFrame:

        if self.run_count_dataframe is None or self.price_dataframe is None or self.elevation_dataframe is None:
            raise ValueError("Data from all three files must first be loaded into memory before they can be merged.")
        try:
            # merging run count and price data
            merged_data = pd.merge(self.run_count_dataframe, self.price_dataframe, on='Resort ID', how='outer')

            # merging run-price merge with elevation
            merged_data = pd.merge(merged_data, self.elevation_dataframe, on="Resort ID", how='outer')

            # handling missing data
            missing_runs = merged_data[merged_data['Run Count'].isna()]['Resort']
            missing_prices = merged_data[merged_data['Price (USD)'].isna()]['Resort']
            missing_elevation = merged_data[merged_data['Peak Elevation (m)'].isna()]['Resort']

            if not missing_runs.empty:
                print(f"Resorts missing data for number of runs: {', '.join(missing_runs)}")
            if not missing_prices.empty:
                print(f"Resorts missing data for prices: {', '.join(missing_prices)}")
            if not missing_elevation.empty:
                print(f"Resorts missing data for peak elevation: {', '.join(missing_elevation)}")

            print(f"Input Data Merged!")

            # return merged data-set
            self.merged_data = merged_data
            return self.merged_data
        
        except KeyError as e:
            print(f"Ran into an Error During Merge: {e}")
            raise
        
        except Exception as e:
            print(f"Ran into an Error During Merge: {e}")
            raise


    """
    Precautionary method to handle potential holes in the merged dataset
    @param data: single frame of data (merged)
    """
    def debug_data(self, data: pd.DataFrame) -> pd.DataFrame:

        missing_data = data.isnull().sum()
        print("Missing Values:")
        print(missing_data[missing_data > 0])

        # handling missing values under each feature
        if 'Run Count' in data.columns:
            data['Run Count'] = data['Run Count'].fillna(data['Run Count'].median())
        if 'Price (USD)' in data.columns:
            data['Price (USD)'] = data['Price (USD)'].fillna(data['Price (USD)'].median())
        if 'Peak Elevation (m)' in data.columns:
            data['Peak Elevation (m)'] = data['Peak Elevation (m)'].fillna(data['Peak Elevation (m)'].median())
            
        feature_column = data.select_dtypes(include=['object']).columns
        
        for col in feature_column:
            data[col] = data[col].fillna(data[col].mode()[0])

        # extra-cautionary checking for missing data
        double_check = data.isnull().sum()
        print("\nMissing Values:")
        print(double_check[double_check > 0])

        if double_check.sum() == 0:
            print("There are no holes in the data...")
        else:
            print("Potential Problem: There are still some values missing in the data...")

        return data


    """
    Straight-forward numerical normalization to remove bias in the data
    @param data: single frame of data (merged)
    """
    def normalize_data(self, data: pd.DataFrame) -> pd.DataFrame:

        normalized = data.copy()
        data_columns = normalized.select_dtypes(include=['int64', 'float64']).columns
        data_columns = [col for col in data_columns if col != 'Resort ID']

        # min-max scaling price data
        if 'Price (USD)' in data_columns:
            min_max_scaler = MinMaxScaler()
            normalized['Price (USD)'] = min_max_scaler.fit_transform(normalized[['Price (USD)']])

        # normalizing run-count and peak elevation via the z-score method
        for col in ['Run Count', 'Peak Elevation (m)']:
            if col in data_columns:
                standard_scaler = StandardScaler()
                normalized[col] = standard_scaler.fit_transform(normalized[[col]])

        double_check = set(data_columns) - {'Price (USD)', 'Run Count', 'Peak Elevation (m)'}
        
        if double_check:
            print(f"Potential Problem: Data not Normalized: {', '.join(double_check)}")

        return normalized
    

    """
    Method to perform validation checks on the merged data, ensuring that values
    attached to ski resorts match their values in their native datasets.
    @param data: single frame of data (merged)
    """
    def validation(self, data: pd.DataFrame) -> bool:

        valid = True

        # validating column headers
        data_columns = ['Resort ID', 'Resort', 'Country', 'Run Count', 'Price (USD)', 'Peak Elevation (m)']
        missing_columns = set(data_columns) - set(data.columns)

        if missing_columns:
            print(f"Columns of Data Missing: {', '.join(missing_columns)}")
            valid = False

        # validating existing data vals
        if data.isnull().any().any():
            print("Ran into an Error: There are Missing Values...")
            print(data.isnull().sum())
            valid = False

        # validating data types
        data_types = {
            'Resort ID': 'int64',
            'Resort': 'object',
            'Country': 'object',
            'Run Count': 'int64',
            'Price (USD)': 'float64',
            'Peak Elevation (m)': 'float64'
        }

        for col, expected_data_type in data_types.items():
            if col in data.columns:
                if data[col].dtype != expected_data_type:
                    print(f"Ran into an Error: Column '{col}' has Data Type {data[col].dtype}, but Expected {expected_data_type}")
                    data[col] = data[col].astype(expected_data_type)
                    print(f"Converted '{col}' to {expected_data_type}")

        # validating value signs
        if 'Run Count' in data.columns and (data['Run Count'] < 0).any():
            print("Ran into an Error: Run Count contains negative values...")
            data['Run Count'] = data['Run Count'].abs()

        if 'Price (USD)' in data.columns and (data['Price (USD)'] < 0).any():
            print("Ran into an Error: Price contains negative values...")
            data['Price (USD)'] = data['Price (USD)'].abs()

        if 'Peak Elevation (m)' in data.columns and (data['Peak Elevation (m)'] < 0).any():
            print("Ran into an Error: Peak Elevation contains negative values...")
            data['Peak Elevation (m)'] = data['Peak Elevation (m)'].abs()

        # validating that each resort has a unique ID#
        if 'Resort ID' in data.columns and not data['Resort ID'].is_unique:
            print("Ran into an Error: Resort ID # is not valid...")
            valid = False

        # validating country assignments
        if 'Country' in data.columns:
            if not all(data['Country'].isin(['United States', 'Canada'])):
                print("Ran into an Error: There is an entry under 'Country' other than 'United States' and 'Canada'")
                valid = False

        if valid:
            print("Validation Checks Passed Successfully!")
        else:
            print("Validation Checks Failed, There are Errors in Data Organization.")
        
        return valid


    """
    This function serves to writing the manipulated input data to a new CSV file that will be
    used as input for sorting and computing the weighted sum
    @param data: the individual frames of data being written
    @param output_file: the new CSV to receive the data as output-input
    """
    def write_csv(self, data: pd.DataFrame, output_file: str) -> None:

        output_file = "data-sets/processed_resorts_data.csv"

        try:
            os.makedirs(os.path.dirname(output_file), exist_ok=True)

            data.to_csv(output_file, index=False)
            print(f"Pre-Processed Data Written to: {output_file}")

        except IOError as e:
            print(f"Ran into an Error: Problem occurred saving processed data to a CSV: {e}")
            raise

        except Exception as e:
            print(f"Ran into an Error: Problem occurred while saving processed data to a CSV: {e}")
            raise

    """
    Manages the flow of every other method in this class, ensuring every method is called
    in the proper order
    """
    def pre_process_data(self) -> pd.DataFrame:

        try:
            self.read_data()
            print("Data Read and Loaded into Memory...")

            self.run_count_dataframe = self.organize_data(self.run_count_dataframe, 'runs')
            self.price_dataframe = self.organize_data(self.price_dataframe, 'prices')
            self.elevation_dataframe = self.organize_data(self.elevation_dataframe, 'elevation')
            print("Data Organized...")

            merged_data = self.merge_data()
            print("Data Merged...")

            debugged_data = self.debug_data(merged_data)
            print("Data Debugged...")

            debugged_data['Run Count'] = debugged_data['Run Count'].astype(int)
            debugged_data['Price (USD)'] = debugged_data['Price (USD)'].astype(float)
            debugged_data['Peak Elevation (m)'] = debugged_data['Peak Elevation (m)'].astype(float)
            print("Converted Data Types...")

            normalized_data = self.normalize_data(debugged_data)
            print("Data Normalized...")

            if not self.validation(normalized_data):
                raise ValueError("Potential Error Warning: Validation Failed, Execution Will Continue, But May Fail...")

            pre_processed_data = normalized_data

            output_file = ("data-sets", "processed-resorts-data.csv")
            self.write_csv(pre_processed_data, output_file)

            return pre_processed_data

        except Exception as e:
            print(f"Ran into an Error: Pre-Processing Failed: {str(e)}")
            raise  
