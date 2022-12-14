from bs4 import BeautifulSoup
import requests
import psycopg2


def parliament(conn):
    url = "https://election.ekantipur.com/pradesh-3/district-kathmandu?lng=eng"
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'html.parser')
    election = soup.find('div', class_='election-2079')
    all_const = election.find_all('div', class_="card")
    id = 0
    id_ext = 0
    cur = conn.cursor()
    for card in all_const:
        const = card.find('h3', class_='card-title').text
        const_num = const.strip().split()[-1]
        candidates = card.find_all('div', class_='candidate-wrapper')
        count = 1
        id_ext += 1
        for candidate in candidates:
            if count > 3:
                break
            name = candidate.find('div', class_='nominee-name').text
            party = candidate.find(
                'div', class_="candidate-party-name").find('a').text
            vote = candidate.find('div', class_="vote-count").text.strip()
            vote=vote.replace(",","")
            print(f"{name} | {party.strip()}")

            count += 1
            id += 1

            update_script = "UPDATE e_app_details SET id=%s,name=%s,party=%s,vote=%s,area_id=%s WHERE id=%s;"
            update_values = (f'{id}', f'{name}', f'{party.strip()}',
                             f'{vote}', f'{const_num}', id)
            cur.execute(update_script, update_values)

            r = requests.get(
                'https://www.timeanddate.com/worldclock/nepal/kathmandu')
            soup = BeautifulSoup(r.text, "html.parser")
            time = soup.find(
                'div', {'class': 'bk-focus__qlook'}).find('span').text
            time_script = "UPDATE e_app_main set updated_time=%s where id=%s"
            cur.execute(time_script, (time, 1))
        print("-----------------------------------------------------\n")
        count += 1


def provincial(conn):
    url = "https://election.ekantipur.com/province-level-results/pradesh-3/district-kathmandu?lng=eng"
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'html.parser')
    all_const = soup.find_all('div', class_="chartClass")
    id = 30
    id_ext = 10
    cur = conn.cursor()
    for card in all_const:
        const = card.find(
            'div', class_='sabha-widget-title').find('h3').text.strip()[-6:].strip()
        print(f"Kathmandu-{const}")
        election = card.find('ul', class_='election-list')
        election_list = election.find_all('li', class_='election-list__item')
        count = 1
        id_ext += 1
        for candidate in election_list:
            if count > 3:
                break
            count += 1
            id += 1
            name = candidate.find('div', class_='nominee-name').text.strip()
            party = candidate.find(
                'div', class_='candidate-party-name').text.strip()
            vote = candidate.find('span', class_="vote-count").text.strip()
            vote=vote.replace(",","")
            # print(f"{name} | {party}" | {vote})

            update_script = "UPDATE e_app_details SET id=%s,name=%s,party=%s,vote=%s,area_id=%s WHERE id=%s;"
            update_values = (f'{id}', f'{name}', f'{party.strip()}',
                             f'{vote}', f'{id_ext}', id)
            cur.execute(update_script, update_values)

            r = requests.get(
                'https://www.timeanddate.com/worldclock/nepal/kathmandu')
            soup = BeautifulSoup(r.text, "html.parser")
            time = soup.find(
                'div', {'class': 'bk-focus__qlook'}).find('span').text
            time_script = "UPDATE e_app_main set updated_time=%s where id=%s"
            cur.execute(time_script, (time, 1))

        print("-----------------------------------------------------\n")


def hot_seat(conn):

    seats = [2, 23, 20, 16, 17, 3, 4, 5, 6, 11, 10]

    url = "https://election.ekantipur.com/?lng=eng"
    id = 90
    id_ext = 30
    for item in seats:
        html_text = requests.get(url).text
        soup = BeautifulSoup(html_text, 'html.parser')
        cards = soup.find_all('div', class_='card')

        const = cards[item].find(
            'h3', class_='card-title').text.strip().split()
        print(const[0]+"-"+const[-1])
        candidates = cards[item].find('ul', class_='candidate-list')
        leaderboard = candidates.find_all('li', class_='candidate-list__item')
        id_ext += 1
        cur = conn.cursor()
        for candidate in leaderboard:
            id += 1
            name = candidate.find('h4', class_='nominee-name').text.strip()
            party = candidate.find('h3', class_='party-name').text.strip()
            vote = candidate.find('div', class_='vote-count').text.strip()
            vote=vote.replace(",","")
            print(f"{name} | {party} | {vote}")
            update_script = "UPDATE e_app_details SET id=%s,name=%s,party=%s,vote=%s,area_id=%s WHERE id=%s;"

            update_values = (f'{id}', f'{name}', f'{party}',
                             f'{vote}', f'{id_ext}', id)
            cur.execute(update_script, update_values)
        print("-------------------------------------------------------\n")


def init():

    # Initialize datbase connection
    hostname = 'ec2-44-194-92-192.compute-1.amazonaws.com'
    database = 'dbs7ud3vc8mmko'
    username = 'fwewuizhuazuib'
    pwd = '3d27558e10cab7826d1d7b0491a32bdeb22621f4ee15decef0759a548a9e775a'
    port_id = 5432


    conn = psycopg2.connect(host=hostname,
                            dbname=database,
                            user=username,
                            password=pwd,
                            port=port_id)

    parliament(conn)
    provincial(conn)

    hot_seat(conn)

    # cur = conn.cursor()

    # Sort the data

    # sort constituencies
    # cur.execute(
    #     'create table new as select * from e_app_election_area order by id;')
    # cur.execute('drop table e_app_election_area;')
    # cur.execute('create table e_app_election_area as select * from new;')
    # cur.execute('drop table new;')

    # # sort the candidates by votes
    # cur.execute(
    #     'create table new as select * from e_app_details order by area_id asc ,vote desc;')
    # cur.execute('drop table e_app_details;')
    # cur.execute('create table e_app_details as select * from new;')
    # cur.execute('drop table new;')

    # reorder the id
    # cur.execute('ALTER TABLE e_app_details drop column id;')
    # cur.execute('ALTER TABLE e_app_details add id serial;')
    conn.commit()

    conn.close()


init()