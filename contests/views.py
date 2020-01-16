from django.shortcuts import render
from bs4 import BeautifulSoup
import requests

# from PIL import Image

dict_url = {}
dict_contests = {}
dict_contests_cc = {}
counter = 1


def home(request):
    return render(request, 'home.html')


def contests(request):
    req = requests.get('https://codeforces.com' + '/contests')
    soup = BeautifulSoup(req.text, "html.parser")
    results = soup.find("div", {"class": "datatable"})
    result = results.find("table")
    links = results.findAll("tr")
    count = 0
    counter1 = 1
    for item in links:
        item_text = item.findAll("td")
        if item_text is not None:
            count = 0
            name = ""
            time = ""
            length = 0

            for contest_info in item_text:
                if count == 0:
                    name = contest_info.text
                    # print(name)
                    count += 1
                    continue
                if count == 1:
                    # time_info = contest_info.find("a")
                    # if time_info is not None:
                    #     time = time_info.text

                    count += 1
                    continue
                if count == 2:
                    time_info = contest_info.find("a")
                    time = time_info.text
                    # print(time)
                    count += 1
                    continue
                if count == 3:
                    length = contest_info.text
                    # print(length)
                    count += 1
                    continue
            link_contests = "https://codeforces.com/contests"
            if name is not None and time is not None and length != 0:
                tuple = [name, time, length, link_contests]
                dict_contests[counter1] = tuple
                counter1 += 1

    dict_contests_cc = codechef_contests(request)

    return render(request, 'contests.html',
                  {'list_url': dict_contests.items(), 'list_url_cc': dict_contests_cc.items()})


def codechef_contests(request):
    req = requests.get('https://www.codechef.com/contests')
    soup = BeautifulSoup(req.text, "html.parser")
    results = soup.findAll("table", {"class": "dataTable"})
    # future contests only
    count = 0
    counter2 = 1
    for table_data in results:
        if count == 0:
            count += 1
            continue
        if count == 1:
            name = ""
            url1 = ""
            start_time = ""
            end_time = ""
            table_columns = table_data.findAll("tr")
            for all_tr in table_columns:

                table_col_td = all_tr.findAll("td")
                for table_content in table_col_td:
                    link_url = table_content.find("a")
                    if link_url is not None:
                        url1 = link_url.attrs["href"]
                        name = link_url.text
                        print("here", name)
                        break

                time = all_tr.find("td", {"class": "start_date"})
                if time is not None:
                    start_time = time.text
                else:
                    start_time = None
                print(start_time)
                time = all_tr.find("td", {"class": "end_date"})
                if time is not None:
                    end_time = time.text
                else:
                    end_time = None
                print(end_time)
                if name is not None and start_time is not None and end_time is not None:
                    tuple = [name, url1, start_time, end_time]
                    print(tuple)
                    dict_contests_cc[counter2] = tuple
                    counter2 += 1
                    count += 1

    return dict_contests_cc


def problemset(request):
    return render(request, 'problemset.html')


def tags(request):
    global dict_url
    global counter
    range1 = request.GET['range1']
    range2 = request.GET['range2']
    print(range1, range2)
    tags_str = range1 + "-" + range2
    print(tags_str)
    range1 = int(range1)
    range2 = int(range2)
    problemset1(request, tags_str)
    problemset2(request, range1, range2)
    return render(request, 'tags.html', {'list_url': dict_url.items()})


def problemset1(request, tags_str):
    global dict_url
    global counter
    cf = 'https://codeforces.com'
    # query = {'q': 'Forest', 'order': 'popular', 'min_width': '800', 'min_height': '600'}
    # params = "writing-first-c-program-hello-world-example"
    req = requests.get(cf + '/problemset', )
    soup = BeautifulSoup(req.text, "html.parser")
    results = soup.find("div", {"class": "pagination"})
    result = results.findAll("a")
    total = result[-2].text
    total = int(total)
    print(total)
    total = 1
    x = 1
    save = ""

    while (x <= total):

        page = 'https://codeforces.com/problemset/page/' + str(x)
        params = {'tags': tags_str}
        req = requests.get(page, params=params)
        print(req.url)
        soup = BeautifulSoup(req.text, "html.parser")
        # print(soup.prettify())
        results = soup.find("table", {"class": "problems"})
        links = results.findAll("tr")
        for item in links:
            item_text = item.findAll("td")
            name = ""
            new_url = ""
            rating = 0

            for td in item_text:
                find_div = td.find("div")
                find_span = td.find('span', {"class": "ProblemRating"})
                if find_div is not None:
                    url = find_div.find("a")
                    # print(url)
                    url1 = url.attrs["href"]
                    name = url.text

                    new_url = cf + url1

                    # print(url1,text_url,1500)
                    # print(str1)

                    # dict_url [counter] =str1

                    # list_url.append(c)
                    # print()
                if find_span is not None:
                    rating = find_span.text

            if name is not None and new_url is not None and rating is not None and rating != 0:
                r = requests.get(new_url)
                new_url = r.url
                tuple = [name, new_url, rating]
                # print(new_url)
                dict_url[counter] = tuple
                counter += 1

        x = x + 1

    # return render(request,'contest.html',{'list_url': dict_url.items()})


def problemset2(request, range1, range2):
    print("here")
    range1 = int(range1)
    range2 = int(range2)
    global dict_url
    cc = 'https://codechef.com'
    global counter
    start = ""
    end = ""
    start_index = 0
    end_index = 0
    if range1 >= 500 and range1 <= 900:
        start = "school"
        start_index = 1
    elif range1 > 900 and range1 <= 1500:
        start = "easy"
        start_index = 2
    elif range1 > 1500 and range1 <= 2200:
        start = "medium"
        start_index = 3
    else:
        start = "hard"
        start_index = 4
    if range2 >= 500 and range2 <= 900:
        end = "school"
        end_index = 1
    elif range2 > 900 and range2 <= 1500:
        end = "easy"
        end_index = 2
    elif range2 > 1500 and range2 <= 2200:
        end = "medium"
        end_index = 3
    else:
        end = "hard"
        end_index = 4

    while start_index <= end_index:

        page = 'https://codechef.com/problems/' + start
        req = requests.get(page)
        print("here")
        print(req.url)
        soup = BeautifulSoup(req.text, "html.parser")
        # print(soup.prettify())
        results = soup.find("table", {"class": "dataTable"})
        links = results.findAll("tr")
        for item in links:
            item_text = item.findAll("td")
            name = ""
            new_url = ""
            rating = 0
            itr = 0
            for td in item_text:
                itr += 1
                find_div = td.find("div", {"class": "problemname"})
                find_a = td.find('a')
                if find_div is not None:
                    url = find_div.find("a")
                    # print(url)
                    url1 = url.attrs["href"]
                    name = url.text

                    new_url = cc + url1

                    # print(url1,text_url,1500)
                    print(new_url)

                    # dict_url [counter] =str1

                    # list_url.append(c)
                    # print()
                if itr == 4:
                    accuracy = find_a.text
                    accuracy = 100 - float(accuracy)
                    rating = range1 + ((range2 - range1) * accuracy) / 100
                    rating = int(rating)

            if rating >= range1 and rating <= range2:
                r = requests.get(new_url)
                new_url = r.url
                tuple = [name, new_url, rating]
                # print(new_url)
                dict_url[counter] = tuple
                counter += 1
                if counter > 100:
                    break

        if start == 'school':
            start = 'easy'
        elif start == 'easy':
            start = 'medium'
        elif start == 'medium':
            start = 'hard'
        start_index += 1