# PURPOSE:
# works in BotAgency.
# uses HTML navigation methods unique to monster.com

from trunk.basic_bot import *

class MonsterBot(BasicBot):

    def __init__(self, history):
        super().__init__('monster_bot', history)

    def scrape_this_page(self, soup):

        row_titles = soup.find_all('span', {'itemprop': 'title'})
        row_dates = soup.find_all('time', {'itemprop': 'datePosted'})
        row_cities = soup.find_all('span', {'itemprop': 'address'})
        row_companies = soup.find_all('span', {'itemprop': 'name'})

        print('hey hey hey')
        print(row_titles)
        print(row_dates)
        print(row_cities)
        print(row_companies)

        for i in range(len(row_titles)):

            self.tally()

            title = strip(row_titles[i].get_text())
            company = row_companies[i].get_text()
            date = row_dates[i].get_text()
            city = strip(row_companies[i].get_text())
            url = row_titles[i].parent.get('href')

            self.bullshit_filter(title, company, url, city, date)

    def navigate_to_next_page(self, soup):
        """
        There is no 'next' button.
        Instead we have to observe the pagination numbers and choose our URL based off of that.
        ^^^scratch that^^^ page button links can't be retrieved without some requests tweaking

        Solution: Turn page by appending string to link
        Caution: Base URL must be the first page of the search, so this function can append a pagination
        """
        print('current page %d' % self.current_page_number)
        print('next page %d' % (self.current_page_number + 1))

        next_page_number = self.current_page_number + 1
        next_page_link = self.base_url + '&page=' + str(next_page_number)

        print('next page link %s' % next_page_link)

        r = requests.get(next_page_link)
        next_soup = BeautifulSoup(r.content, "html.parser")
        self.current_soup = next_soup
        self.current_url = next_page_link



    def end_check(self, soup):
        """Since we can't access the pagination HTML code, just sample the jobs, if any"""

        blocks = soup.find_all('span', {'itemprop': 'title'})

        if len(blocks) == 0:
            print('REACHED END OF JOB BOARD')
            return False
        else:
            print('NEXT PAGE CONFIRMED')
            return True




