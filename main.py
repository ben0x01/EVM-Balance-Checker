async def run_main():
    address_list = get_address_list()  # Get the list of addresses to check

    tasks = []

    # Loop through each address and create a BalanceChecker instance
    for address in address_list:
        balance_checker = BalanceChecker(address)
        tasks.append(asyncio.create_task(balance_checker.run_checker()))

    # Await all balance checks
    balances = await asyncio.gather(*tasks)

    # Setup the final results to be written (presumably to an Excel file)
    setup_balances_to_write(balances)

    logger.success(f'All balances have been successfully written to wallets.xlsx!')


# Add logging to file and run the main function
logger.add('logs.log')
asyncio.run(run_main())
