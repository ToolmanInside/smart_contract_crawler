import vthread
import requests
import os
import json
import threading
import queue
import time
import random

MAX_FILE_NUMBER = 1371
CRAWL_TOKEN_1 = '35AH2NBKUWRVQNHFIKRE12TFHH64BKV3TI'
CRAWL_TOKEN_2 = 'ISQS1ADHV4HIP5R5X9QY1WX8A1ZZKGI1KN'
TOKEN_LIST = [CRAWL_TOKEN_1, CRAWL_TOKEN_2]
CRAWL_INTERVAL = 0.2
if not os.path.exists('bytecode_dict'):
    with open('bytecode_dict', 'w') as f:
        BYTECODE_DICT = set()
        BYTECODE_DICT.add('0x')
        print(BYTECODE_DICT, file = f)
BYTECODE_DICT = eval(open('bytecode_dict', 'r').readlines()[0])
pool_1 = vthread.pool(5, gqueue=1)
pool_2 = vthread.pool(5, gqueue=2)

class JsonParser(object):
    def __init__(self):
        self.__file_dir = os.path.join(os.getcwd(), 'jsons')
        self.contract_address = queue.Queue()

    def parse_json_files(self):
        contract_count = 900
        while (contract_count < MAX_FILE_NUMBER):
            #contract_count += self.__start_sign
            suff_fix = str(contract_count).zfill(4)
            file_name = 'contract' + '0' * 8 + suff_fix + '.json'
            file_dir = os.path.join(self.__file_dir, file_name)
            with open(file_dir) as f:
                #self.contract_address[contract_count] = list()
                strs = f.readlines()
                list_length = len(strs)
                for index in range(list_length):
                    address = json.loads(strs[index])['address']
                    bytecode = json.loads(strs[index])['bytecode']
                    if bytecode not in BYTECODE_DICT:
                        BYTECODE_DICT.add(bytecode)
                        self.contract_address.put(address)
            contract_count += 1
        with open('bytecode_dict', 'w') as f:
            print(BYTECODE_DICT, file = f)
        print(len(BYTECODE_DICT))
        print('Parse JSON file successful!')
        return self.contract_address

@vthread.pool(8)
def main_run(address):
    save_dir = os.path.join(os.getcwd(), 'contracts_4')
    crawl_token = random.choice(TOKEN_LIST)
    URL = 'https://api.etherscan.io/api?module=contract&action=getsourcecode&address=' + address + '&apikey=' + crawl_token
    try:
        response = requests.get(URL).content
    except:
        with open("Connection Fail", "a+") as con_fail:
            print(address, file = con_fail)
            return
 
    if response:
        ABI = eval(response)['result'][0]['ABI']
        if ABI == "Contract source code not verified":
            with open('fail_file', 'a+') as fail_file:
                print(address, file = fail_file)
                return 

        realcode = eval(response)['result'][0]['SourceCode']
        with open(os.path.join(save_dir, 'contract@' + address + '.sol'), 'a+') as f:
            print(realcode, file = f)

        time.sleep(CRAWL_INTERVAL)

def run():

    if not os.path.isdir('contracts_4'):
        os.mkdir('contracts_4')
    
    js = JsonParser()
    address_queue = js.parse_json_files()

    while not address_queue.empty():
        address = address_queue.get_nowait()
        main_run(address)

if __name__ == '__main__':
    run()
