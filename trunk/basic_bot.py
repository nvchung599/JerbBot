# PURPOSE:
# Bot parent class.
# Children bots scan/scrape their assigned websites, filtering jobs as they go.
# These jobs are reported back to the Agency.

from trunk.job import *
from trunk.general import *
import requests
from bs4 import BeautifulSoup
import abc


class BasicBot(metaclass=abc.ABCMeta):

    # ------------------------------------------------------------------------------------------------------------------
    # INITIALIZER
    # ------------------------------------------------------------------------------------------------------------------

    def __init__(self, name, history):

        self.name = name
        if not os.path.exists("trunk/branch/" + str(self.name) + ".txt"):
            self.initialize_base_url()

        self.base_url = read_file("trunk/branch/" + self.name + ".txt")
        self.current_url = self.base_url
        self.current_soup = None
        self.current_page_number = 1
        self.history = history
        self.jobs = []
        self.job_index = 0
        self.job_index_rejected = 0
        self.need_to_terminate = False

        self.initialize_search_settings()
        # TODO TODO TODO TODO TODO TODO TODO TODO
        # TODO TODO TODO TODO TODO TODO TODO TODO
        self.bad_word_tolerance = int(file_to_set('trunk/filters/bad_word_tolerance.txt').pop()) # Body Text
        self.good_word_tolerance = int(file_to_set('trunk/filters/good_word_tolerance.txt').pop()) # Body Text
        self.min_years_exp = int(file_to_set('trunk/filters/min_years_exp.txt').pop())
        self.min_str_len = int(file_to_set('trunk/filters/min_str_len.txt').pop())
        self.page_limit = int(file_to_set('trunk/filters/page_limit.txt').pop())
        # TODO TODO TODO TODO TODO TODO TODO TODO
        # TODO TODO TODO TODO TODO TODO TODO TODO

        self.initialize_filters()
        self.essential_body = file_to_set('trunk/filters/essential_body.txt')
        self.excluded_body = file_to_set('trunk/filters/excluded_body.txt')
        self.excluded_title = file_to_set('trunk/filters/excluded_title.txt')

    # ------------------------------------------------------------------------------------------------------------------
    # NAV & SCAN
    # ------------------------------------------------------------------------------------------------------------------

    def scrape_all_pages(self):
        """navigate and scrape site until specified/unspecified page
        limit or some other form of termination (hangups, errors)"""

        # requests per page on indeed???
        # make 'current_soup'
        # reduce requests from min 4 per page to min 1 per page
        # make initial soup before loop, seed loop with soup

        r = requests.get(self.current_url)
        self.current_soup = BeautifulSoup(r.content, "html.parser")

        for i in range(self.page_limit):
            try:

                self.scrape_this_page(self.current_soup)

                if not self.end_check(self.current_soup):
                    break

                self.navigate_to_next_page(self.current_soup)

                if self.need_to_terminate:
                    print(self.name + ' has encountered a problem (probably requests hangup) and is terminating early')
                    break

                self.current_page_number += 1



            except:
                print('\n\nSCRAPE_ALL_PAGES HAS ENCOUNTERED AN EXCEPTION AND HAS BROKEN LOOP')
                print('RETURNING JOB LIST AS IS\n\n')
                break
            else:
                print('All lights green')

        only_new_jobs = []

        for each_job in self.jobs:
            if each_job.rejection_identifier not in [5, 6]:
                only_new_jobs.append(each_job)

        return only_new_jobs

    @abc.abstractmethod
    def scrape_this_page(self, soup):
        """Parse the current URL and pass every job posting on the page through the function bullshit_filter()"""
    @abc.abstractmethod
    def navigate_to_next_page(self, soup):
        """Turns to the next page, overcoming any bot/scraping protection the site may have"""
    @abc.abstractmethod
    def end_check(self, soup):
        """Verifies that a next page exists"""

    def tally(self):
        """This function should be called every time a job posting is processed"""

        self.job_index += 1
        print(self.name + ' processing job # ' + str(self.job_index))

    def extract_job_details(self, job):
        """Given a job w/ URL defined... load the job with all applicable text belonging to that page"""

        my_words = []
        try:
            r = requests.get(job.url)
        except:
            print('page loading error on job # %d       -' % self.job_index)
            print(job.url)
            job.reject(4)
            self.job_index_rejected += 1
            return 'bad url'

        soup = BeautifulSoup(r.content, 'html.parser')
        target_tags = ['p', 'li', 'ul', 'span', 'br', 'font']

        for tag in target_tags:
            target_blocks = soup.find_all(tag)
            for block in target_blocks:
                append_this = get_words(block.get_text())
                if len(append_this) >= self.min_str_len:
                    my_words += append_this

        job.body = my_words

    def filter_history(self, job):
        """Exclude duplicates of jobs that have already been saved to disk"""

        if job in self.history:
            print("historical duplicate on job # %d     X" % self.job_index)
            # print(job.url)
            job.reject(6)
            self.job_index_rejected += 1
            return

    def filter_title(self, job):
        """Reject jobs with at least 1 bad word"""
        title_words = get_words(job.title)
        for word in title_words:
            if word in self.excluded_title:
                print("bad title on job # %d                X" % self.job_index)
                # print(job.url)
                job.reject(1)
                self.job_index_rejected += 1
                return

    def filter_duplicate(self, job):
        """Exclude duplicates of jobs that have already been found during this search"""

        if job in self.jobs:
            print("duplicate posting on job # %d        X" % self.job_index)
            # print(job.url)
            job.reject(5)
            self.job_index_rejected += 1
            return

    def filter_body(self, job):
        """
        Reject jobs based on:
            -good word count/tolerance
            -bad word count/tolerance
            -particular strings
            -whether any text was extracted at all
        """

        # empty string indicates website has counter-scraping measures, implement delay in request to counteract
        if len(job.body) == 0:
            job.reject(4)
            self.job_index_rejected += 1
            print('text extraction error on job # %d    -' % self.job_index)
            print(job.url)
            return

        bad_word_count = 0
        bad_words = []
        good_word_count = 0
        good_words = []

        for i in range(len(job.body)):

            # check for singular, DESIRED keywords. a specified number of desired keywords is required for approval
            if job.body[i] in self.essential_body:
                if job.body[i] not in good_words:  # no dupes
                    good_words.append(job.body[i])
                    job.good_hits.append(job.body[i])
                    good_word_count += 1

            # check for singular, FORBIDDEN keywords. a specified number of forbidden keywords is tolerated
            if job.body[i] in self.excluded_body:

                if job.body[i] not in bad_words:
                    bad_words.append(job.body[i])
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
                if is_integer(job.body[i]):
                    my_int = int(job.body[i])
                    if my_int > self.min_years_exp:
                        for j in range(5):  # scan the few words following the number
                            try:
                                if job.body[i+j] in ('experience', 'years'):
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
        """Does a full-spectrum-relevance check and records the job, relevant or not"""

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

    @staticmethod
    def initialize_filters():
        """The filters are shared by all bots, and are stored in .txt files in trunk/filters"""

        directory_name = 'trunk/filters'
        essential_body = directory_name + "/essential_body.txt"
        excluded_body = directory_name + "/excluded_body.txt"
        excluded_title = directory_name + "/excluded_title.txt"

        if not os.path.exists(directory_name):
            create_folder(directory_name)

        for file in (essential_body, excluded_body, excluded_title):
            if not os.path.isfile(file):
                print("Creating new file " + file)
                write_file(file, "")

    def initialize_search_settings(self):

        directory_name = 'trunk/filters'

        bad_word_tolerance_filename = directory_name + "/bad_word_tolerance.txt"
        good_word_tolerance_filename = directory_name + "/good_word_tolerance.txt"
        min_years_exp_filename = directory_name + "/min_years_exp.txt"
        min_str_len_filename = directory_name + "/min_str_len.txt"
        page_limit_filename = directory_name + "/page_limit.txt"

        if not os.path.exists(directory_name):
            create_folder(directory_name)

        for file in (bad_word_tolerance_filename, good_word_tolerance_filename, min_years_exp_filename, min_str_len_filename, page_limit_filename):
            if not os.path.isfile(file):
                print("Creating new file " + file)
                write_file(file, "0")
        return 0

    def initialize_base_url(self):
        """Base URLs are stored in .txt files alongside their respective bots in trunk/branch"""

        path = "trunk/branch/" + str(self.name) + ".txt"
        if not os.path.exists(path):
            print("\n!! NEW BOT DETECTED !!\n")
            print("Defining new basis for " + self.name)
        else:
            print("Updating basis for " + self.name)

        print("Input base URL:")
        input_url = input()
        write_file(path, input_url)
