import requests
import json
import os
import urllib.parse
from datetime import datetime
import time
from colorama import *
import pytz

wib = pytz.timezone('Asia/Jakarta')

class AllianceMicroNode:
    def __init__(self) -> None:
        self.session = requests.Session()
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'no-cache',
            'Host': 'api.micro-node.alliancegames.xyz',
            'Origin': 'https://micro-node.alliancegames.xyz',
            'Pragma': 'no-cache',
            'Referer': 'https://micro-node.alliancegames.xyz/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0'
        }

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def log(self, message):
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}{message}",
            flush=True
        )

    def welcome(self):
        print(
            f"""
        {Fore.GREEN + Style.BRIGHT}Auto Claim {Fore.BLUE + Style.BRIGHT}Alliance Micro Node - BOT
            """
            f"""
        {Fore.GREEN + Style.BRIGHT}Rey? {Fore.YELLOW + Style.BRIGHT}<INI WATERMARK>
            """
        )

    def format_seconds(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"

    def load_data(self, query: str):
        query_params = urllib.parse.parse_qs(query)
        user_param = query_params.get('user', [None])[0]
        hash = query_params.get('hash', [None])[0]

        if user_param:
            try:
                user_data_json = urllib.parse.unquote(user_param)
                user_data = json.loads(user_data_json)

                user_id_str = user_data.get('id')
                username = user_data.get('username')

                return hash, user_id_str, username

            except json.JSONDecodeError:
                raise ValueError("Failed to decode user data JSON.")
            except ValueError as ve:
                raise ve
        else:
            raise ValueError("User data not found in query.")

        
    def user_login(self, hash: str, query: str, user_id: str, username: str):
        url = 'https://api.micro-node.alliancegames.xyz/user'
        data = json.dumps({'hash':hash, 'initData':query, 'referralCode':'756A7N', 'tgId':int(user_id), 'username':username})
        self.headers.update({
            'Content-Type': 'application/json'
        })

        response = self.session.post(url, headers=self.headers, data=data)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    
    def user_info(self, hash: str, query: str, user_id: str):
        url = 'https://api.micro-node.alliancegames.xyz/user/info'
        data = json.dumps({'hash':hash, 'initData':query, 'tgId':int(user_id)})
        self.headers.update({
            'Content-Type': 'application/json'
        })

        response = self.session.post(url, headers=self.headers, data=data)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def open_clusterblocks(self, hash: str, query: str, user_id: str):
        url = 'https://api.micro-node.alliancegames.xyz/user/box'
        data = json.dumps({'hash':hash, 'initData':query, 'tgId':int(user_id)})
        self.headers.update({
            'Content-Type': 'application/json'
        })

        response = self.session.post(url, headers=self.headers, data=data)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def quest_lists(self, hash: str, query: str, user_id: str):
        url = 'https://api.micro-node.alliancegames.xyz/quest'
        data = json.dumps({'hash':hash, 'initData':query, 'tgId':int(user_id)})
        self.headers.update({
            'Content-Type': 'application/json'
        })

        response = self.session.post(url, headers=self.headers, data=data)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def start_quests(self, hash: str, query: str, user_id: str, quest_id: int):
        url = f'https://api.micro-node.alliancegames.xyz/quest/{quest_id}'
        data = json.dumps({'hash':hash, 'initData':query, 'tgId':int(user_id)})
        self.headers.update({
            'Content-Type': 'application/json'
        })

        response = self.session.post(url, headers=self.headers, data=data)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def claim_quests(self, hash: str, query: str, user_id: str, quest_id: int):
        url = f'https://api.micro-node.alliancegames.xyz/quest/{quest_id}'
        data = json.dumps({'hash':hash, 'initData':query, 'tgId':int(user_id)})
        self.headers.update({
            'Content-Type': 'application/json'
        })

        response = self.session.patch(url, headers=self.headers, data=data)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def hold_nodes(self, hash: str, query: str, ms: int, user_id: str):
        url = 'https://api.micro-node.alliancegames.xyz/user/tap'
        data = json.dumps({'hash':hash, 'initData':query, 'milliseconds':ms, 'tgId':int(user_id)})
        self.headers.update({
            'Content-Type': 'application/json'
        })

        response = self.session.post(url, headers=self.headers, data=data)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    
    def process_query(self, query: str):
        hash, user_id, username = self.load_data(query)
        self.user_login(hash, query, user_id, username)

        user = self.user_info(hash, query, user_id)
        if not user:
            self.log(
                f"{Fore.MAGENTA+Style.BRIGHT}[ Account{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {username} {Style.RESET_ALL}"
                f"{Fore.RED+Style.BRIGHT}Query ID Isn't Valid{Style.RESET_ALL}"
                f"{Fore.MAGENTA+Style.BRIGHT} ]{Style.RESET_ALL}"
            )
            return

        if user and user['status'] == 'success':
            self.log(
                f"{Fore.MAGENTA+Style.BRIGHT}[ Account{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {user['data']['username']} {Style.RESET_ALL}"
                f"{Fore.MAGENTA+Style.BRIGHT}] [ Balance{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {user['data']['points']} $mcWORK {Style.RESET_ALL}"
                f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {user['data']['usdt']} $USDT {Style.RESET_ALL}"
                f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
            )
            time.sleep(1)

            available_box = user['data']['boxQuantity']
            if available_box > 0:
                while available_box > 0:
                    open = self.open_clusterblocks(hash, query, user_id)
                    if open and open['status'] == 'success':
                        available_box -= 1
                        self.log(
                            f"{Fore.MAGENTA+Style.BRIGHT}[ Cluster Blocks{Style.RESET_ALL}"
                            f"{Fore.GREEN+Style.BRIGHT} Is Opened {Style.RESET_ALL}"
                            f"{Fore.MAGENTA+Style.BRIGHT}] [ Reward{Style.RESET_ALL}"
                            f"{Fore.WHITE+Style.BRIGHT} {open['data']['points']} $mcWORK {Style.RESET_ALL}"
                            f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                            f"{Fore.WHITE+Style.BRIGHT} {open['data']['usdt']} $USDT {Style.RESET_ALL}"
                            f"{Fore.MAGENTA+Style.BRIGHT}] [ Count{Style.RESET_ALL}"
                            f"{Fore.WHITE+Style.BRIGHT} {available_box} Left {Style.RESET_ALL}"
                            f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                        )
                    else:
                        break

                    time.sleep(2.5)

                if available_box == 0:
                    self.log(
                        f"{Fore.MAGENTA+Style.BRIGHT}[ Cluster Blocks{Style.RESET_ALL}"
                        f"{Fore.YELLOW+Style.BRIGHT} Not Available for Open {Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                    )
            else:
                self.log(
                    f"{Fore.MAGENTA+Style.BRIGHT}[ Cluster Blocks{Style.RESET_ALL}"
                    f"{Fore.YELLOW+Style.BRIGHT} Not Available for Open {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                )

            quests = self.quest_lists(hash, query, user_id)
            if quests and quests['status'] == 'success':
                for quest in quests['data']['quests']['mission']:
                    quest_id = str(quest['id'])
                    completed = quest['completed']
                    claimed = quest['claimed']

                    if quest and not completed and not claimed:
                        start = self.start_quests(hash, query, user_id, quest_id)
                        if start and start['status'] == 'success':
                            self.log(
                                f"{Fore.MAGENTA+Style.BRIGHT}[ Quets{Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT} {quest['name']} {Style.RESET_ALL}"
                                f"{Fore.GREEN+Style.BRIGHT}Is Started{Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT} ]{Style.RESET_ALL}"
                            )
                            time.sleep(1)

                            claim = self.claim_quests(hash, query, user_id, quest_id)
                            if claim and claim['status'] == 'success':
                                self.log(
                                    f"{Fore.MAGENTA+Style.BRIGHT}[ Quets{Style.RESET_ALL}"
                                    f"{Fore.WHITE+Style.BRIGHT} {quest['name']} {Style.RESET_ALL}"
                                    f"{Fore.GREEN+Style.BRIGHT}Is Claimed{Style.RESET_ALL}"
                                    f"{Fore.MAGENTA+Style.BRIGHT} ] [ Reward{Style.RESET_ALL}"
                                    f"{Fore.WHITE+Style.BRIGHT} {quest['points']} $mcWORK {Style.RESET_ALL}"
                                    f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                                    f"{Fore.WHITE+Style.BRIGHT} +{quest['booster']} Booster {Style.RESET_ALL}"
                                    f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                                )
                            else:
                                self.log(
                                    f"{Fore.MAGENTA+Style.BRIGHT}[ Quets{Style.RESET_ALL}"
                                    f"{Fore.WHITE+Style.BRIGHT} {quest['name']} {Style.RESET_ALL}"
                                    f"{Fore.RED+Style.BRIGHT}Isn't Claimed{Style.RESET_ALL}"
                                    f"{Fore.MAGENTA+Style.BRIGHT} ]{Style.RESET_ALL}"
                                )
                            time.sleep(1)

                        else:
                            self.log(
                                f"{Fore.MAGENTA+Style.BRIGHT}[ Quets{Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT} {quest['name']} {Style.RESET_ALL}"
                                f"{Fore.RED+Style.BRIGHT}Isn't Started{Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT} ]{Style.RESET_ALL}"
                            )

                    elif quest and completed and not claimed:
                        claim = self.claim_quests(hash, query, user_id, quest_id)
                        if claim and claim['status'] == 'success':
                            self.log(
                                f"{Fore.MAGENTA+Style.BRIGHT}[ Quets{Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT} {quest['name']} {Style.RESET_ALL}"
                                f"{Fore.GREEN+Style.BRIGHT}Is Claimed{Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT} ] [ Reward{Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT} {quest['points']} $mcWORK {Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT} +{quest['booster']} Booster {Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                            )
                        else:
                            self.log(
                                f"{Fore.MAGENTA+Style.BRIGHT}[ Quets{Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT} {quest['name']} {Style.RESET_ALL}"
                                f"{Fore.RED+Style.BRIGHT}Isn't Claimed{Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT} ]{Style.RESET_ALL}"
                            )
                        time.sleep(1)

            else:
                self.log(
                    f"{Fore.MAGENTA+Style.BRIGHT}[ Quets{Style.RESET_ALL}"
                    f"{Fore.RED+Style.BRIGHT} Data Is None {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                )
            time.sleep(1)

            ms = user['data']['targetTime'] * 10
            hold = self.hold_nodes(hash, query, ms, user_id)
            if hold and hold['status'] == 'success':
                timestamp = datetime.fromtimestamp(hold['data']['currentTime']).strftime('%Y-%m-%d %H:%M')
                self.log(
                    f"{Fore.MAGENTA+Style.BRIGHT}[ Hold and Release{Style.RESET_ALL}"
                    f"{Fore.GREEN+Style.BRIGHT} Is Success {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                )
                self.log(
                    f"{Fore.MAGENTA+Style.BRIGHT}[ Simultaneous Request{Style.RESET_ALL}"
                    f"{Fore.WHITE+Style.BRIGHT} {hold['data']['simultaneousRequests']} req/s {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                )
                self.log(
                    f"{Fore.MAGENTA+Style.BRIGHT}[ Nearby Active IPs{Style.RESET_ALL}"
                    f"{Fore.WHITE+Style.BRIGHT} {hold['data']['nearbyActiveIps']} devices {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                )
                self.log(
                    f"{Fore.MAGENTA+Style.BRIGHT}[ Nearby Server Load{Style.RESET_ALL}"
                    f"{Fore.WHITE+Style.BRIGHT} {hold['data']['nearbyServerLoad']}% {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                )
                self.log(
                    f"{Fore.MAGENTA+Style.BRIGHT}[ Network Strength{Style.RESET_ALL}"
                    f"{Fore.WHITE+Style.BRIGHT} {hold['data']['networkStrength']} Mbps {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                )
                self.log(
                    f"{Fore.MAGENTA+Style.BRIGHT}[ Request Timestamp{Style.RESET_ALL}"
                    f"{Fore.WHITE+Style.BRIGHT} {timestamp} {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                )
                self.log(
                    f"{Fore.MAGENTA+Style.BRIGHT}[ Reward{Style.RESET_ALL}"
                    f"{Fore.WHITE+Style.BRIGHT} {hold['data']['points']} $mcWORK {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                )
            else:
                self.log(
                    f"{Fore.MAGENTA+Style.BRIGHT}[ Hold and Release{Style.RESET_ALL}"
                    f"{Fore.RED+Style.BRIGHT} Isn't Success {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                )

    def main(self):
        try:
            with open('query.txt', 'r') as file:
                queries = [line.strip() for line in file if line.strip()]

            while True:
                self.clear_terminal()
                time.sleep(1)
                self.welcome()
                self.log(
                    f"{Fore.GREEN + Style.BRIGHT}Account's Total: {Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT}{len(queries)}{Style.RESET_ALL}"
                )
                self.log(f"{Fore.CYAN + Style.BRIGHT}-{Style.RESET_ALL}"*75)

                for query in queries:
                    query = query.strip()
                    if query:
                        self.process_query(query)
                        self.log(f"{Fore.CYAN+Style.BRIGHT}-{Style.RESET_ALL}"*75)
                        time.sleep(3)

                seconds = 1800
                while seconds > 0:
                    formatted_time = self.format_seconds(seconds)
                    print(
                        f"{Fore.CYAN+Style.BRIGHT}[ Wait for{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} {formatted_time} {Style.RESET_ALL}"
                        f"{Fore.CYAN+Style.BRIGHT}... ]{Style.RESET_ALL}",
                        end="\r"
                    )
                    time.sleep(1)
                    seconds -= 1

        except KeyboardInterrupt:
            self.log(f"{Fore.RED + Style.BRIGHT}[ EXIT ] Alliance Micro Node - BOT.{Style.RESET_ALL}")
        except Exception as e:
            self.log(f"{Fore.RED + Style.BRIGHT}An error occurred: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    bot = AllianceMicroNode()
    bot.main()