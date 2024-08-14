import os
import sys
import numpy as np
import pandas as pd

main_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(main_dir)

from ANALYSIS.COUNTRIES import mapping_name
from ANALYSIS.Pop_Stat_Calculation import POP_STAT_CALCULATION
from ANALYSIS.Population_Data_For_Date import POPULATION_DATA_FOR_DATE


DEATH_DATA = pd.read_csv(os.path.join(main_dir,"DATA/death_data/deaths_by_cause.csv"), low_memory=False)

POPULATION_DIR = os.path.join(main_dir, 'DATA/population_data_by_country')
RESULTS_DIR = os.path.join(main_dir, 'RESULTS/POPSTAT_OTHER_DISEASES')

class POP_STAT_CALCULATION_FOR_OTHER_DISEASES(POP_STAT_CALCULATION):
    def __init__(self, disease, year):
        POPULATION_DATA_FOR_DATE(year)
        super().__init__()
        self.CONSIDERING_COUNTRIES = 4
        self.disease = disease
        self.disease_data = {}
        self.DEATH_DATA = DEATH_DATA[DEATH_DATA['Causes name'] == disease]
        self.DEATH_DATA = self.DEATH_DATA[self.DEATH_DATA['Year'] == year]

        for country in self.DEATH_DATA['Entity'].unique():
            pre_name = country
            country = mapping_name(country)
            if country is None:
                continue
            death_data_per_country = self.DEATH_DATA[self.DEATH_DATA['Entity'] == pre_name]
            total_deaths = death_data_per_country["Death Numbers"].values[0]
            pop_data = pd.read_csv(os.path.join(POPULATION_DIR, f'{country}_population.csv'))
            total_population = pop_data['total'].sum()
            total_deaths_per_million = total_deaths/total_population
            print(total_deaths_per_million)
            self.disease_data[country] = total_deaths_per_million

        self.common_countries = set(self.population_data.keys() & self.disease_data.keys())

    def remove_nan_values(self):
        NAN_COUNTRIES = []
        for country, dist in self.population_data.items():
            if not np.isfinite(dist).all():
                NAN_COUNTRIES.append(country)
                print(f"Warning: Non-finite values found in population data for {country}")
        
        for country, value in self.disease_data.items():
            if not np.isfinite(value):
                NAN_COUNTRIES.append(country)
                print(f"Warning: Non-finite value found in {self.disease} data for {country}")

        if NAN_COUNTRIES:
            self.population_data = {country: dist for country, dist in self.population_data.items() if country not in NAN_COUNTRIES}
            self.disease_data = {country: value for country, value in self.disease_data.items() if country not in NAN_COUNTRIES}
    
    def run(self):
        self.remove_nan_values()
        self.progressive_reference_countries, self.regressive_reference_countries = self.find_optimal_reference()
        self.progressive_reference_countries = self.progressive_reference_countries[:self.CONSIDERING_COUNTRIES]
        self.regressive_reference_countries = self.regressive_reference_countries[:self.CONSIDERING_COUNTRIES]
        for country, correlation in self.progressive_reference_countries:
            self.create_POPSTAT_DISEASE_data(country)
        for country, correlation in self.regressive_reference_countries:
            self.create_POPSTAT_DISEASE_data(country)
        return self.progressive_reference_countries, self.regressive_reference_countries

    def create_POPSTAT_DISEASE_data(self, reference_country):
        data = self.POPSTAT_DISEASE(reference_country)
        data = pd.DataFrame(data.items(), columns = ['Country', f'POPSTAT_{self.disease}'])
        try:
            data.to_csv(os.path.join(RESULTS_DIR, f'{self.disease}/{reference_country}_POPSTAT_{self.disease}.csv'), index = False)
        except:
            os.mkdir(os.path.join(RESULTS_DIR, self.disease))
            data.to_csv(os.path.join(RESULTS_DIR, f'{self.disease}/{reference_country}_POPSTAT_{self.disease}.csv'), index = False)
        
        print(f"POPSTAT_{self.disease} data saved successfully for {reference_country}")

    def POPSTAT_DISEASE(self, reference_country):
        return super().POPSTAT_COVID19(reference_country)
    
    def find_optimal_reference(self):
        country_correlations = {}

        common_countries = set(self.population_data.keys()) & set(self.disease_data.keys())

        for reference_country in common_countries:
            distances = self.POPSTAT_DISEASE(reference_country)

            common_distances = [distances[country] for country in common_countries]
            common_disease_data = [self.disease_data[country] for country in common_countries]

            correlation = np.corrcoef(common_distances, common_disease_data)[0, 1]
            country_correlations[reference_country] = correlation

        country_correlations = sorted(country_correlations.items(), key = lambda x: abs(x[1]), reverse = True)
        country_correlations_progressive = sorted(country_correlations, key = lambda x: x[1], reverse = True)
        country_correlations_regressive = sorted(country_correlations, key = lambda x: x[1], reverse = False)

        print(f"Top {self.CONSIDERING_COUNTRIES} countries with highest correlation with progressive population distribution")
        for country, correlation in country_correlations_progressive[:self.CONSIDERING_COUNTRIES]:
            print(f"{country}: {correlation}")

        print()

        print(f"Top {self.CONSIDERING_COUNTRIES} countries with highest correlation with regressive population distribution")
        for country, correlation in country_correlations_regressive[:self.CONSIDERING_COUNTRIES]:
            print(f"{country}: {correlation}")

        return country_correlations_progressive, country_correlations_regressive


if __name__ == "__main__":
    disease = 'Meningitis'
    year = 2017
    POP_STAT_CALCULATION_FOR_OTHER_DISEASES(disease, year).run()