# PURPOSE:
# works in BotAgency.
# uses HTML navigation methods unique to Indeed.com

from trunk.basic_bot import *
from fake_useragent import UserAgent


class IndeedBot(BasicBot):

    def __init__(self, history):
        super().__init__('indeed_bot', history)
        self.max_retries = 25

    def scrape_this_page(self, soup):

        row_blocks = soup.find_all('h2', {'class': 'jobtitle'})
        row_dates = soup.find_all('span', {'class': 'date'})
        row_cities = soup.find_all('span', {'class': 'location'})

        for i in range(len(row_blocks)):

            self.tally()
            title = row_blocks[i].contents[1].get('title')
            company = strip(row_blocks[i].next_sibling.next_sibling.get_text())
            url = 'https://www.indeed.com' + row_blocks[i].contents[1].get('href')
            date = row_dates[i].get_text()
            city = row_cities[i].get_text()
            self.bullshit_filter(title, company, url, city, date)


    def navigate_to_next_page(self, soup):
        """
        Indeed.com has an anti-scraping mechanism (intentional or unintentional) that randomly prevents the bot from obtaining the correct URL from
        the 'Next' button. When this happens, the resulting URL either leads to an invalid page (creates an exception)
        or it links to the same page as before, keeping the bot in one spot.

        This can be circumvented by simply looping the HTML request and randomizing the user-agent until the bot can
        verify a page turn by observing the bolded pagination in the page footer.
        """

        are_we_there_yet = False
        ua = UserAgent()
        retries = 0

        while not are_we_there_yet:

            print('TRYING TO TURN PAGE')
            retries += 1
            if retries > self.max_retries:
                self.need_to_terminate = True
                break

            # vvv Rolled Dice vvv
            headers = {'User-Agent': ua.random}
            next_page_element = soup.find_all('span', {'class': 'np'})

            # get next page address
            if self.current_page_number == 1:
                try:
                    next_page_link = next_page_element[0].parent.parent.get('href')
                except:
                    print('NEXT PAGE BUTTON FOULED, RETRY')
                    continue
            else:
                try:
                    next_page_link = next_page_element[1].parent.parent.get('href')
                except:
                    print('NEXT PAGE BUTTON FOULED, RETRY')
                    continue
            next_page_link = "https://www.indeed.com" + next_page_link

            # verify that the next page is consistent with the bold page number footer
            r = requests.get(next_page_link, headers=headers)
            next_soup = BeautifulSoup(r.content, "html.parser")
            pagination_buttons = next_soup.find('div', {'class': 'pagination'})

            # gets bold number
            next_page_number = self.current_page_number + 1
            bold_page_number = int(pagination_buttons.find('b').get_text())
            if bold_page_number == next_page_number:
                are_we_there_yet = True
                print('BOLD NUMBER IDENTIFIED AS %d' % bold_page_number)
            else:
                # roll the dice for current page's HTML code
                print('RETRYING HTML REQUEST ON CURRENT PAGE')
                r = requests.get(self.current_url, headers=headers)
                soup = BeautifulSoup(r.content, "html.parser")

        if self.need_to_terminate:
            pass
        else:
            self.current_url = next_page_link
            self.current_soup = next_soup
            print("TURNED PAGE TO " + self.current_url)

    def end_check(self, soup):
        """In the case of Indeed, the last page will not have any 'Next' pagination, bold or not"""

        row_blocks = soup.find_all('span', {'class': 'np'})
        button_list = []
        for block in row_blocks:
            button_list += get_words(block.get_text())

        if 'next' not in button_list:
            print('REACHED END OF JOB BOARD')
            return False
        else:
            print('NEXT BUTTON CONFIRMED')
            return True




