from trunk.basic_bot import *
from trunk.branch.indeed_bot import *
from trunk.branch.secretary_bot import *

history = []
indeed_bot = IndeedBot(history)
url = 'https://www.monster.com/jobs/search/?q=mechanical+engineer&where=Milpitas%2c+CA&&client=classic&sort=dt.rv.di&rad=50&page=30'
job = Job('','',url,'', '')

r = requests.get(url)
soup = BeautifulSoup(r.content, "html.parser")

blocks = soup.find_all('span', {'itemprop': 'title'})
print(len(blocks))
for block in blocks:
    print(block)

# indeed_bot.extract_job_details(job)
# print('\n\n=================================================================================================')
# print(job.body)
# print(get_words(job.body))
# indeed_bot.filter_body(job)
# print(job.rejection_reason)
# print(job.is_relevant)
# print(indeed_bot.excluded_body)