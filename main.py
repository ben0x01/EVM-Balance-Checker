from modules.checker_module import BalanceChecker 
from utils.utils import get_address_list, setup_balances_to_write

async def run_main():
    address_list = get_address_list() 

    tasks = []

    for address in address_list:
        balance_checker = BalanceChecker(address)
        tasks.append(asyncio.create_task(balance_checker.run_checker()))

    balances = await asyncio.gather(*tasks)

    setup_balances_to_write(balances)

    logger.success(f'All balances have been successfully written to wallets.xlsx!')


# Add logging to file and run the main function
logger.add('logs.log')
asyncio.run(run_main())
