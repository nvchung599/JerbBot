# AGENCY PURPOSE:
#
# houses all instances of bots
# aggregates job data from all of its bots (indeed_bot, craigs_bot, etc).
# also possesses a 'secretary_bot' which is responsible for offline job refiltering.
#
# provides all methods for UI
#
# provides all methods for job history data management

from trunk.branch.indeed_bot import *
from trunk.branch.craigs_bot import *
from trunk.branch.secretary_bot import *

class Agency(object):

    def __init__(self):

        self.new_jobs = []
        self.old_jobs = []
        self.all_jobs = []
        self.jobs_recorded_load()
        self.secretary_bot = SecretaryBot()
        self.bot_squad = []
        self.bot_squad.append(IndeedBot(self.old_jobs))
        # self.bot_squad.append(CraigsBot(self.old_jobs))

        print('\n')
        print("NOTE: Changes to Job class effect secretary_bot's filters, basic_bot's filters, statistics(), [unique]_bot extraction methods")
        print("NOTE: you have delete the history list if any changes were made to the Job class")
        print("NOTE: you have to recompile the program for filter additions/subtractions changes to take place")
        print("SUGGESTION: to better tune the bot, set good_word_tolerance to 0 temporarily to observe postings")
        print('\n')
        print('_____Default Parameters_____')
        print('...')
        print('bad_word_tolerance       %d' % self.secretary_bot.bad_word_tolerance)
        print('good_word_tolerance      %d' % self.secretary_bot.good_word_tolerance)
        print('min_years_exp            %d' % self.secretary_bot.min_years_exp)
        print('min_str_len              %d' % self.secretary_bot.min_str_len)
        print('...')

    def ui(self):

        i_want_to_quit = False

        while not i_want_to_quit:

            print('__________________________________________________________________')
            print(' 1-Repo  |  2-Scrape    |  3-Commit    |              |  5-Config ')
            print(' q-Quit  |  w-ApplyOne  |  e-ApplyAll  |  r-Refresh   |           ')
            print('__________________ Input Command & Press Enter ___________________')
            my_input = input()

            if my_input == '1':
                if self.jobs_recorded_load():
                    self.print_all(self.old_jobs)
                    self.statistics(self.old_jobs)
                continue

            if my_input == '2':
                self.scrape()
                continue

            if my_input == '3':
                self.jobs_recorded_update(self.new_jobs)
                continue

            # TODO HISTORY: refresh, clear
            if my_input == 'r':
                self.refresh_history()
                continue

            # TODO CONFIG: page count, filters parameters, toggle bots, min years exp
            if my_input == '5':
                print('WIP for this input')
                continue

            if my_input == 'q':
                print('Have a nice day')
                break

            if my_input == 'e':
                if self.jobs_recorded_load():
                    self.apply_all()
                continue

            if my_input == 'w':
                if self.jobs_recorded_load():
                    self.apply_one()
                continue

    # Commands all bots to scrape their sites. Resulting jobs aggregated. DOES NOT SAVE TO FILE
    def scrape(self):

        self.jobs_recorded_load()
        self.new_jobs = []

        for bot in self.bot_squad:
            self.new_jobs += bot.scrape_all_pages()

        self.statistics(self.new_jobs)
        print('SCRAPE COMPLETE. NOTE: Resulting job list still in RAM')
        print('We observed %d new jobs' % len(self.new_jobs))

    # Prints stats on a given job list
    def statistics(self, jobs):

        total_absolute = len(jobs)
        if total_absolute == 0:
            print('Statistics() Error: div by zero')
            print('the job list called must be empty/nonexistent')
            return

        # number of jobs not applied for yet (relevant & irrelevant)
        total_pending = 0
        for job in jobs:
            if job.rejection_identifier != 0:
                total_pending += 1

        reason_0 = 0
        reason_1 = 0
        reason_2 = 0
        reason_3 = 0
        reason_4 = 0

        for job in jobs:
            if not job.is_relevant:
                if job.rejection_identifier == 0:
                    reason_0 += 1
                if job.rejection_identifier == 1:
                    reason_1 += 1
                if job.rejection_identifier == 2:
                    reason_2 += 1
                if job.rejection_identifier == 3:
                    reason_3 += 1
                if job.rejection_identifier == 4:
                    reason_4 += 1

        # do not include reason 0
        total_reject = reason_1 + reason_2 + reason_3 + reason_4

        print('\n')
        print('_____Job Statistics_____')
        print('...')
        print('Relevant Jobs        %d' % (total_pending-total_reject))
        print('Irrelevant Jobs      %d' % total_reject)
        print('Applied Jobs         %d' % reason_0)
        print('...')
        print('Approved Pending     %d %%' % (((total_pending-total_reject) / total_pending) * 100))
        print('Rejected-Title       %d %%' % ((reason_1 / total_pending) * 100))
        print('Rejected-BodyText    %d %%' % ((reason_2 / total_pending) * 100))
        print('Rejected-Experience  %d %%' % ((reason_3 / total_pending) * 100))
        print('Rejected-BadUrl      %d %%' % ((reason_4 / total_pending) * 100))
        print('\n')

        # FOR REFERENCE
        # 0: 'applied/removed'
        # 1: 'bad title'
        # 2: 'bad body text'
        # 3: 'bad exp req'
        # 4: 'bad url'
        # 5: 'duplicate'
        # 6: 'history duplicate'

    # Prints each job entry to screen
    def print_all(self, these_jobs):

        if len(these_jobs) == 0:
            print('print_all() recieved empty input')
            return

        for job in these_jobs:
            if job.is_relevant:
                print(job)
            else:
                continue

    # Manually process jobs one by one, user can selectively remove jobs from relevant job pool
    # TODO: distinguish between <applied/removed> and <rejected/removed>
    def apply_one(self):

        temp_old_jobs = self.old_jobs

        for job in temp_old_jobs:

            if job.is_relevant:
                print(job)
                print('\nExamine this job, then provide command')
                print('______________________________')
                print(" 1-Mark  |  2-Next  |  q-Quit")
                print('____________ Input ___________')
                my_input = input()

                if my_input == '1':
                    job.reject(0)
                    print('Marked as applied/removed')
                    continue

                if my_input == '2':
                    print('Skipping...')
                    continue

                if my_input == 'q':
                    break

        print('\n\n\n\n\nSession ended, saving results')
        self.jobs_recorded_overwrite(temp_old_jobs)

    # Removes all relevant jobs from history, and marks them as 'applied/removed'
    def apply_all(self):

        print("Are you sure? Enter 'y' if so")

        if input() == 'y':

            for job in self.old_jobs:
                if job.is_relevant:
                    job.reject(0)  # 0 for apply
            self.jobs_recorded_overwrite(self.old_jobs)
            print('All relevant jobs have been marked as applied')

        else:
            print('returning to main menu')

    def refresh_history(self):
        self.old_jobs = self.secretary_bot.bullshit_filter(self.old_jobs)
        self.statistics(self.old_jobs)
        self.jobs_recorded_overwrite(self.old_jobs)

    # Adds new jobs to file, but does not overwrite (which erases historical jobs)
    def jobs_recorded_update(self, jobs):
        if len(jobs) == 0:
            print('There is no data to save')
        else:
            jobs += self.old_jobs  # <- only difference between updates/overwrite is this line
            with open('trunk/records/jobs_recorded.pkl', 'wb') as file_output:
                pickle.dump(jobs, file_output, pickle.HIGHEST_PROTOCOL)
                self.old_jobs = jobs
            print('Job list has been committed to disk')

    def jobs_recorded_overwrite(self, jobs):
        if len(jobs) == 0:
            print('There is no data to save')
        else:
            with open('trunk/records/jobs_recorded.pkl', 'wb') as file_output:
                pickle.dump(jobs, file_output, pickle.HIGHEST_PROTOCOL)
                self.old_jobs = jobs
            print('Job list has been committed to disk')

    def jobs_recorded_load(self):

        if os.path.exists('trunk/records/jobs_recorded.pkl'):
            with open('trunk/records/jobs_recorded.pkl', 'rb') as file_input:
                self.old_jobs = pickle.load(file_input)
            return True
        else:
            print("job_records cannot be found")
            return False

    # UNUSED!!!
    # TODO not useful for bullshit_filter(), but good for updating records
    def jobs_remove_duplicates(self, job_list):
        new_job_list = []
        for job in job_list:
            if job not in new_job_list:
                new_job_list.append(job)
        return new_job_list


