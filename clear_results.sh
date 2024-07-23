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
}

# Function to clear all PNG files in the RESULTS/
delete_all_generated_png_files_in_RESULTS() {
    local current_dir=$(pwd)
    rm -f "$current_dir"/RESULTS/PYRAMIDS/*.png
    rm -f "$current_dir"/RESULTS/COMBINED_DISTRIBUTIONS/*.png
}

execute_with_confirmation "delete_all_generated_csv_files_in_DATA"
execute_with_confirmation "delete_all_generated_png_files_in_RESULTS"