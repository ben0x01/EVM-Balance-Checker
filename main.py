import asyncio

from loguru import logger

from modules.checker_module import BalanceChecker 
from utils.utils import get_address_list, setup_balances_to_write

async def run_main(max_threads: int = None):
    address_list = get_address_list()  # Get the list of addresses to check

    tasks = []

    # Loop through each address and create a BalanceChecker instance
    for address in address_list:
        balance_checker = BalanceChecker(address, max_threads=max_threads)
        tasks.append(asyncio.create_task(balance_checker.run_checker()))

    # Await all balance checks
    balances = await asyncio.gather(*tasks)

    # Write the balances to the text file
    setup_balances_to_write(balances, address_list)

    logger.success(f'All balances have been successfully written to wallet_balances.txt!')


# Configure logging to file
logger.add('logs.log')

# Define the number of threads to use for balance checking
NUMBER_OF_THREADS = 15

# Run the main function
asyncio.run(run_main(max_threads=NUMBER_OF_THREADS))
