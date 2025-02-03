import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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

        # Data type info
        print('=='*20 + f'\nData Summary\n' + '=='*20 )
        data_summary = df.info() 
        print('=='*20 +'\n')

        # Descriptive statistics
        describe =  df.describe() 
        print('=='*20 + f'\nDescriptive Statistics\n' + '=='*20  )
        display(describe)
        
        #Display the dataset
        # Adjust display options to show all columns
        # pd.set_option('display.max_columns', None)
        print('=='*20 + f'\nDataset Overview\n'+ '=='*20 )
        return display(df.head())
        
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
        null_counts = self.df.isnull().sum()

        display(null_counts)
        

    def drop_specified_columns(self, columns):
        """
        Drop specified columns from the DataFrame.
        """
        print(f"Dropping missing values in columns: {columns}")
        self.df.dropna(subset=columns, inplace=True)

        display(self.df.isna().sum())

        return self.df
    
    def check_outliers_and_plot(self):
        """
        Detect outliers in numerical columns using the IQR method and plot boxplots.
        """
        

        outlier_columns = []

        for column in self.numerical_columns:
            Q1 = self.df[column].quantile(0.25)
            Q3 = self.df[column].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR

            # Find outliers
            outlier_indices = self.df[(self.df[column] < lower_bound) | (self.df[column] > upper_bound)].index.tolist()

            if outlier_indices: 
                outlier_columns.append(column)

        print("***********************************************")
        print("Columns Containing Outliers Include:", outlier_columns)
        print("***********************************************")

        if outlier_columns:
            # Plot boxplots for columns with outliers
            num_rows = (len(outlier_columns) + 2) // 3
            num_cols = min(len(outlier_columns), 3)
            fig, axes = plt.subplots(nrows=num_rows, ncols=num_cols, figsize=(20, 8))

            # Ensure axes is always iterable
            if len(outlier_columns) == 1:
                axes = [axes]  # Make axes a list to allow consistent indexing
            else:
                axes = axes.flatten() if num_rows > 1 else axes

            for i, column in enumerate(outlier_columns):
                sns.boxplot(x=self.df[column], ax=axes[i])
                axes[i].set_xlabel(column)
                axes[i].set_ylabel('Values')
                axes[i].set_title(f'{column}')
                axes[i].tick_params(axis='x', rotation=45)

            # Remove any unused subplots
            if len(outlier_columns) < len(axes):
                for j in range(len(outlier_columns), len(axes)):
                    fig.delaxes(axes[j])

            # Adjust layout to prevent overlapping
            plt.tight_layout()
            plt.show()
        else:
            print("NO OUTLIERS FOUND")

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

class EDA:
    """Class to Perform EDA on the dataset."""
    col_list = ['brand', 'year', 'price_in_kes', 'made_in_group', 'body_type_group', 
                'grouped_seating_capacity', 'fuel_type_grouped', 'transmission_group', 'drive_type_group']

    def __init__(self):
        pass
    
    def plot_univariate(self, data, column):
        """Plots univariate analysis for a given column using Seaborn."""
        plt.figure(figsize=(8, 5))
        
        if data[column].dtype == 'object':  # Categorical
            if data[column].nunique() <= 10:  # Few unique categories
                sns.countplot(x=column, data=data, order=data[column].value_counts().index, hue=column, palette="viridis")
                plt.xticks(rotation=30)
                plt.title(f"Distribution of {column.title()}")
            else:  # More than 10 unique categories
                top_10_categories = data[column].value_counts().nlargest(10).index
                filtered_data = data[data[column].isin(top_10_categories)]
                sns.countplot(x=column, data=filtered_data, order=top_10_categories, hue=column, palette="viridis")
                plt.xticks(rotation=30)
                plt.title(f"Top 10 Categories in {column.title()}")
        else:  # Numerical
            sns.histplot(data[column], kde=True, color="blue")
            plt.title(f"Distribution of {column.title()}")
            plt.xlabel(column)
            plt.ylabel("Frequency")
        
        plt.tight_layout()
        plt.show()

    def plot_bivariate(self, data, column, target):
        """Plots bivariate analysis for a given column against the target variable."""
        
        # Ensure we're not plotting the target against itself
        if column == target:
            # print(f"Skipping: {column} is the target variable.")
            return
        
        plt.figure(figsize=(8, 5))

        if data[column].dtype == 'object':  # Categorical
            if data[column].nunique() < 10:  # Few unique categories
                sns.boxplot(x=column, y=target, data=data, order=data[column].value_counts(ascending=False).index)
                plt.xticks(rotation=45)
                plt.title(f"{target} vs. {column.title()}")
            else:  # More than 10 unique categories
                top_10_categories = data[column].value_counts().nlargest(10).index
                filtered_data = data[data[column].isin(top_10_categories)]
                sns.boxplot(x=column, y=target, data=filtered_data, order=top_10_categories)
                plt.xticks(rotation=30)
                plt.title(f"{target} vs. {column.title()} (Top 10 Categories)")
        else:  # Numerical
            sns.scatterplot(x=column, y=target, data=data)
            plt.title(f"{target} vs. {column.title()}")

        plt.tight_layout()
        plt.show()

    
    
    
