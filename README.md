# JerbBot

The task of job hunting can be divided into three tasks:

* searching for applicable jobs <<< __JerbBot automates this__
* applying to those jobs
* interviewing for those jobs

In addition to performing typical advance search functions, JerbBot
picks up where jobsite search engines fall short:

* classifying job descriptions by experience requirements
* "soft" filters with keyword occurrence thresholds for
acceptance/rejection
* providing search statistics and insights into the job market

![JerbBot Block Diagram](https://github.com/nvchung599/JerbBot/blob/master/JerbBot%20Block%20Diagram.png)

## Getting Started

Install:
* requests
* beautifulsoup4
* fake-useragent

Run main.py

Most numerical settings can be adjusted in the text-based UI

Keyword libraries are .txt files that you must modify directly

Jobsite seed URLs are .txt files that you must modify directly

* __excluded_title.txt__ is an absolute keyword exclusion list for job
posting titles
* __excluded_body.txt__ is a soft keyword exclusion list for job posting
bodies/descriptions. __bad_word_tolerance__ specifies the allowance for
unique occurrences of these undesired words before a job is classified as
irrelevant by the filtering algorithm. This tolerance can be adjusted in
the config.
* __essential_body.txt__ is a soft keyword inclusion list for job posting
bodies/descriptions. __good_word_tolerance__ specifies the requirement for
unique occurrences of these desired words before a job is classified as
relevant by the filtering algorithm. This tolerance can be adjusted in
the config.

To start with a clean slate, delete __jobs_saved.pkl__. It will
reinitialize upon performing another scrape

When first tuning the filters for your specific job market, set
__good_word_tolerance__ to 0. Spot check jobs and construct your keyword
lists progressively, increasing/decreasing tolerances as necessary.

__View Jobs__ displays all relevant, pending jobs and some statistics.
I use the PyCharm IDE, so URLs are clickable in the console.

__Scrape Jobs__ performs a jobsite scrape.

__Config__ allows modification of some search/filter parameters. Restart
for changes to take effect.

__Apply Tracker__ is like a tinder for viewing/processing your search
results. This feature is incomplete -- jobs applied/removed cannot be
accessed again.

__Refresh__ reapplies filters to your job cache. Use after updating your
keyword lists and/or numerical filter parameters.

Jobsite Scraping:
![Scraping](https://github.com/nvchung599/JerbBot/blob/master/Scraping.png)

Filtered Results:
![Results](https://github.com/nvchung599/JerbBot/blob/master/Results.png)

## Acknowledgments

* Friends and family who guided me during the days of unemployment

