from bardapi import BardCookies
import datetime

cookie_dict = {
    "__Secure-1PSID": "ZggRFwb02xeo-o1vJIH-Ykd1hWVF3vDNUbRRG7caVGtyNvR7DkdXoUrh7q8cnBaScxqqOA.",
    "__Secure-1PSIDTS": "",
    "__Secure-1PSIDCC": "APoG2W8vAKe9bpx-hgSXdCGuwWOqPpWLrKYGT_QHe6UC1H6DqEKs2i2VTozZfeZHd9Sm0RsRbr8"
}

bard = BardCookies(cookie_dict=cookie_dict)

while True:
    Query = input("Enter your query: ")
    Reply = bard.get_answer(Query)['content']
    print(Reply)