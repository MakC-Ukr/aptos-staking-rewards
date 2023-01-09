import requests
import os

headers = {'Content-Type': 'application/json'}
RPC_URL="https://fullnode.mainnet.aptoslabs.com/v1"

TEMP_ADDR = "0xee49776eff9fd395eb90d601449542080645e63704f518b31c6f72b6a95d7868"


def get_validator_rewards(account_addr, epoch_number=-1):
    """Returns a dicitonary of epoch-reward for the past 25 epochs"""
    response = requests.get(f'{RPC_URL}/accounts/{account_addr}/events/0x1::stake::StakePool/distribute_rewards_events',headers=headers).json()
    res = {}
    for sequence in response:
        res[int(sequence['sequence_number'])] = float(sequence['data']['rewards_amount'])/1e8
    if epoch_number != -1:
        return res[str(epoch_number)]
    return res

def get_validator_stake(account_addr):
    """Returns the active stake for a validator"""
    response = requests.get(f'{RPC_URL}/accounts/{account_addr}/resources',headers=headers).json()
    stake = float(response[0]['data']['active']['value'])
    return stake/1e8

def get_epoch_num():
    response = requests.get('https://fullnode.mainnet.aptoslabs.com/v1/', headers=headers).json()
    epoch_num = int(response['epoch'])
    return epoch_num

def get_chain_params():
    res = {}
    res['EPOCHS_PER_YEAR'] = 4380
    res['SECONDS_PER_EPOCH'] = 7200
    res['MAX_REWARD_RATE'] = 0.0700
    res['MIN_REWARD_RATE'] = 0.0325
    res['DISINFLATION_RATE'] = 0.015
    return res