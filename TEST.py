from trunk.basic_bot import *
from trunk.branch.indeed_bot import *
from trunk.branch.secretary_bot import *

history = []
indeed_bot = IndeedBot(history)
url = 'https://sfbay.craigslist.org/search/egr'
job = Job('','',url,'', '')

r = requests.get(url)
soup = BeautifulSoup(r.content, "html.parser")
row_blocks = soup.find_all('span', {'class': 'result-hood'})
row_num = 0

for row in row_blocks:
    row_num += 1
    print(row_num)
    print(row.get_text())

# indeed_bot.extract_job_details(job)
# print('\n\n=================================================================================================')
# print(job.body)
# print(get_words(job.body))
# indeed_bot.filter_body(job)
# print(job.rejection_reason)
# print(job.is_relevant)
# print(indeed_bot.excluded_body)