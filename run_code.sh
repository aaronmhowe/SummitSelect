#!/bin/bash

PYTHON_PATH="/usr/bin/python3"
MAIN="/home/eriksai/Projects/PythonProjects/SummitSelect/src/main.py"
RUN_COUNT_DATA="data-sets/resorts_runs.csv"
PRICE_DATA="data-sets/resorts_prices.csv"
ELEVATION_DATA="data-sets/resorts_elevation.csv"
OUTPUT_FILE="output/Ski_Resorts_Results.txt"

if [ "$#" -eq 3 ]; then

    RUN_COUNT_DATA="$1"
    PRICE_DATA="$2"
    ELEVATION_DATA="$3"

    if [ "$#" -eq 4 ]; then

        OUTPUT_FILE="$4"

    fi

elif [ "$3" -ne 0 ]; then

    echo "Usage: $0 [run_count_data price_data elevation_data [output_file]]"
    exit 1

fi

"$PYTHON_PATH" "$MAIN_SCRIPT" \
    --run_count_data "$RUN_COUNT_DATA" \
    --price_data "$PRICE_DATA" \
    --elevation_data "$ELEVATION_DATA" \
    --output "$OUTPUT_FILE"

if [ $? -eq 0 ]; then

    echo "Program Execution Complete. Results Dumped to $OUTPUT_FILE"

else

    echo "Ran into an Error: Problem occurred while executing the program..."

fi 