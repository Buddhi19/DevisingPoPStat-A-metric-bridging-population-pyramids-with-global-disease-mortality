import os
import sys
import pandas as pd

main_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(main_dir)


def EVAL(name: str = 'japan'):
    DATA_PATH = os.path.join(main_dir, f'RESULTS/CORRELATION_DATA_FOR_OTHER_DISEASES/Correlation_Coefficient_{name}.csv')
    data = pd.read_csv(DATA_PATH)
    count = 0
    for disease in data['Cause of Death'].unique():
        data_per_disease = data[data['Cause of Death'] == disease]
        if data_per_disease['r squared value'].max() == data_per_disease[data_per_disease['Parameter'] == 'POPSTAT_COVID19']['r squared value'].values[0]:
            print(f"{disease} is best fitted with POPSTAT with R squared value of {data_per_disease['r squared value'].max()}")
            count += 1
    print(f"Total {count} diseases are best fitted with POPSTAT")


if __name__ == '__main__':
    EVAL()