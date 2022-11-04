from web3 import Web3
import csv
import os

# Helper function to retrieve eth name from a string
# Is called only when str contains '.eth'
def get_eth_name(str):
    cur_word = ""
    for element in str:
        if element == ' ':
            cur_word = ""
        else:
            cur_word = cur_word + element
            if cur_word.endswith('.eth'):
                return cur_word
    
# Input: valid eth_name
# Output: wallet address of user 'eth_name'
def get_wallet_address_from_eth_name(eth_name):
    w3 = Web3(Web3.HTTPProvider(os.environ.get('infura_node')))
    eth_address = w3.ens.address(name=eth_name)
    return eth_address

def get_wallet_address_from_user(user_details):
    name = user_details[1]
    bio = user_details[5]

    if('.eth' not in name and '.eth' not in bio):
        wallet_address = 'None'
    elif('.eth' in name):
        eth_name = get_eth_name(name)
        wallet_address = get_wallet_address_from_eth_name(eth_name)
    else:
        eth_name = get_eth_name(bio)
        wallet_address = get_wallet_address_from_eth_name(eth_name)
    
    return wallet_address
        

