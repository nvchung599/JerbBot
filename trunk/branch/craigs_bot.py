# PURPOSE:
# works in BotAgency.
# uses HTML navigation methods unique to Craigslist.com

# TODO: bring CraigsBot up to date and employ it in Agency
# TODO: tune extract_body_details here, since craigslist postings are all internal


from trunk.basic_bot import *


class CraigsBot(BasicBot):

    def __init__(self, history):
        super().__init__('craigs_bot', history)

    def navigate_to_next_page(self):

        r = requests.get(self.current_url)
        soup = BeautifulSoup(r.content, "html.parser")
        next_page_element = soup.find_all('a', {'title': 'next page'})
        link_page_link = next_page_element[0].get('href')
        link_page_link = "https://sfbay.craigslist.org" + link_page_link
        self.current_url = link_page_link

    def scrape_this_page(self):

        r = requests.get(self.current_url)
        soup = BeautifulSoup(r.content, "html.parser")
        row_blocks = soup.find_all('p', {'class': 'result-info'})
        row_dates = soup.find_all('time', {'class': 'result-date'})

        for i in range(len(row_blocks)):

            self.tally()

            title = row_blocks[i].contents[5].get_text()
            company = "---"
            url = 'https://sfbay.craigslist.org' + row_blocks[i].contents[5].get('href')
            date = row_dates[i].get_text()
            #TODO city
            city = ''

            self.bullshit_filter(title, company, url, city, date)

    def end_check(self):
        """TODO"""

    def extract_job_details(self, job):
        """TODO"""