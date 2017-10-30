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
from trunk.branch.monster_bot import *
from trunk.branch.secretary_bot import *
import pickle


class Agency(object):

    def __init__(self):

        sort_files()
        self.new_jobs = []
        self.old_jobs = []
        self.all_jobs = []
        self.jobs_load()
        self.secretary_bot = SecretaryBot()
        self.bot_squad = []

        """INITIALIZE BOTS HERE"""
        self.bot_squad.append(IndeedBot(self.old_jobs))
        # self.bot_squad.append(CraigsBot(self.old_jobs))
        # self.bot_squad.append(MonsterBot(self.old_jobs))

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
            print('      1-View Jobs    |    2-Scrape Jobs      |    3-Config ')
            print('      q-Quit         |    w-Apply Tracker    |    r-Refresh                 ')
            print('__________________ Input Command & Press Enter ___________________')
            my_input = input()

            if my_input == '1':
                if self.jobs_load():
                    self.print_all(self.old_jobs)
                    self.statistics(self.old_jobs)
                continue

            if my_input == '2':
                self.scrape()
                self.jobs_save(self.new_jobs, 'update')
                self.new_jobs = []
                continue

            #if my_input == '3':
            #    self.jobs_save(self.new_jobs, 'update')
            #    self.new_jobs = []
            #    continue

            if my_input == 'r':
                self.refresh_history()
                self.statistics(self.old_jobs)
                continue

            if my_input == '3':
                self.modify_search_settings()
                continue

            if my_input == 'q':
                print('bfy loves you')
                break

            #if my_input == 'e':
            #    if self.jobs_load():
            #        self.apply_all()
            #    continue

            if my_input == 'w':
                if self.jobs_load():
                    self.apply_one()
                continue

    def scrape(self):
        """Commands all bots to scrape their sites. Resulting jobs aggregated and stored in RAM.
        The UI command '3-save/commit' transfers these jobs from RAM to disk """

        self.jobs_load()
        self.new_jobs = []

        for bot in self.bot_squad:
            self.new_jobs += bot.scrape_all_pages()

        self.statistics(self.new_jobs)
        print('SCRAPE COMPLETE. NOTE: Resulting job list still in RAM')
        print('We observed %d new jobs' % len(self.new_jobs))

    @staticmethod
    def statistics(jobs):
        """Prints stats on a given job list"""
        total_absolute = len(jobs)
        if total_absolute == 0:
            print('Statistics() Error: div by zero')
            print('the job list called must be empty/nonexistent')
            return

        # number of jobs not applied for yet (relevant & irrelevant)
        total_pending = 0
        for job in jobs:
            if job.rejection_identifier not in ['a', 'r']:
                total_pending += 1

        reason_a = 0
        reason_r = 0
        reason_1 = 0
        reason_2 = 0
        reason_3 = 0
        reason_4 = 0

        for job in jobs:
            if not job.is_relevant:
                if job.rejection_identifier == 'a':
                    reason_a += 1
                if job.rejection_identifier == 'r':
                    reason_r += 1
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
        print('Pending Relevant Jobs        %d' % (total_pending-total_reject))
        print('Pending Irrelevant Jobs      %d' % total_reject)
        print('Jobs You Applied/Removed     %d' % reason_a)
        print('Jobs You Rejected/Removed    %d' % reason_r)
        print('...')
        print('Relevant Pending         %d %%' % (((total_pending-total_reject) / total_pending) * 100))
        print('Irrelevant-Title         %d %%' % ((reason_1 / total_pending) * 100))
        print('Irrelevant-BodyText      %d %%' % ((reason_2 / total_pending) * 100))
        print('Irrelevant-Experience    %d %%' % ((reason_3 / total_pending) * 100))
        print('Irrelevant-BadUrl        %d %%' % ((reason_4 / total_pending) * 100))
        print('\n')

        # FOR REFERENCE
        # 0: 'applied/removed'
        # 1: 'bad title'
        # 2: 'bad body text'
        # 3: 'bad exp req'
        # 4: 'bad url'
        # 5: 'duplicate'
        # 6: 'history duplicate'

    @staticmethod
    def print_all(jobs):
        """Prints each job entry to screen"""

        if len(jobs) == 0:
            print('print_all() recieved empty input')
            return

        for job in jobs:
            if job.is_relevant:
                print(job)
            else:
                continue

    def apply_one(self):
        """Manually process jobs one by one, user can selectively remove jobs from relevant job pool"""
        temp_old_jobs = self.old_jobs

        for job in temp_old_jobs:

            if job.is_relevant:
                print(job)
                print('\nExamine this job, then provide command')
                print('_________________________________')
                print(" 1-Apply  |  2-Reject  |  3-Skip ")
                print(" q-Quit                          ")
                print('____________ Input ______________')
                my_input = input()

                if my_input == '1':
                    job.reject('a')
                    print('Marked as applied & removed')
                    continue

                if my_input == '2':
                    job.reject('r')
                    print('Marked as rejected & removed')
                    continue

                if my_input == '3':
                    print('Skipping...')
                    continue

                if my_input == 'q':
                    break
                else:
                    print('Wrong input... Skipping...')
                    continue

        print('\n\n\n\n\nSession ended, saving results')
        self.jobs_save(temp_old_jobs, 'overwrite')

    def apply_all(self):
        """Removes all relevant jobs from history, and marks them as 'applied/removed'"""

        print("Are you sure? Enter 'y' if so")

        if input() == 'y':

            for job in self.old_jobs:
                if job.is_relevant:
                    job.reject('a')  # 0 for apply
            self.jobs_save(self.old_jobs, 'overwrite')
            print('All relevant jobs have been marked as applied')

        else:
            print('returning to main menu')

    def refresh_history(self):
        """Reapplies filters to jobs that are stored on disk. Saves automatically."""

        self.old_jobs = self.secretary_bot.history_bullshit_filter(self.old_jobs)
        self.jobs_save(self.old_jobs, 'overwrite')

    def jobs_save(self, jobs, method):
        """
        method 'update'
        Adds new jobs to existing job list on disk.

        method 'overwrite'
        An overwrite save of jobs on disk, used when jobs on disk have been modified and should be overwritten
        """

        if len(jobs) == 0:
            print('There is no data to save')
        else:

            if method == 'update':
                jobs += self.old_jobs
            elif method == 'overwrite':
                pass

            with open('trunk/records/jobs_saved.pkl', 'wb') as file_output:
                pickle.dump(jobs, file_output, pickle.HIGHEST_PROTOCOL)
                self.old_jobs = jobs
            print('Job list has been committed to disk')

    def jobs_load(self):
        """Updates Agency's job list. Call whenever you need to modify the job list in RAM."""

        if os.path.exists('trunk/records/jobs_saved.pkl'):
            with open('trunk/records/jobs_saved.pkl', 'rb') as file_input:
                self.old_jobs = pickle.load(file_input)
            return True
        else:
            print("job_records cannot be found")
            return False

    def modify_search_settings(self):
        """Initializes search settings on program start"""
        want_to_exit = False
        while want_to_exit == False:

            print('_____ Current Settings _____\n'
                  ' good_word_tolerance  = %d\n' % self.bot_squad[0].good_word_tolerance,
                  'bad_word_tolerance   = %d\n' % self.bot_squad[0].bad_word_tolerance,
                  'min_years_exp        = %d\n' % self.bot_squad[0].min_years_exp,
                  'min_str_len          = %d\n' % self.bot_squad[0].min_str_len,
                  'page_limit           = %d\n' % self.bot_squad[0].page_limit,)

            for bot in self.bot_squad:
                print('     %s is seeded with URL:' % bot.name)
                print('     %s\n' % bot.base_url)

            print('Choose parameter to modify:\n'
                  '____________________________________\n'
                  ' 1-good_word_tolerance   |   q-Quit\n'
                  ' 2-bad_word_tolerance    |   w-Seed URLs\n'
                  ' 3-min_years_exp         |   e-Site Toggles\n'
                  ' 4-min_str_len           |   r-Filter Tuning\n'
                  ' 5-page_limit            |\n'
                  '_______________ Input ______________\n')
            my_input = input()

            if my_input == '1':
                print('Input integer:\n')
                parameter_input = input()
                if not is_integer(parameter_input):
                    print('Invalid input\n'
                          'returning to main menu')
                    return
                else:
                    f = open('trunk/filters/good_word_tolerance.txt', 'w')
                    f.write(parameter_input)
                    f.close()
                    print('good_word_tolerance changed to %d\n' % int(parameter_input))
                    print('restart program to take effect')
                continue

            if my_input == '2':
                print('Input integer:\n')
                parameter_input = input()
                if not is_integer(parameter_input):
                    print('Invalid input\n'
                          'returning to main menu')
                    return
                else:
                    f = open('trunk/filters/bad_word_tolerance.txt', 'w')
                    f.write(parameter_input)
                    f.close()
                    print('bad_word_tolerance changed to %d\n' % int(parameter_input))
                    print('restart program to take effect')
                continue

            if my_input == '3':
                print('Input integer:\n')
                parameter_input = input()
                if not is_integer(parameter_input):
                    print('Invalid input\n'
                          'returning to main menu')
                    return
                else:
                    f = open('trunk/filters/min_years_exp.txt', 'w')
                    f.write(parameter_input)
                    f.close()
                    print('min_years_exp changed to %d\n' % int(parameter_input))
                    print('restart program to take effect')
                continue

            if my_input == '4':
                print('Input integer:\n')
                parameter_input = input()
                if not is_integer(parameter_input):
                    print('Invalid input\n'
                          'returning to main menu')
                    return
                else:
                    f = open('trunk/filters/min_str_len.txt', 'w')
                    f.write(parameter_input)
                    f.close()
                    print('min_str_len changed to %d\n' % int(parameter_input))
                    print('restart program to take effect')
                continue

            if my_input == '5':
                print('Input integer:\n')
                parameter_input = input()
                if not is_integer(parameter_input):
                    print('Invalid input\n'
                          'returning to main menu')
                    return
                else:
                    f = open('trunk/filters/page_limit.txt', 'w')
                    f.write(parameter_input)
                    f.close()
                    print('page_limit changed to %d\n' % int(parameter_input))
                    print('restart program to take effect')
                continue

            if my_input == 'q':
                want_to_exit = True
                print('Returning to main menu')
                continue

            if my_input == 'w':
                print('WIP')
                continue

            if my_input == 'e':
                print('WIP')
                continue

            if my_input == 'r':
                print('Instructions: edit keyword libraries directly in the .txt files:\n'
                      '     trunk/filters/essential_body.txt\n'
                      '     trunk/filters/excluded_body.txt\n'
                      '     trunk/filters/excluded_title.txt\n')
                return

            print('Invalid input\n')


            # TODO TODO TODO TODO TODO TODO TODO TODO
            # TODO TODO TODO TODO TODO TODO TODO TODO
    def modify_numerical_parameter(self, parameter_name):
        print('Input integer for %s:\n' % parameter_name)
        parameter_input = input()
        if not is_integer(parameter_input):
            print('Invalid input\n'
                  'returning to main menu')
            return False
        else:
            parameter_path = 'trunk/filters/' + parameter_name + '.txt'
            f = open(parameter_path, 'w')
            f.write(parameter_input)
            f.close()
            print('%s changed to %d\n' % (parameter_name, int(parameter_input)))
        return True
            # TODO TODO TODO TODO TODO TODO TODO TODO
            # TODO TODO TODO TODO TODO TODO TODO TODO