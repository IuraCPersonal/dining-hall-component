import threading, statistics
from colorama import init, Fore, Back, Style


class SafePrint:
    __lock = threading.Lock()
    __green = '\033[32m'
    __lightgreen = '\033[92m'
    __blue = '\033[34m'
    __red = '\033[31m'
    __pink = '\033[95m'
    __yellow = '\033[93m'

    # @staticmethod
    # def log(text):
    #     with SafePrint.__lock:
    #         print(f' DH : {SafePrint.__lightgreen}{text}')

    @staticmethod
    def log(text):
        with SafePrint.__lock:
            print(f'[{Fore.RED}DH{Style.RESET_ALL}] {text}')

    @staticmethod
    def order_made(table_id, order_id):
        with SafePrint.__lock:
            print(f'[{Fore.RED}DH{Style.RESET_ALL}] TABLE ({Fore.YELLOW}{table_id}{Style.RESET_ALL}) has made ORDER ({Fore.BLUE}{order_id}{Style.RESET_ALL})')

    @staticmethod
    def took_order(waiter_id, order_id, table_id):
        with SafePrint.__lock:
            print(f'[{Fore.RED}DH{Style.RESET_ALL}] WAITR ({Fore.MAGENTA}{waiter_id}{Style.RESET_ALL}) took ORDER ({Fore.BLUE}{order_id}{Style.RESET_ALL}) from TABLE ({Fore.YELLOW}{table_id}{Style.RESET_ALL})')

    @staticmethod
    def serve_order(waiter_id, order_id, table_id, order_stars):
        with SafePrint.__lock:
            print(f'[{Fore.RED}DH{Style.RESET_ALL}] WAITR ({Fore.MAGENTA}{waiter_id}{Style.RESET_ALL}) served ORDER ({Fore.BLUE}{order_id}{Style.RESET_ALL}) to TABLE ({Fore.YELLOW}{table_id}{Style.RESET_ALL}) | REVIEW: {Fore.MAGENTA}{order_stars} ⭐{Style.RESET_ALL}')

    @staticmethod
    def reputation(reputation_system):
        with SafePrint.__lock:
            print(f'[{Fore.RED}DH{Style.RESET_ALL}] {Fore.LIGHTRED_EX}REPUTATION: {statistics.mean(reputation_system)}⭐{Style.RESET_ALL}')