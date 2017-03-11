from trunk.branch.indeed_bot import *
from trunk.branch.craigs_bot import *
import pickle
from trunk.Agency import *



sort_files()
my_agency = Agency()
my_agency.ui()

print(len(my_agency.old_jobs))
for job in my_agency.old_jobs:
    print(job.rejection_identifier)
    # if job.rejection_identifier != 0:
    #     print('0')

# TODO BREAK BREAK BREAK BREAK BREAK BREAK BREAK BREAK BREAK BREAK BREAK BREAK BREAK BREAK BREAK BREAK BREAK BREAK

# this_bot = IndeedBot()
#
# this_bot.scrape_all_pages()
#
# dupes = 0
#
# for job in this_bot.jobs:
#     if job.is_relevant:
#         print(job)
#     else:
#         continue
#
# for job in this_bot.jobs:
#
#     if not job.is_relevant:
#         print(job.title + " at " + job.company + " was rejected for " + job.rejection_reason)
#         print(job.url)
#         if job.rejection_identifier == 5:
#             dupes += 1
#     else:
#         continue
#
# print('\n')
# print(this_bot.name + ' report')
# print('jobs scanned = %d' % this_bot.job_index)
# print('percent filtered = %d%%' % (100*this_bot.job_index_rejected/this_bot.job_index))
# print('relevant postings = %d' % (this_bot.job_index-this_bot.job_index_rejected))
# print('number of duplicate postings = %d' % dupes)
# print('\n')

# TODO BREAK BREAK BREAK BREAK BREAK BREAK BREAK BREAK BREAK BREAK BREAK BREAK BREAK BREAK BREAK BREAK BREAK BREAK

# my_job1 = Job('asda', 'asdsa', 'asdsa', 'asdas')
# my_job2 = Job('asda', 'asdsa', 'asdsa', 'asdas')
# my_job3 = Job('asda', 'asdsa', 'asds123a', 'asdas')
#
# my_list = [my_job1, my_job2, my_job3]
#
# my_agency = BotAgency()
# my_list = my_agency.jobs_remove_duplicates(my_list)
#
# for job in my_list:
#     print(job)

# TODO BREAK BREAK BREAK BREAK BREAK BREAK BREAK BREAK BREAK BREAK BREAK BREAK BREAK BREAK BREAK BREAK BREAK BREAK

# url = "https://shimmick.mua.hrdepartment.com/hr/ats/Posting/view/1/0"
# my_job = Job('asda', 'asdsa', url, 'asdas')
# this_bot.extract_job_details(my_job)
# print(my_job.body)

# sort_files()


