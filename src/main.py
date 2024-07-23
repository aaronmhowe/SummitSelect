from process_data import PreProcessing
from ranking_data import RankingSkiResorts
from weighted_sum import WeightedSumModel
import pandas as pd
import argparse
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

"""
Main Application Class
@author Aaron Howe
@version Python 3.10.12
"""
class SummitSelect_Main:

    """
    Constructor
    @param run_count_data: Path to data for the number of runs per resort
    @param price_data: Path to data for the price of a lift ticket per resort
    @param elevation_data: Path to data for the peak elevation (in meters) per resort
    """
    def __init__(self, run_count_data: str, price_data: str, elevation_data: str):

        self.run_count_data = run_count_data
        self.price_data = price_data
        self.elevation_data = elevation_data

        self.preprocessor = PreProcessing(run_count_data, price_data, elevation_data)

        self.data = None
        self.rank = None
        self.weighted_model = None
        
        self.processed_data = None
        self.rankings = {}
        self.final_ranking = None
    

    """
    Data processing function, reading the data, loading it into memory, performing organization methods,
    merging the three key features into one dataset, normalization, and validation.
    @return the data pre-processed
    @raise: Exception: Errors during pre-processing
    """
    def process_data(self) -> pd.DataFrame:

        try:

            print("Processing Data...")
            self.processed_data = self.preprocessor.pre_process_data()
            self.data = self.processed_data
            print("Data Successfully Processed!")

            self.rank = RankingSkiResorts(self.processed_data)
            self.weighted_model = WeightedSumModel(self.processed_data)

            return self.processed_data
        
        except Exception as e:

            print(f"Ran into an Error: Problem occurred while processing the data... {str(e)}")
            raise
    

    """
    Developing the ranked list of each key feature from the input data
    @param data: Input data post-processing
    @return the ranked list (dictionary)
    @raise: ValueError: An error indicating the 'rank' object hasn't been initialized properly, or at all
    @raise: Exception: Errors while ranking the input data
    """
    def create_rankings(self, data: pd.DataFrame) -> dict:

        if self.rank is None:
            
            raise ValueError("The ranking object has not been initialized properly, or at all. Has the data been processed?")
        
        try:

            print("Developing Ranked Data...")

            self.rankings = {
                'runs': self.rank.sorting_by_run_count(),
                'price': self.rank.sorting_by_price(),
                'elevation': self.rank.sorting_by_elevation()
            }

            print("Rankings Finished!")

            for criterion, ranking in self.rankings.items():
                print(f"\nTop Five Resorts, Sorted by {criterion}:")
                print(ranking.head().to_string(index=False))

            return self.rankings
        
        except Exception as e:

            print(f"Ran into an Error: Problem occurred while developing the ranked data... {str(e)}")
            raise
    

    """
    Develops the final overall ranking of top-n ski resorts based on the computed results of the
    weighted sum model on the rankings of the three key features, based on user preference.
    @param rankings: The dictionary that holds the ranked data for each feature
    @return The overall ranked list of ski resorts
    @raise ValueError: An error indicating that the object reference of the WeightedSumModel has not
                       been initialized
    @raise Exception: Errors while developing the overall ranking
    """
    def create_final_ranking(self, run_pref: bool, price_pref: bool, elevation_pref: bool) -> pd.DataFrame:

        if self.weighted_model is None:
            raise ValueError("The Class 'WeightedSumModel' Has Not Been Properly Initialized...")
        
        try:
            # retrieving the user's selected preferences
            print("\nCurating a list of resorts...")
            self.weighted_model.set_preferences(run_pref, price_pref, elevation_pref)
            self.weighted_model.normalize_data()
            self.weighted_model.weighted_sum_model()

            self.final_ranking = self.weighted_model.ranking()

            print("\nFinal List Successfully Developed!")
            print("\nTop 10 Resorts:")
            print(self.weighted_model.return_ranking(10).to_string(index=False))

            return self.final_ranking
        
        except Exception as e:

            print(f"Ran into an Error: Problem occurred while developing the final list of ranked data... {str(e)}")
            raise


    """
    Dumping the final list into an output text file for the user to view and save their results
    @param rankings: The dictionary that holds the rankings of each feature
    @param final_ranking: The dictionary that holds the final list of ranked ski resorts
    @param output_file: The variable holder for the output file to dump the results into
    @raise Exception: Errors while writing to a file
    """
    def dump_output(self, rankings: dict, final_ranking: pd.DataFrame, output_file: str) -> None:

        try:

            print(f"\nDumping Output into {output_file}...")

            with open(output_file, 'w') as f:

                f.write("SummitSelect: List of Recommended Ski Resorts\n")
                f.write("=" * 40 + "\n\n")

                f.write("Final List:\n")
                f.write("-" * 40 + "\n")

                for _, resort in final_ranking.iterrows():
                    f.write(f"{int(resort['Rank'])} Rank: {resort['Resort']}\n")
                    f.write(f" Run Count: {resort['Run Count']}\n")
                    f.write(f" Price (USD): ${resort['Price (USD)']:.2f}\n")
                    f.write(f" Peak Elevation (m): {int(resort['Peak Elevation (m)'])}\n")
                    f.write(f" Total Score: {resort['Total Weighted Score']:.4f}\n\n")

                f.write("\nHow Each Feature Ranks Based on Your Preferences:\n")
                f.write("-" * 40 + "\n")

                for criterion, ranking in rankings.items():
                    f.write(f"\nTop 10 Resorts By {criterion.capitalize()}:\n")

                    for i, (_, resort) in enumerate(ranking.head(10).iterrows(), 1):
                        f.write(f"{i}. {resort['Resort']} - ")

                        if criterion == 'runs':
                            f.write(f"{int(resort['Run Count'])} runs\n")
                        elif criterion == 'price':
                            f.write(f"${resort['Price (USD)']:.2f}\n")
                        elif criterion == 'elevation':
                            f.write(f"{int(resort['Peak Elevation (m)'])} meters\n")

            print(f"Houston, we have output in {output_file}...")

        except Exception as e:

            print(f"Ran into an Error: Problem occurred while writing to the output file...{str(e)}")
            raise
    

    """
    This function executes the main application function, processing the data, developing the lists,
    curating a final list, and dumping the output into the results text file.
    @raise ValueError: Error indicating there's an issue with the input data.
    @raise FileNotFoundError: Error indicating there's an input file missing.
    @raise Exception: Errors when executing the list development from the input data.
    """
    def run(self, output_file):

        try:

            print("Thank you for Choosing SummitSelect.")
            print("As I'm sure you're already aware, this application will help you pick out your best bang-for-buck ski resort.")
            print("We analyze data for the number of runs, price per lift ticket, and peak elevation from 100 different resorts across North America.")
            print("We will now curate your list...")

            processed_data = self.process_data()
            print("Processing Step Complete.\n")

            print("Please Specify Your Preferences: ")
            run_count_preference = input("Are you looking for a resort with a higher number of runs? (Yes/No): ").lower() == 'yes'
            price_preference = input("Are you looking for cheaper lift ticket prices? (Yes/No): ").lower() == 'yes'
            elevation_preference = input("Are you looking for a resort with a higher peak elevation? (Yes/No): ").lower() == 'yes'

            print("Now ranking each feature based on your preferences...")
            rankings = self.create_rankings(processed_data)
            print("Rankings Developed.\n")

            print("Now developing a ranked list of resorts curated to your preferences...")
            final_ranking = self.create_final_ranking(run_count_preference, price_preference, elevation_preference)
            print("List Created Successfully.\n")

            print("Sending your list to the output folder...")
            
            try:
                self.dump_output(rankings, final_ranking, output_file)
            except Exception as e:
                print(f"Ran into an Error: Problem occurred writing to the output file... {str(e)}")
                print("Execution Will Continue.")

            print(f"\nSee '{output_file}' for your curated list.")

        except ValueError as ve:

            print(f"\nRan into an Error: Problem occurred involving the input data... {str(ve)}")
            print("Double check that the input files contain data...")

        except FileNotFoundError as fnf:

            print(f"\nRan into an Error: Could not find file {str(fnf)}")
            print(f"Ensure the necessary input files exist...")

        except Exception as e:

            print(f"\nRan into an Error: Proble occurred during developing stage... {str(e)}")

        finally:

            print("\nI hope this program has helped you in finding your dream resort. If you're going to shred, shred hard, but be safe!.")                
    

"""
Functiong for parsing command-line arguments
@return parsed arguments
"""
def add_args():

    parsing_helper = argparse.ArgumentParser(description="SummitSelect: Find Your Dream Resort!")

    parsing_helper.add_argument('--run_count_data', type=str, required=True, help="Path to Run Count Data For Each Resort.")
    parsing_helper.add_argument('--price_data', type=str, required=True, help="Path to Price Data For Each Resort.")
    parsing_helper.add_argument('--elevation_data', type=str, required=True, help="Path to Peak Elevation Data for Each Resort.")
    parsing_helper.add_argument('--output', type=str, default='Ski_Resort_Results.txt', help="Path to the Output File.")

    args = parsing_helper.parse_args()

    return args


"""
Main Application Function
@raise KeyboardInterrupt: User ended the program, whether intentional or not
@raise Exception: Errors with the application as a whole, can be very broad
"""
def main():

    try:
        args = add_args()
        app = SummitSelect_Main(args.run_count_data, args.price_data, args.elevation_data)
        app.run(args.output)

    except KeyboardInterrupt:
        print("\nUser Ended Program Functions. Program Will Now Exit.")
        sys.exit(1)

    except Exception as e:
        print("\nRan into an Error: Problem occurred during program execution. Please see error code for details.")
        print(f"Error Code: {str(e)}")
        print(f"Program Will Now Exit.")
        sys.exit(1)


if __name__ == "__main__":
    main()
