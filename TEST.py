from trunk.basic_bot import *
from trunk.branch.indeed_bot import *

history = []

indeed_bot = IndeedBot(history)
url = 'https://jobs.apple.com/search?job=55834501&openJobId=55834501#&openJobId=55834501'
job = Job('','',url,'', '')
indeed_bot.extract_job_details(job)
print('\n\n=================================================================================================')
print(job.body)
print(get_words(job.body))
indeed_bot.filter_body(job)
print(job.rejection_reason)
print(job.is_relevant)
print(indeed_bot.excluded_body)