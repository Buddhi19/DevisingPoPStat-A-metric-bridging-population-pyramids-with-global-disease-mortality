#!/bin/bash

# Function to execute commands with confirmation
execute_with_confirmation() {
    local command=$1
    read -p "Do you want to execute the command: $command (y/n)? " choice
    if [[ "$choice" = "y" || "$choice" = "Y" ]]; then
        echo "Executing command: $command"
        eval $command
        echo "Command executed successfully"
    else
        echo "Command not executed"
    fi
}

# Function to clear all csv files in the DATA/
delete_all_generated_csv_files_in_DATA() {
    local current_dir=$(pwd)
    rm -f "$current_dir"/DATA/covid_data_by_country/*.csv
    rm -f "$current_dir"/DATA/population_data_by_country/*.csv
    rm -f "$current_dir"/RESULTS/CORRELATION_DATA_FOR_OTHER_DISEASES/*.csv
}

# Function to clear all PNG files in the RESULTS/
delete_all_generated_png_files_in_RESULTS() {
    local current_dir=$(pwd)
    rm -f "$current_dir"/RESULTS/PYRAMIDS/*.png
    rm -f "$current_dir"/RESULTS/COMBINED_DISTRIBUTIONS/*.png
    rm -f "$current_dir"/RESULTS/CORRELATION_WITH_OTHER_DISEASES/*.png
    rm -f "$current_dir"/RESULTS/POPSTATCOVID/PLOTS/PROGRESSIVE/cases/*.png
    rm -f "$current_dir"/RESULTS/POPSTATCOVID/PLOTS/PROGRESSIVE/deaths/*.png
    rm -f "$current_dir"/RESULTS/POPSTATCOVID/PLOTS/REGRESSIVE/cases/*.png
    rm -f "$current_dir"/RESULTS/POPSTATCOVID/PLOTS/REGRESSIVE/deaths/*.png
}

delete_all_generated_csv_files_in_RESULTS() {
    local current_dir=$(pwd)
    rm -f "$current_dir"/RESULTS/POPSTAT_COUNTRY_DATA/*.csv
}

execute_with_confirmation "delete_all_generated_csv_files_in_DATA"
execute_with_confirmation "delete_all_generated_png_files_in_RESULTS"
execute_with_confirmation "delete_all_generated_csv_files_in_RESULTS"