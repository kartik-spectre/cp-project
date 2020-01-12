from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
#from PIL import Image
def home(request):
    return render(request,'home.html')

def problemset(request):
    return render(request, 'problemset.html')
def tags(request):
    range1 = request.GET['range1']
    range2 = request.GET['range2']
    print(range1 ,range2)
    tags_str=range1+"-"+range2
    print(tags_str)
    dict_url=problemset1(request,tags_str)
    return render(request,'tags.html',{'list_url': dict_url.items()})
def problemset1(request,tags_str):
    cf = 'https://codeforces.com'
    # query = {'q': 'Forest', 'order': 'popular', 'min_width': '800', 'min_height': '600'}
    # params = "writing-first-c-program-hello-world-example"
    counter=1
    dict_url={}
    req = requests.get(cf + '/problemset',)
    soup = BeautifulSoup(req.text, "html.parser")
    results = soup.find("div", {"class": "pagination"})
    result = results.findAll("a")
    total = result[-2].text
    total = int(total)
    print(total)
    total=1
    x = 1
    save = ""

    while (x <= total):

        page = 'https://codeforces.com/problemset/page/' + str(x)
        params = {'tags':tags_str}
        req = requests.get(page,params=params)
        soup = BeautifulSoup(req.text, "html.parser")
        # print(soup.prettify())
        results = soup.find("table", {"class": "problems"})
        links = results.findAll("tr")
        for item in links:
            item_text = item.findAll("td")
            name=""
            new_url=""
            rating=0

            for td in item_text:
                find_div = td.find("div")
                find_span= td.find('span',{"class": "ProblemRating"})
                if find_div is not None:
                    url = find_div.find("a")
                    # print(url)
                    url1 = url.attrs["href"]
                    name = url.text

                    new_url = cf + url1

                    # print(url1,text_url,1500)
                    #print(str1)

                    #dict_url [counter] =str1

                    #list_url.append(c)
                    # print()
                if find_span is not None :
                    rating = find_span.text

            if name is not None and new_url is not None and rating is not None and rating !=0:
                r = requests.get(new_url)
                new_url = r.url
                tuple=[name,new_url,rating]
                print(new_url)
                dict_url[counter]=tuple
                counter += 1




        x = x + 1
    return dict_url


    #return render(request,'contest.html',{'list_url': dict_url.items()})
