import pandas as pd
import numpy as np

"""
This class ranks ski resorts based on a set of user selected criteria, involving preferences
on number of runs, prices for adult lift tickets, and the resorts' peak elevation. The user
may decide they care more about high run counts with low pricing, but not be picky about
the peak elevation of the resort, and thus the #1 resort in their output should mirror those
preferences. I implement various sorting algorithms that work together to compile the most accurate
list for the users' preferences.
@author Aaron Howe
@version Python 3.10.12
"""
class RankingSkiResorts:


    """
    Constructor
    @param data: data from pre-processing
    """
    def __init__(self, data: pd.DataFrame):

        if not isinstance(data, pd.DataFrame):

            raise TypeError("Input data needs to be a DataFrame...")
        
        data_columns = ['Resort ID', 'Resort', 'Country', 'Run Count', 'Price (USD)', 'Peak Elevation (m)']
        missing_cols = set(data_columns) - set(data.columns)

        if missing_cols:
            
            raise ValueError(f"Missing input data: {', '.join(missing_cols)}")
        
        self.data = data.copy()
        self.run_count_ranking = None
        self.price_ranking = None
        self.elevation_ranking = None

        print(f"Class Constructed with {len(self.data)} Resorts...")
    

    """
    Sorting the data by number of runs
    @param ascending: If false, sort from most to least number of runs
    @return pandas.DataFrame: a single frame of data containing the sorted list by run count
    """
    def sorting_by_run_count(self, ascending=False) -> pd.DataFrame:

        if self.data is None:
            
            raise ValueError("Could Not Find Data...")
        
        try:

            sorted_data = self.data.sort_values(by='Run Count', ascending=ascending)
            sorted_data['Run Count Ranking'] = range(1, len(sorted_data) + 1)

            data_columns = ['Run Count Ranking', 'Resort ID', 'Resort', 'Country', 'Run Count']
            self.run_count_ranking = sorted_data[data_columns]

            print(f"Sorted by Run Count ({'ascending' if ascending else 'descending'} Order...)")
            
            return self.run_count_ranking
        
        except KeyError:

            raise KeyError("Run Count not Found. Potential Issue with Data Processing...")
        
        except Exception as e:

            raise Exception(f"Ran into an Error: Problem occurred while sorting the data... {str(e)}")
    

    """
    Sorting the data by prices of lift tickets
    @param ascending: If true, sort from least to most expensive
    @return pandas.DataFrame: a single frame of data containing the sorted list by price
    """
    def sorting_by_price(self, ascending=True) -> pd.DataFrame:

        if self.data is None:

            raise ValueError("Could Not Find Data...")
        
        try:

            sorted_data = self.data.sort_values(by='Price (USD)', ascending=ascending)
            sorted_data['Price Ranking'] = range(1, len(sorted_data) + 1)

            data_columns = ['Price Ranking', 'Resort ID', 'Resort', 'Country', 'Price (USD)']
            self.price_ranking = sorted_data[data_columns]

            print(f"Sorted by Price ({'ascending' if ascending else 'descending'} Order...)")

            return self.price_ranking

        except KeyError:

            raise KeyError("Price (USD) not found. Potential Issue with Data Processing...")

        except Exception as e:

            raise Exception(f"Ran into an Error: Problem occurred while while sorting the data... {str(e)}")        


    """
    Sorting the data by peak elevation (a metric to estimate quality of snow)
    @param ascending: If false, sort from highest to lowest peak elevation
    @return pandas.DataFrame: a single frame of data containing the sorted list by peak elevation
    """
    def sorting_by_elevation(self, ascending=False) -> pd.DataFrame:

        if self.data is None:

            raise ValueError("Could not Find Data...")
        
        try:

            sorted_data = self.data.sort_values(by='Peak Elevation (m)', ascending=ascending)
            sorted_data['Elevation Ranking'] = range(1, len(sorted_data) + 1)

            data_columns = ['Elevation Ranking', 'Resort_ID', 'Resort', 'Country', 'Peak Elevation (m)']
            self.elevation_ranking = sorted_data[data_columns]

            print(f"Sorted by Peak Elevation ({'ascending' if ascending else 'descending'} Order...)")

            return self.elevation_ranking
        
        except KeyError:

            raise KeyError("Peak Elevation not Found. Potential Problem with Data Processing...")
        
        except Exception as e:

            raise Exception(f"Ran into an Error: Problem occurred while sorting data... {str(e)}")
    

    """
    constructs a ranking of resorts based on user selected criteria, using the sorted lists
    @param user_criteria: users' selected feature (runs, prices, elevation)
    @param ascending: If false, constructs a ranking from "I care" to "I don't care"
    """
    def criteria(self, user_criteria, ascending=False) -> pd.DataFrame:

        if self.data is None:

            raise ValueError("Could not Find Data...")
        
        hash = {
            'runs': ('Run Count', 'Run Count Ranking', self.sorting_by_run_count),
            'price': ('Price (USD)', 'Price Ranking', self.sorting_by_price),
            'elevation': ('Peak Elevation (m)', 'Elevation Ranking', self.sorting_by_elevation)
        }

        if user_criteria.lower() not in hash:

            raise ValueError("Criteria Not Valid. Choose Between 'runs', 'price', and/or 'elevation'!")
        
        column, ranking_column, sorting = hash[user_criteria.lower()]

        if user_criteria.lower() == 'price':

            ranking = sorting(not ascending)

        else:

            ranking = sorting(ascending)

        print(f"Constructed Ranking Based on User Preference {user_criteria} ({'ascending' if ascending else 'descending'} Order...)")

        return ranking
    

    """
    This function takes the ranking from users' preferences, and returns their top N resorts
    @param ranking: the ranked list of resorts based on preference (run list, price list, elevation list)
    @param n: variable defining how many top n resorts to return
    @return top n resorts per preference
    """
    def return_ranking(self, ranking: pd.DataFrame, n=10) -> pd.DataFrame:

        if not isinstance(ranking, pd.DataFrame):

            raise TypeError("Ranking needs to be in a DataFrame...")
        
        if ranking.empty:

            raise ValueError("Ranking Data Empty...")
        
        if n < 1:

            raise ValueError("Value of N is negative, needs to be positive...")
        
        if n > len(ranking):

            print(f"The value of N ({n}) appears to be greater than the number of resorts in the ranking ({len(ranking)}), this is an error...")
            print("Will return all resorts...")
            n = len(ranking)

        top_n = ranking.head(n)

        print(f"Producing Top {n} Resorts...")

        return top_n
    

    """
    This functions then takes the top n resorts from each of the three ranked lists, and uses
    weighted sum learning to construct the overall best bang-for-buck top n list
    @param run_count_weight: weight of feature 'number of runs'
    @param price_weight: weight of feature 'lift ticket price'
    @param elevation_weight: weight of feature 'peak elevation'
    @param n: the top n resorts based on user preference
    @return ranked list of resorts
    """
    def final_list(self, run_count_weight: float = 0.33, price_weight: float = 0.33, elevation_weight: float = 0.33, n: int = 10) -> pd.DataFrame:

        if not np.isclose(run_count_weight + price_weight + elevation_weight, 1.0):

            raise ValueError("Weights Do Not Add Up to 1, This is an Error...")
        
        if any(w < 0 for w in [run_count_weight, price_weight, elevation_weight]):

            raise ValueError("Weights Found to be Negative, This is an Error...")
        
        run_ranking = self.sorting_by_run_count()
        price_ranking = self.sorting_by_price()
        elevation_ranking = self.sorting_by_elevation()

        top_n_runs = self.return_ranking(run_ranking, n)
        top_n_prices = self.return_ranking(price_ranking, n)
        top_n_elevation = self.return_ranking(elevation_ranking, n)

        compute_final_ranking = pd.concat([top_n_runs, top_n_prices, top_n_elevation])
        compute_final_ranking = compute_final_ranking.drop_duplicates(subset='Resort ID')

        compute_final_ranking['Scores'] = (

            run_count_weight * (compute_final_ranking['Run Count Ranking'].max() - compute_final_ranking['Run Count Ranking'] + 1) / compute_final_ranking['Run Count Ranking'].max() +
            price_weight * (compute_final_ranking['Price Ranking'].max() - compute_final_ranking['Price Ranking'] + 1) / compute_final_ranking['Price Ranking'].max() +
            elevation_weight * (compute_final_ranking['Price Ranking'].max() - compute_final_ranking['Elevation Ranking'] + 1) / compute_final_ranking['Elevation Ranking'].max()

        )

        final_ranking = compute_final_ranking.sort_values('Scores', ascending=False).reset_index(drop=True)
        final_ranking['Final List', 'Resort ID', 'Resort', 'Country', 'Country', 'Run Count', 'Price (USD)', 'Peak Elevation (m)', 'Scores']

        print(f"Final Ranked List of Top {len(final_ranking)} Resorts Constructed!")
        
        return final_ranking
