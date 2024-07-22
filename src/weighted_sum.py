import pandas as pd
import numpy as np

"""
This class implements the weight sum machine learning model, which is used
to merge the three sorted lists for number of runs, lift ticket pricing, and
peak elevation data, created based on users' selected preferences. This model is
responsible for constructing a list that ranks a resort for a criteria that could be
"Most number of runs, don't care about pricing, with highest quality of snow", or 
"Don't care about number of runs, cheapest resorts, highest quality of snow".
@author Aaron Howe
@version Python 3.10.12
"""
class WeightedSumModel:


    """
    Constructor
    @param data: ranked ski resort data acquired from process_data.py
    """
    def __init__(self, data: pd.DataFrame):
        
        data_columns = ['Resort ID', 'Resort', 'Country', 'Run Count', 'Price (USD)', 'Peak Elevation (m)']
        missing_cols = set(data_columns) - set(data.columns)

        if missing_cols:

            raise ValueError(f"Missing input data: {', '.join(missing_cols)}")
        
        self.data = data.copy()
        self.weights = {'Run Count': 0.33, 'Price (USD)': 0.33, 'Peak Elevation (m)': 0.33}
        self.normalized = pd.DataFrame()
        self.w_scores = pd.DataFrame()
        self.final_ranking = pd.DataFrame()
    

    """
    Function to define the weights for each selected feature based on user preference
    @param weights: a dictionary to hold (feature, value) pairs, where value is the weight of each feature
    """
    def feature_weights(self) -> None:

        features = ['Run Count', 'Price (USD)', 'Peak Elevation (m)']
        user_preference = {}

        # Prompting User
        print("Please specify your preferences...\n")
        print("A 'Yes' to Run Count will find resorts with the highest number of runs.")
        print("A 'Yes' to Prices will find resorts with the cheapest prices.")
        print("A 'Yes' to Elevation will find resorts with the highest peak elevation (in meters)\n")

        for feature in features:

            while True:

                response = input(f"{feature} Preference (Yes/No): ").strip().lower()

                if response in ['y', 'yes']:

                    user_preference[feature] = True
                    break

                elif response in ['n', 'no']:

                    user_preference[feature] = False
                    break

                else:

                    print("Input Error: Please Enter a 'Yes' or 'No' Response...")

        feature_weights = 1.0 / len(features)
        self.weights = {f: feature_weights if user_preference[f] else -feature_weights for f in features}

        print("\nCalculated Weights:")
        
        for feature, weight in self.weights.items():

            print(f"{feature}: {weight:.2f}")

        print("\nPositive Values = Higher Run Count and Elevation, and Lower Prices...")
    

    """
    Function for computing normalized scores at 0 to 1 to prevent bias
    """
    def normalize_data(self) -> None:

        if self.data.empty:

            raise ValueError("Data Not Found...")
        
        normalized_features = ['Run Count', 'Price (USD)', 'Peak Elevation (m)']
        self.normalized = self.data[['Resort ID', 'Resort', 'Country']].copy()

        for feature in normalized_features:

            if feature not in self.data.columns:

                raise ValueError(f"Couldn't Find '{feature}' in the Data-Set(s)")
            
            min = self.data[feature].min()
            max = self.data[feature].max()

            # setting the normalized score to 1 if the values of the features are equal
            if min == max:

                self.normalized[f'{feature} (Normalized)'] = 1

            else:

                if feature == 'Price (USD)':

                    self.normalized[f'{feature} (Normalized)'] = (max - self.data[feature]) / (max - min)

                else:

                    self.normalized[f'{feature} (Normalized)'] = (self.data[feature] - min) / (max - min)

        print(f"Normalized Features {', '.join(normalized_features)}")
    

    """
    Algorithm for the weighted sum model, computing the weighted sum for each resort to construct
    a generalized ranking based on user preference
    """
    def weighted_sum_model(self) -> None:

        if self.normalized.empty:

            raise ValueError("Features Not Normalized...")
        
        if not self.weights:

            raise ValueError("No Feature Weights Found...")
        
        self.w_scores = self.normalized[['Resort ID', 'Resort', 'Country']].copy()

        overall_weight = 0

        # weighted_sum computation
        for feature, weight in self.weights.items():

            normalized_features = f'{feature} (Normalized)'

            if normalized_features not in self.normalized.columns:

                raise ValueError(f"Could Not Find Normalized Feature(s): {feature}")
            
            self.w_scores[f'{feature} (Weight)'] = self.normalized[normalized_features] * weight
            overall_weight += self.w_scores[f'{feature} (Weight)']

        self.w_scores['Total Weighted Score'] = overall_weight
        self.w_scores = self.w_scores.sort_values('Total Weighted Score', ascending=False).reset_index(drop=True)
        print(f"Top Resort: {self.w_scores.iloc[0]['Resort']}")

    """
    Constructs a ranking based on the scores comptued from the weighted sum model
    @return the ranked resorts
    """
    def ranking(self) -> pd.DataFrame:

        if self.w_scores.empty:

            raise ValueError("Could Not Find the Overall Total Weighted Scores...")
        
        self.final_ranking = self.w_scores.copy()
        self.final_ranking['Rank'] = self.final_ranking.index + 1

        data_columns = ['Rank', 'Resort ID', 'Resort', 'Country', 'Total Weighted Score']

        for feature in self.weights.keys():

            data_columns.append(f'{feature} (Weight)')

        self.final_ranking = self.final_ranking[data_columns]
        print(f"Top Ranked Resort: {self.final_ranking.iloc[0]['Resort']}")

        return self.final_ranking
    

    """
    Returns the top n ski resorts from the constructed ranked list
    @param n: the top n ski resorts
    @return n
    """
    def return_ranking(self, n=10) -> pd.DataFrame:

        if self.final_ranking.empty:

            raise ValueError("Could Not Find a Final Ranking of Resorts...")
        
        if not isinstance(n, int) or n < 1:

            raise ValueError("Resorts 'n' is found to not hold a positive value...")
        
        if n > len(self.final_ranking):

            print(f"Only {len(self.final_ranking)} Resorts Can be Loaded...")
            n = len(self.final_ranking)

        top_n = self.final_ranking.head(n)

        for _, resort in top_n.iterrows():

            print(f"{resort['Rank']} Ranking: {resort['Resort']}")

        return top_n
