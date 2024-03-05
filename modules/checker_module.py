import asyncio
from aiohttp import ClientResponseError
from loguru import logger
from web3 import AsyncWeb3
import random

import random

from utils.config import RPC
from settings import DECIMALS, PROXY


class BalanceChecker:
    def __init__(self, address: str):
        self.chains = ['ethereum', 'zksync', 'arbitrum', 'optimism', 'scroll', 'base']
        self.address = address
    
    async def run_checker(self):
        try:
            tasks = [asyncio.create_task(self.check_balance(chain)) for chain in self.chains]

            balances = await asyncio.gather(*tasks)
            
            sum_balances = sum(balances)
            chain_balances = dict(zip(self.chains, balances))
            
            logger.info(f'{self.address} | Balance: {sum_balances} ETH.')
            
            return chain_balances

        except Exception as e:
            logger.error(f'{self.address} | Unexpected error: {e}')
    
    async def check_balance(self, chain):
        request_kwargs = {'proxy': f'http://{random.choice(PROXY)}'} if PROXY else {}
        w3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(random.choice(RPC[chain]['rpc'])), request_kwargs=request_kwargs)

        try:
            wei_balance = await w3.eth.get_balance(w3.to_checksum_address(self.address))
        except ClientResponseError:
            logger.error('Too many requests. Sleep 5 sec.')
            await asyncio.sleep(5)
            return await self.check_balance(chain)
        
        eth_balance = round(w3.from_wei(wei_balance, 'ether'), DECIMALS)

        return eth_balance