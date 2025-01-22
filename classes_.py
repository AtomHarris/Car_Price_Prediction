import os
import numpy as np
import pandas as pd


class DataLoading:
    def __init__(self):
        pass

    def read_data(self, file_path):
        """Reading the file"""
        _,file_ext =os.path.splitext(file_path)

        if file_ext == '.csv':
            return pd.read_csv(file_path, index_col=None)
        
        elif file_ext == '.tsv':
            return pd.read_csv(file_path, sep='\t')

        elif file_ext == '.json':
            return pd.read_json(file_path)

        elif file_ext in ['.xls', '.xlsx']:
            return pd.read_excel(file_path)

        else:
            raise ValueError(f"Unsupported file format:")
        
class DataInfo:
    """Class to get dataset information """
    def __init__(self):      
        pass

    def info(self, df): 
        """
        Displaying Relevant Information on the the Dataset Provided
        """    
        # Counting no of rows 
        print('=='*20 + f'\nShape of the dataset : {df.shape} \n' + '=='*20 + '\n')
        
        # Extracting column names
        column_name =  df.columns 
        print('=='*20 + f'\nColumn Names\n' + '=='*20 +  f'\n{column_name} \n ')
        # List of all numerical columns
        numerical_cols = df.select_dtypes(include=[np.number]).columns
        print('=='*20 + f'\nNumerical Columns\n' + '=='*20)
        print(numerical_cols, end="\n\n")
        
        # List of all categorical columns
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns
        print('=='*20 + f'\nCategorical Columns\n' + '=='*20)
        print(categorical_cols, end="\n\n")

        # Descriptive statistics
        describe =  df.describe() 
        print('=='*20 + f'\nDescriptive Statistics\n' + '=='*20  )
        display(describe)
        
        #Display the dataset
        # Adjust display options to show all columns
        pd.set_option('display.max_columns', None)
        print('=='*20 + f'\nDataset Overview\n'+ '=='*20 )
        return df.head()
class DataChecks:
    """Class to Perform various checks on the dataset"""
    def __init__(self, df):
        self.df = df
        self.categorical_columns = [] 
        self.numerical_columns = []
        self.null_info = None  # To store missing values information
        self._identify_columns()

    def _identify_columns(self):
        """
        Identify numerical and categorical columns.
        """
        for col in self.df.columns:
            if self.df[col].dtype == object:
                self.categorical_columns.append(col)
            else:
                self.numerical_columns.append(col)
        
    def check_duplicates(self):
        """
        Display the duplicated rows for visual assessment.
        """
        df_sorted = self.df.sort_values(by=self.df.columns.tolist())

        # Find duplicated rows
        duplicates = df_sorted[df_sorted.duplicated(keep=False)]

        print("***********************************************")
        print(" Total Number of Duplicated Rows:", len(duplicates))
        print("***********************************************")

        if not duplicates.empty:
            # Display the duplicated rows as HTML
            display(duplicates)
        else:
            print("NO DUPLICATES FOUND")

    def drop_duplicated(self):
        """
        Drop duplicate rows from the dataset.
        """
        # Dropping the duplicates
        self.df.drop_duplicates(inplace=True)
        print("Duplicates have been removed.")
        return self.df

    def check_missing(self):
        """
        Identify Null values in the dataset as value counts and percentages.
        """
        # Get features with null values
        null_features = self.df.columns[self.df.isnull().any()].tolist()
        
        if null_features:
            # Calculate the number of missing values for each feature
            null_counts = self.df[null_features].isnull().sum()
            
            # Calculate the percentage of missing data for each feature
            null_percentages = self.df[null_features].isnull().mean() * 100
            
            # Create a DataFrame to display the results
            self.null_info = pd.DataFrame({
                'Column Names': null_features,
                'Missing Values': null_counts,
                'Percentage Missing': null_percentages
            }).reset_index(drop=True)
            
            # Display the results
            display(self.null_info)
        else:
            self.null_info = None
            print("NO NULL VALUES FOUND") 

    def drop_missing(self, threshold=30):
        """
        Drop columns with more than `threshold` percent missing values.
        """
        if self.null_info is None:
            print("No missing value analysis found. Please run `check_missing` first.")
        else:
            # Identify columns to drop based on the threshold
            columns_to_drop = self.null_info[
                self.null_info['Percentage Missing'] > threshold
            ]['Column Names'].tolist()

            if columns_to_drop:
                print(f"Dropping columns with more than {threshold}% missing values: {columns_to_drop}")
                self.df.drop(columns=columns_to_drop, inplace=True)
            else:
                print(f"No columns found with more than {threshold}% missing values.")
        return self.df
