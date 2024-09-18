import asyncio
from aiohttp import ClientResponseError
from loguru import logger
from web3 import Web3
import random
from concurrent.futures import ThreadPoolExecutor

from utils.config import RPC
from settings import DECIMALS


class BalanceChecker:
    def __init__(self, address: str, max_threads: int = None):
        self.chains = ['ethereum', 'zksync', 'arbitrum', 'optimism', 'scroll', 'base']
        self.address = address
        self.executor = ThreadPoolExecutor(max_workers=max_threads or len(self.chains)) 

    async def run_checker(self):
        try:
            loop = asyncio.get_event_loop()

            tasks = [
                loop.run_in_executor(self.executor, self.check_balance, chain)
                for chain in self.chains
            ]

            balances = await asyncio.gather(*tasks)
            
            sum_balances = sum(balances)
            chain_balances = dict(zip(self.chains, balances))
            
            logger.info(f'{self.address} | Balance: {sum_balances} ETH.')
            
            return chain_balances

        except Exception as e:
            logger.error(f'{self.address} | Unexpected error: {e}')
    
    def check_balance(self, chain):
        w3 = Web3(Web3.HTTPProvider(random.choice(RPC[chain]['rpc'])))

        try:
            wei_balance = w3.eth.get_balance(w3.to_checksum_address(self.address))
        except ClientResponseError:
            logger.error('Too many requests. Sleep 5 sec.')
            asyncio.sleep(5) 
            return self.check_balance(chain)

        eth_balance = round(w3.from_wei(wei_balance, 'ether'), DECIMALS)

        return eth_balance
