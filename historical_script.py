import pandas as pd
import json
from helpers import *

def is_latest(historical_df):
    curr_epoch = get_epoch_num()
    if historical_df[historical_df['epoch_num'] == curr_epoch-2].iloc[0]['completed'] == 1:
        return True
    print("Is Not Latest")
    return False

def load_files():
    base_dir_path = os.path.dirname(os.path.realpath(__file__))
    df = pd.read_csv(f'{base_dir_path}/data/aptos_historical.csv')
    RELEVANT_VALIDATORS = json.load(open(f'{base_dir_path}/RELEVANT_VALIDATORS.json', 'r'))
    return df, RELEVANT_VALIDATORS

def save_historical_df(historical_df):
    base_dir_path = os.path.dirname(os.path.realpath(__file__))
    historical_df.to_csv(f'{base_dir_path}/data/aptos_historical.csv', index=False)

def main():
    df, all_validators = load_files()
    if is_latest(df):
        return
    curr_epoch = get_epoch_num()
    print("curr_epoch:", curr_epoch)
    chain_params = get_chain_params()

    new_row = {}
    new_row['epoch_num'] = curr_epoch
    new_row['completed'] = 0

    for i in chain_params.keys():
        new_row[i] = chain_params[i]

    for validator in all_validators:
        stake = get_validator_stake(validator['address'])
        new_row[f'val_{validator["index"]}_stake'] = stake

        rewards = get_validator_rewards(validator['address'])
        df.loc[df['epoch_num'] == curr_epoch-2, f'val_{validator["index"]}_reward'] = rewards[curr_epoch-2]

        print('validator', validator['index'], ' done')

    df.loc[df['epoch_num'] == curr_epoch-2, 'completed'] = 1
    df = pd.concat([df, pd.DataFrame(new_row, index=[0])],ignore_index=True)
    df.sort_values(by='epoch_num', ascending=True)
    save_historical_df(df)

if __name__ == '__main__':
    print("Hello world")
    main()