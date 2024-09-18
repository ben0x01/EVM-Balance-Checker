def get_address_list() -> list:
    with open('wallets.txt', 'r') as f:
        wallet_list = [line.strip() for line in f.readlines() if line.strip()]

    return wallet_list

def format_balances(address: str, balances: dict) -> str:
    formatted_balances = ', '.join([f'{network}:{balance}' for network, balance in balances.items()])
    return f'{address} - {formatted_balances}'

def setup_balances_to_write(all_balances: list, address_list: list):
    with open('wallet_balances.txt', 'w') as f:
        for address, balances in zip(address_list, all_balances):
            formatted_line = format_balances(address, balances)
            f.write(formatted_line + '\n')
