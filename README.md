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
4. Alternatively, in your terminal, cd into /src (`cd path/to/file/SummitSelect/src`), and then type and enter `python3 FortuneCookieClassifier.py`, allow the program to complete execution, then type and enter `python3 OCR_MutliClassifier.py`. This does the exact same thing as the shell script.
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
### Argument Parsing in Python Usig argparse
https://www.geeksforgeeks.org/command-line-option-and-argument-parsing-using-argparse-in-python/
https://www.youtube.com/watch?v=88pl8TuuKz0&ab_channel=NeuralNine 
# Project Report
Report coming soon, containing a more in-depth project overview, why I chose to pursue the project,
algorithm analysis, and more...
