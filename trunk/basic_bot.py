from trunk.job import *
from trunk.general import *
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


class BasicBot(object):

    # ------------------------------------------------------------------------------------------------------------------
    # INITIALIZER
    # ------------------------------------------------------------------------------------------------------------------

    def __init__(self, name, history):

        self.name = name
        if not os.path.exists("trunk/branch/" + str(self.name) + ".txt"):
            self.define_basis()

        self.base_url = read_file("trunk/branch/" + self.name + ".txt")
        self.current_url = self.base_url
        self.page_limit = 5
        self.current_page_number = 1
        self.history = history
        self.jobs = []
        self.job_index = 0
        self.job_index_rejected = 0
        self.need_to_terminate = False

        # TODO read these from file
        self.bad_word_tolerance = 3
        self.good_word_tolerance = 2
        self.min_years_exp = 4
        self.min_str_len = 4
        self.max_retries = 25


        self.essential_body = file_to_set('trunk/filters/essential_body.txt')
        self.excluded_body = file_to_set('trunk/filters/excluded_body.txt')
        self.excluded_title = file_to_set('trunk/filters/excluded_title.txt')

    # ------------------------------------------------------------------------------------------------------------------
    # NAV & SCAN
    # ------------------------------------------------------------------------------------------------------------------

    def scrape_all_pages(self):
        for i in range(self.page_limit):
            try:
                self.scrape_this_page()
                if not self.end_check():
                    break
                self.navigate_to_next_page()
                self.current_page_number += 1

                if self.need_to_terminate:
                    print(self.name + ' has encountered a problem (probably requests hangup) and is terminating early')
                    break

            except:
                print('\n\nSCRAPE_ALL_PAGES HAS ENCOUNTERED ERROR AND HAS BROKEN LOOP')
                print('RETURNING JOB LIST AS IS\n\n')
                break
            else:
                print(self.name + ' RETURNING ALL FOUND JOBS')

        only_new_jobs = []

        for each_job in self.jobs:
            if each_job.rejection_identifier not in [5, 6]:
                only_new_jobs.append(each_job)

        return only_new_jobs
        # TODO return statistics too
        # TODO return only those jobs that were not rejected by historical filter

    def scrape_this_page(self):
        print('implementation belongs to child classes')

    def navigate_to_next_page(self):
        print('implementation belongs to child classes')

    def end_check(self):
        print('implementation belongs to child classes')

    def tally(self):
        self.job_index += 1
        print(self.name + ' processing job # ' + str(self.job_index))

    # TODO need an extraction algorithm that will pull relevant, non-hyperlinked text from body (the meat of posting)
    # TODO maintain spacing between words when appending lines to strings

    # Given a job instance w/ URL defined... load job.body with all applicable text belonging to that page
    def extract_job_details(self, job):

        my_str = ''
        try:
            r = requests.get(job.url)
        except:
            print('error on page of job # %d            -' % self.job_index)
            print(job.url)
            job.reject(4)
            self.job_index_rejected += 1
            return 'bad url'

        soup = BeautifulSoup(r.content, 'html.parser')
        target_tags = ['p', 'li', 'ul', 'span', 'br', 'font']

        for tag in target_tags:
            target_blocks = soup.find_all(tag)
            for block in target_blocks:
                append_this = block.get_text()
                if len(get_words(append_this)) >= self.min_str_len:
                    my_str += ' '  # ensures that lines don't stick w/o spacing
                    my_str += append_this
                # else:
                #     print('HIT')
                # print(len(get_words(append_this)))
                # print('---' + append_this + '\n\n')
                # my_str += (block.get_text() + '\n')

        job.body = my_str

    def filter_history(self, job):
        if job in self.history:
            print("historical duplicate on job # %d     X" % self.job_index)
            # print(job.url)
            job.reject(6)
            self.job_index_rejected += 1
            return

    def filter_title(self, job):

        title_words = get_words(job.title)
        for word in title_words:
            if word in self.excluded_title:
                print("bad title on job # %d                X" % self.job_index)
                # print(job.url)
                job.reject(1)
                self.job_index_rejected += 1
                return

    def filter_duplicate(self, job):

        if job in self.jobs:
            print("duplicate posting on job # %d        X" % self.job_index)
            # print(job.url)
            job.reject(5)
            self.job_index_rejected += 1
            return

    def filter_body(self, job):

        # TODO empty string indicates website has counter-scraping measures, implement delay in request to counteract
        if job.body == '':
            job.reject(4)
            self.job_index_rejected += 1
            print('error on page of job # %d            -' % self.job_index)
            print(job.url)
            return

        body_words = get_words(job.body)
        bad_word_count = 0
        bad_words = []
        good_word_count = 0
        good_words = []

        for i in range(len(body_words)):

            # check for singular, DESIRED keywords. a specified number of desired keywords is required for approval
            if body_words[i] in self.essential_body:
                if body_words[i] not in good_words:  # no dupes
                    good_words.append(body_words[i])
                    good_word_count += 1

            # check for singular, FORBIDDEN keywords. a specified number of forbidden keywords is tolerated
            if body_words[i] in self.excluded_body:

                if body_words[i] not in bad_words:
                    bad_words.append(body_words[i])
                    bad_word_count += 1
                # print('BAD WORD FOUND ' + body_words[i])
                if bad_word_count > self.bad_word_tolerance:
                    job.reject(2)
                    self.job_index_rejected += 1
                    print("bad body text on job # %d            X" % self.job_index)
                    print(bad_words)
                    print(job.url)
                    return

            # check for characteristic "_ or more years of exp" line
            try:  # check if it's a number
                if is_integer(body_words[i]):
                    my_int = int(body_words[i])
                    if my_int > self.min_years_exp:
                        for j in range(5):  # scan the few words following the number
                            try:
                                if body_words[i+j] in ('experience', 'years'):
                                    job.reject(3)
                                    self.job_index_rejected += 1
                                    print('bad exp req on job # %d              X' % self.job_index)
                                    # print(job.url)
                                    return
                            except:
                                pass
            except:
                pass  # if it's not a number

        if good_word_count < self.good_word_tolerance:
            job.reject(2)
            self.job_index_rejected += 1
            print("lack of good text on job # %d        X" % self.job_index)
            print(good_words)
            print(job.url)

    def bullshit_filter(self, title, company, url, city, date):

        this_job = Job(title, company, url, city, date)

        self.filter_history(this_job)

        if this_job.is_relevant:
            self.filter_duplicate(this_job)

        if this_job.is_relevant:
            self.filter_title(this_job)

        if this_job.is_relevant:
            self.extract_job_details(this_job)

            if this_job.is_relevant:
                self.filter_body(this_job)

        if this_job.is_relevant:
            print('job # %d approved                    O' % self.job_index)
        self.jobs.append(this_job)

    # ------------------------------------------------------------------------------------------------------------------
    # FILE & MEMORY MANAGEMENT
    # ------------------------------------------------------------------------------------------------------------------

    # Each website that is crawled is placed in a separate project folder
    def create_project_dir(self, directory_name):
        if not os.path.exists(directory_name):
            os.makedirs(directory_name)
            print("Creating new directory: " + directory_name)
        else:
            print("Existing directory detected: " + directory_name)

    # TODO implement ordered tree search algorithm
    # Create queue and crawled files (if not created)
    def initialize_files(self):

        directory_name = 'trunk/filters'
        essential_body = directory_name + "/essential_body.txt"
        excluded_body = directory_name + "/excluded_body.txt"
        excluded_title = directory_name + "/excluded_title.txt"
        if not os.path.exists(directory_name):
            self.create_project_dir(directory_name)
        for file in (essential_body, excluded_body, excluded_title):
            if not os.path.isfile(file):
                print("Creating new file " + file)
                write_file(file, "")

        directory_name = 'trunk/records'
        jobs_record = directory_name + "/jobs_record.txt"
        jobs_rejected = directory_name + "/jobs_rejected.txt"
        jobs_applied = directory_name + "/jobs_applied.txt"
        if not os.path.exists(directory_name):
            self.create_project_dir(directory_name)
        for file in (jobs_record, jobs_rejected, jobs_applied):
            if not os.path.isfile(file):
                print("Creating new file " + file)
                write_file(file, "")

    # creates or updates basis.txt in current directory
    def define_basis(self):

        path = "trunk/branch/" + str(self.name) + ".txt"
        if not os.path.exists(path):
            print("Defining new basis for " + self.name)
        else:
            print("Updating basis for " + self.name)

        input_url = input("Input new base URL for %s: ", self.name)
        write_file(path, input_url)
