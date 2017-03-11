# TODO list acceptable input base url, and basic method of filtering
# TODO tune extract body deets in child class


from trunk.basic_bot import *


class IndeedBot(BasicBot):

    def __init__(self, history):
        super().__init__('indeed_bot', history)

    def navigate_to_next_page(self):

        are_we_there_yet = False  # indicator for whether or not we succeeded at jumping the page
        ua = UserAgent()
        retries = 0

        while not are_we_there_yet:

            print('TRYING TO TURN PAGE')
            retries += 1
            if retries > self.max_retries:
                self.need_to_terminate = True
                break

            # roll dice for current page's HTML code
            headers = {'User-Agent': ua.random}
            r = requests.get(self.current_url, headers=headers)
            soup = BeautifulSoup(r.content, "html.parser")
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
            soup = BeautifulSoup(r.content, "html.parser")
            pagination_buttons = soup.find('div', {'class': 'pagination'})

            # gets bold number
            next_page_number = self.current_page_number + 1
            bold_page_number = int(pagination_buttons.find('b').get_text())
            if bold_page_number == next_page_number:
                are_we_there_yet = True
                print('BOLD NUMBER IDENTIFIED AS %d' % bold_page_number)

        self.current_url = next_page_link

        print("TURNED PAGE TO " + self.current_url)

    def scrape_this_page(self):

        r = requests.get(self.current_url)
        soup = BeautifulSoup(r.content, "html.parser")
        row_blocks = soup.find_all('h2', {'class': 'jobtitle'})
        row_dates = soup.find_all('span', {'class': 'date'})
        row_cities = soup.find_all('span', {'itemprop': 'addressLocality'})

        for i in range(len(row_blocks)):

            self.tally()

            title = row_blocks[i].contents[1].get('title')
            company = strip(row_blocks[i].next_sibling.next_sibling.get_text())
            url = 'https://www.indeed.com' + row_blocks[i].contents[1].get('href')
            date = row_dates[i].get_text()
            city = row_cities[i].get_text()

            self.bullshit_filter(title, company, url, city, date)

    def end_check(self):
        r = requests.get(self.current_url)
        soup = BeautifulSoup(r.content, "html.parser")
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
