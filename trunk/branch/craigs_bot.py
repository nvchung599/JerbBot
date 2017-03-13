# PURPOSE:
# works in BotAgency.
# uses HTML navigation methods unique to Craigslist.com

# TODO: bring CraigsBot up to date and employ it in Agency
# TODO: tune extract_body_details here, since craigslist postings are all internal


from trunk.basic_bot import *


class CraigsBot(BasicBot):

    def __init__(self, history):
        super().__init__('craigs_bot', history)
        self.previous_url = ''

    def scrape_this_page(self, soup):

        row_blocks = soup.find_all('p', {'class': 'result-info'})
        row_dates = soup.find_all('time', {'class': 'result-date'})
        row_cities = soup.find_all('span', {'class': 'result-hood'})

        for i in range(len(row_blocks)):

            self.tally()

            title = row_blocks[i].contents[5].get_text()
            company = "---"
            url = 'https://sfbay.craigslist.org' + row_blocks[i].contents[5].get('href')
            date = row_dates[i].get_text()
            # city = row_cities[i].get_text()
            city = "---"
            # not every listing has a city, resulting in a desynch error... don't bother with this one


            self.bullshit_filter(title, company, url, city, date)


    def navigate_to_next_page(self, soup):

        self.previous_url = self.current_url

        next_page_element = soup.find_all('a', {'title': 'next page'})
        next_page_link = next_page_element[0].get('href')
        next_page_link = "https://sfbay.craigslist.org" + next_page_link

        r = requests.get(next_page_link)
        next_soup = BeautifulSoup(r.content, "html.parser")
        self.current_soup = next_soup
        self.current_url = next_page_link

    def end_check(self, soup):

        next_page_element = soup.find_all('a', {'title': 'next page'})
        next_page_link = next_page_element[0].get('href')

        if self.previous_url == self.current_url:
            print('REACHED END OF JOB BOARD')
            return False
        else:
            print('NEXT PAGE CONFIRMED')
            return True

    # def extract_job_details(self, job):
    #     """If necessary, tune extract_body_details here, since craigslist postings are all internal"""
