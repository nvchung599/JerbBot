# PURPOSE:
# works in BotAgency.
# does not search for jobs.
# exists to refilter and refresh the jobs_saved.pkl on the disk.

from trunk.basic_bot import *


class SecretaryBot(BasicBot):

    def __init__(self):
        place_holder = []
        super().__init__('secretary_bot', place_holder)

    def history_bullshit_filter(self, old_jobs):
        """reapplies filters to jobs that have already been saved to disk"""

        self.job_index = 0
        refreshed_jobs = []
        print('RECHECKING HISTORY')

        for this_job in old_jobs:

            self.job_index += 1
            print(self.name + " processing job # %d" % self.job_index)

            if this_job.rejection_identifier in ('a', 'r'):  # already marked as removed, don't filter
                refreshed_jobs.append(this_job)
                continue

            this_job.approve()
            this_job.good_hits = []

            self.filter_title(this_job)

            if this_job.is_relevant:
                self.filter_body(this_job)

            if this_job.is_relevant:
                print('job # %d approved                    O' % self.job_index)

            refreshed_jobs.append(this_job)

        return refreshed_jobs

    def scrape_this_page(self):
        return

    def navigate_to_next_page(self):
        return

    def end_check(self):
        return
