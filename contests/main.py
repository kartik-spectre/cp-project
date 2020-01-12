from bs4 import BeautifulSoup
import requests
#from PIL import Image

cf = 'https://codeforces.com'
#query = {'q': 'Forest', 'order': 'popular', 'min_width': '800', 'min_height': '600'}
#params = "writing-first-c-program-hello-world-example"
req = requests.get(cf + '/problemset')
soup = BeautifulSoup(req.text, "html.parser")
results = soup.find("div", {"class": "pagination"})
result = results.findAll("a")
total = result[-2].text
total = int(total)
print(total)
x=1
save=""
while(x<=total):

    page ='https://codeforces.com/problemset/page/'+ str(x)
    req = requests.get(page)#,params=params)
    soup = BeautifulSoup(req.text,"html.parser")
    #print(soup.prettify())
    results = soup.find("table",{"class":"problems"})
    links = results.findAll("tr")
    for item in links:
        flag=False
        item_text = item.findAll("td")
        for txt in item_text:
            text1=txt.findAll("span",{"class":"ProblemRating"})
            for txt2 in text1:
                txt3=txt2.text
                #print(txt3)
                if txt3=="1500":
                    flag=True
        if flag==True:
            for td in item_text:
                find_div = td.find("div")
                if find_div is not None:
                    url = find_div.find("a")
                    #print(url)
                    url1= url.attrs["href"]
                    text_url= url.text
                    str1 = cf + url1

                    #print(url1,text_url,1500)
                    print(str1)
                    #print()
                    break

    x = x + 1