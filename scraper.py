from bs4 import BeautifulSoup
import requests
import sqlite3


# class IterRegistry(type):
#     def __iter__(cls):
#         return iter(cls._registry)


# class Constituency:
#     def __init__(self, area):
#         self.area = area

#     def get_const(self):
#         return self.area


# class Candidate(Constituency):
#     __metaclass__ = IterRegistry
#     _registry = []

#     def __init__(self, name, party, votes, constituency):
#         self.name = name
#         self.party = party
#         self.votes = votes

#         Constituency.__init__(self, constituency)
#         self._registry.append(self)

#     def __str__(self):
#         return self.name

#     def display_info(self):
#         print(
#             f"Name:{self.name}\nParty:{self.party}\nConstituency:{self.area}\nVotes:{self.votes}")


# cand1 = Candidate("Shishir Khanal", "RSP", "17800", "Kathmandu 6")
# cand2 = Candidate("Sarbendra Khanal", "UML", "8500", "Kathmandu 6")
# cand3 = Candidate("Ganesh Parajuli", "UML", "8500", "Kathmandu 7")

# for item in Candidate._registry:
#     print("\n")
#     if item.get_const() == "Kathmandu 6":
#         item.display_info()

conn = sqlite3.connect('db.sqlite3')

url = "https://election.ekantipur.com/pradesh-3/district-kathmandu?lng=eng"
html_text = requests.get(url).text
soup = BeautifulSoup(html_text, 'html.parser')
election = soup.find('div', class_='election-2079')
all_const = election.find_all('div', class_="card")
id = 8
for card in all_const:
    const = card.find('h3', class_='card-title').text
    const_num = const.strip().split()[-1]
    candidates = card.find_all('div', class_='candidate-wrapper')
    count = 1
    for candidate in candidates:
        if count > 3:
            break
        name = candidate.find('div', class_='nominee-name').text
        party = candidate.find(
            'div', class_="candidate-party-name").find('a').text
        print(f"{name} | {party.strip()}")

        count += 1
        id += 1
        conn.execute(f"INSERT INTO e_app_details(id,name,party,vote,area_id) VALUES ('{id}','{name}','{party.strip()}','{count*1400}','{const_num}')")
    print("-----------------------------------------------------\n")
    count += 1
conn.commit()
conn.close()
