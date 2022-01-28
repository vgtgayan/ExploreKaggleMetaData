from time import sleep
import aiohttp
import asyncio
import time
import re
import pandas as pd
import numpy as np
import traceback


async def get_country(session, url):
    '''
        Return the country of a given kaggle user
    '''    
    async with session.get(url) as resp:
        # json_resp = await resp.json()
        html_text = await resp.text()
        # print(html_text)
        country = re.search(r',"country":"([\w ]+)"', html_text)
        if country != None:
            country_ = str(country.group(1))
            print(country_)
            return country_
        else:
            return "NA"


async def get_country_wrapper(usernames):

    try:
        async with aiohttp.ClientSession() as session:
            
            base_url = 'https://www.kaggle.com/'
            result = []
            wait_counter = 0
            for username in usernames:
                url = base_url+str(username)
                if wait_counter%1000 == 0:
                    print("Wait ...")
                    time.sleep(10)
                    print("Go ...")
                result.append(asyncio.create_task(get_country(session, url)))
                # result.append(get_country(session, url))
                wait_counter += 1

            country_lst = await asyncio.gather(*result)
            return country_lst

    except Exception as e:
        print("Error: ", traceback.format_exc())



df = pd.read_csv("Users.csv")
df.head()
sample_df = df.sample(n=10000)

# sample_df = pd.read_csv("sample_Users.csv")
# sample_df.head()


# sample_df.shape
user_list = sample_df['UserName'].to_numpy(copy=True)
# user_list = ['jhovey1', 'jsheppard95', 'dudihgustian', 'khmx5200', 'skshivamkedia']
# print(user_list[:5])

start_time = time.time()
# asyncio.run(get_country_wrapper(user_list[:5])) ## Error out
country_list = asyncio.get_event_loop().run_until_complete(get_country_wrapper(user_list))
print("--- %s seconds ---" % (time.time() - start_time))

# print(country_list)

# Add the country_list to the data frame
sample_df['Country'] = np.array(country_list)
print(sample_df['Country'])
# sample_df.to_csv("sample_Users_with_country.csv")
sample_df.to_csv('sample_Users_with_country.csv.gz', compression='gzip')