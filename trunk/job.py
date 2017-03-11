# PURPOSE:
# Each instance of the Job class represents a job posting extracted from the web


class Job(object):

    def __init__(self, title, company, url, city, date):
        self.title = title
        self.company = company
        self.url = url
        self.date = date  # for now, a string
        self.city = city
        self.body = ''  # TODO, replace this string with an ordered list of strings (hint, get_words).
        self.is_relevant = True  # unless proven otherwise
        self.rejection_reason = ''
        self.rejection_identifier = None

    def __str__(self):
        return(
            '________________________________________________________________________________________________________\n'
            'Title:   %s\n'
            'Company: %s\n'
            'City:    %s\n'
            'Date:    %s\n'
            'URL:     %s'
            % (self.title, self.company, self.city, self.date, self.url)
            )

    # For identifying duplicate postings
    def __eq__(self, other):

        if self.url == other.url:
            return True
        else:
            return False

    def approve(self):
        self.is_relevant = True

    def reject(self, reason_identifier):

        self.is_relevant = False

        reason_dict = {
            0: 'applied',
            1: 'bad title',
            2: 'bad body text',
            3: 'bad exp req',
            4: 'bad url',
            5: 'duplicate',
            6: 'history duplicate'
        }

        self.rejection_reason = reason_dict.get(reason_identifier)
        self.rejection_identifier = reason_identifier
