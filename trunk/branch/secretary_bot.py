from trunk.basic_bot import *

# I work in BotAgency. I do not search for jobs. I exist to refilter and refresh the jobs_recorded.pkl on the disk.
class SecretaryBot(BasicBot):

    def __init__(self):
        place_holder = []
        super().__init__('indeed_bot', place_holder)

    def bullshit_filter(self, old_jobs):

        self.job_index = 0
        refreshed_jobs = []
        print('RECHECKING HISTORY')

        for this_job in old_jobs:

            self.job_index += 1
            print("secretary_bot processing job # %d" % self.job_index)

            if this_job.rejection_identifier == 0:  # already marked as applied
                refreshed_jobs.append(this_job)
                continue

            this_job.approve()

            self.filter_title(this_job)

            if this_job.is_relevant:
                self.filter_body(this_job)

            if this_job.is_relevant:
                print('job # %d approved                    O' % self.job_index)

            refreshed_jobs.append(this_job)

        return refreshed_jobs
