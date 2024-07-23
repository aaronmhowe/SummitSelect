# Choosing the Best Ski Resort
This project functions to help mountain jockies (such as myself) choose the North American ski resort that's right for them.
Whether they're looking to save the most money, find the mountain with the highest number of trails to explore, or
find the mountain with the highest elevation (thus, the best snow), this program can help you find that hidden gem.
## Instructions for Running this Program
1. Install Python 3
    - This program's interpreter is Python 3+, I am using Python 3.10.12, you can download and install Python 3 from this [link](https://www.python.org/downloads/source/).
        - Note: That link takes you to the Python 3 release page for Linux/UNIX Operating Systems. I highly recommend this program is ran on such system.
2. Install PIP: PIP is required for this program.
    - Windows Installation Guide:
        1. On your system search, search for Windows Powershell, Git Bash, or CMD. Right-click the result and click 'Run as Administrator'
        2. type and enter this command:
            `curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py`
            PIP should download to your system.
        3. To install, enter this command:
            `python get-pip.py`
        4. Verify PIP installed by entering:
            `python -m pip help`
            Entering this command should display the location on your system of where PIP is installed
        5. Add a PATH variable for PIP
            1. Open the Windows Search, and type and enter "Environment Variables"
            2. System Properties should open, at the bottom of the window, click "Environment Variables".
            3. This will open a list of environment variables, double-click 'Path', or single-click and then click 'Edit'
            4. Click 'New', and then add the directory of where PIP is installed on your system. This directory should've been displayed from entering into your commmand prompt: `python -m pip help`
            5. Click 'OK' and the changes should save.
        6. Open a clean CMD, Bash, or Powershell, then type and enter `pip help`. This should display the same location information from step 4. You might have to instead enter `pip3 help`. If you're having issues, it might be wise to add the directory where your Python3 installation is located to the same PATH variables from step 5.
    - Linux/UNIX Installation Guide:
        1. In your system terminal, type `wget https://bootstrap.pypa.io/get-pip.py`
            This will download the installer.
        2. Install PIP to your system by typing and entering: `python3 ./get-pip.py`
            PIP should now be installed.
### Unix/Linux Users Only
3. Configure the Shell Script.
    - The shell script located in `SummitSelect/src` will need a couple commands entered into the terminal before it will be an executable.
        1. CD into `/SummitSelect` (`cd path/to/file/SummitSelect`)
        2. Type and enter `chmod +x run_code.sh` and enter your password if/when prompted.
        3. run_code.sh should now be executable. Type and enter `./run_code.sh` to run the shell script.
        4. Additionally: You yourself *might* have to edit the shell script, depending on where in your system your python interpreter is located. If you must, you'll be editing line 3.
Important: Make sure you're in `./src` if you're going to run the `.py` files manually.
## Resources Used
### Original Dataset
https://www.kaggle.com/datasets/ulrikthygepedersen/ski-resorts/code
### North American Ski Resort Price Data:
https://www.onthesnow.com/north-america/lift-tickets
### Pandas
https://pandas.pydata.org/docs/user_guide/10min.html
### Data Pre-Processing
https://www.geeksforgeeks.org/data-preprocessing-machine-learning-python/# 
### Developing a Ranking System
https://www.stratascratch.com/blog/methods-for-ranking-in-pandas/ 
- Referenced Code From:
    https://github.com/Didayolo/ranky/blob/master/ranky/ranking.py 
### Weighted Sum Model
https://www.geeksforgeeks.org/weighted-sum-method-multi-criteria-decision-making/
https://www.youtube.com/watch?v=iAr4tGEYQZ0&ab_channel=HigherMathematicsLearning
https://www.youtube.com/watch?v=EGf9bUgl3R8&ab_channel=labmao 
### Merging Dataframes
https://pandas.pydata.org/docs/user_guide/merging.html
### Argument Parsing in Python Using argparse
https://www.geeksforgeeks.org/command-line-option-and-argument-parsing-using-argparse-in-python/
https://www.youtube.com/watch?v=88pl8TuuKz0&ab_channel=NeuralNine 
### Additional Aid
- I utilized generative AI to assist with debugging and researching topics.
# Project Report
    To re-iterate, this project serves to curate a list of top ski resorts tailored
to the preferences of the user.
### Data Mining Task
    The task of this project is to answer a series of questions about various ski 
resorts across North America, and curate a list, ranking these ski resorts tailored to the answered questions. The questions are as follows:

1. Which ski resorts contain the most runs?
2. Which ski resorts are the most affordable?
3. Which ski resorts have the highest elevation (and consequentially, the best snow)?

    Using the two datasets listed under 'Resources Used', and some tedious browsing 
on Google, I've compiled three separate datasets, each containing data for the same list of 100 ski resorts across the United States and Canada; run count, full-day adult lift ticket prices, and the peak elevation of the resort, respectively. The overall goal is to use the three datasets and the three listed questions to compile a list of ski resort recommendations, of which are the "best bang for your buck", or not, if you decide you want to find and attend the most expensive ski resort. Someone using this program could give the prompt that they want to find the ski resorts with the worst pricing, the least amount of runs, and the lowest elevation if they so please!
### Methodology
    In order to get the data ready for the main algorithm used in this program, the
weighted sum model, I need to perform rather intensive data preprocessing, followed by a ranking system for each key feature. To keep it brief, the data preprocessing, which is mostly done in `process_data.py`, normalizes the data before meging them into a new dataset. This new dataset is then used as input for the ranking functions in `ranking_data.py`. The ranking system of this project is designed to take in user input for the three questions listed under 'Data Mining Task', and *rank* the three unique criteria based on the users' responses. To be specific, the user is asked to give a basic 'yes' or 'no' response to each question. For example, a 'yes' to run count would rank Run Count from most to least runs per resort, a 'yes' to prices would rank Price (USD) from least expensive to most expensive lift tickets, and a 'yes' to elevation would rank Peak Elevation (m) from highest to lowest.

    Once the new input file is created, we come to the real meat and potatoes of this
program, the Weighted Sum Model, or also known as the Multi Criteria Decision Making Model. This model takes in multiple possible pieces of data that relate to a list of items, as we have in our dataset (run count, price, elevation) for each resort, and determines the best item based on the order of scoring for each criteria. The score for each criteria is used to compute a total overall score, and that is how, in this program, each resort is ranked in the final list that is written to the output file.

**Weighted Sum Model**
$$\left A_i^WSM-score \right = \left \sum_{j=1}^n w_j a_ij \right, \left for i = 1, 2, 3, ..., m \right$$
Where m represents the different features, and n is the decision criteria. $`w_j`$ denotes the weights and $`a_ij`$ denotes the performance value, which we substitute with the results of z-score normalization.
