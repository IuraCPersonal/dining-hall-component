import threading
import statistics
from colorama import init, Fore, Back, Style


class Print:
    __lock = threading.Lock()

    @staticmethod
    def log(text):
        with Print.__lock:
            print(f'[{Fore.RED}DH{Style.RESET_ALL}] {text}')

    @staticmethod
    def order_made(table_id, order_id):
        with Print.__lock:
            print(f'[{Fore.RED}DH{Style.RESET_ALL}] TABLE ({Fore.YELLOW}{table_id}{Style.RESET_ALL}) has made ORDER ({Fore.BLUE}{order_id}{Style.RESET_ALL})')

    @staticmethod
    def took_order(waiter_id, order_id, table_id):
        with Print.__lock:
            print(f'[{Fore.RED}DH{Style.RESET_ALL}] WAITR ({Fore.MAGENTA}{waiter_id}{Style.RESET_ALL}) took ORDER ({Fore.BLUE}{order_id}{Style.RESET_ALL}) from TABLE ({Fore.YELLOW}{table_id}{Style.RESET_ALL})')

    @staticmethod
    def serve_order(waiter_id, order_id, table_id, order_stars):
        with Print.__lock:
            print(f'[{Fore.RED}DH{Style.RESET_ALL}] WAITR ({Fore.MAGENTA}{waiter_id}{Style.RESET_ALL}) served ORDER ({Fore.BLUE}{order_id}{Style.RESET_ALL}) to TABLE ({Fore.YELLOW}{table_id}{Style.RESET_ALL}) | REVIEW: {Fore.MAGENTA}{order_stars} ⭐{Style.RESET_ALL}')

    @staticmethod
    def reputation(reputation_system):
        with Print.__lock:
            print(f'[{Fore.RED}DH{Style.RESET_ALL}] {Fore.LIGHTRED_EX}REPUTATION: {statistics.mean(reputation_system)}⭐{Style.RESET_ALL}')
