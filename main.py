import asyncio

from loguru import logger

from modules.checker_module import BalanceChecker 
from utils.utils import get_address_list, setup_balances_to_write

async def run_main(max_threads: int = None):
    address_list = get_address_list()  

    tasks = []

    for address in address_list:
        balance_checker = BalanceChecker(address, max_threads=max_threads)
        tasks.append(asyncio.create_task(balance_checker.run_checker()))

    balances = await asyncio.gather(*tasks)

    setup_balances_to_write(balances, address_list)

    logger.success(f'All balances have been successfully written to wallet_balances.txt!')


logger.add('logs.log')

NUMBER_OF_THREADS = 15

asyncio.run(run_main(max_threads=NUMBER_OF_THREADS))
