import requests
from bs4 import BeautifulSoup
import pandas as pd

import warnings
warnings.simplefilter(action = 'ignore', category = FutureWarning)


def web_scraper(url):
    print('Running Engine')
    #url = input('Please Enter the url')
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    print(f'This is the Page Title \n{soup.title.text}')
    
    link = [str(i).split()[1].split('"')[1] for i in soup.select('h1')] # creating the Link list
    print('Link Collection Successful 100%')
    title = [i.text for i in soup.select('h1')]
    print('Title Collection Successful 100%')


    #Creating a dataframe of our dataset which contains title and link
    data = pd.DataFrame(data = {'Title':title, 'Link':link}).drop_duplicates().reset_index().drop('index',axis = 1)


    #Creating our Location
    data['Location'] = location(data) 
    data['Location'] = update_lc(data)
    data = data[data.Location != 'No Location'].reset_index().drop('index', axis = 1) 
    
    
    data['Year'] = year_update(data)[0] #Year column
    data['Year'] = year_clean(data)

    data['Content'] = year_update(data)[1] #Content colusmn
    print('Year Collection Successful 100%')
    data = content(data)

    print('Starting Job Information Collection')
    cc = description(data)
    data['Job Information'] = cc

    return data

def years(base):
    work = []
    year = []
    content = []
    if len(base) > 1:
        for i in base:
            if 'work' in str(base).lower() or 'experience' in str(base).lower() or 'minimum' in str(base).lower():
                work.append(i)
                content.append(i)
            else:
                #print(f'{base}')
                work.append('No Experience 0 years')
                content.append(base[0])
        
    else:
        if 'work' in str(base).lower() or 'experience' in str(base).lower() or 'minimum' in str(base).lower():
            work.append(base[0])
            content.append(base)
        else:
            #print(f'{base}')
            work.append('No Experience 0 years')
            content.append(base)
        
    for i in work[0]:
        for j in i :
            if str(j) in'0123456789':
                year.append(j)
    return year, content

def year_update(data):
    year = []
    content = []
    for index, i in enumerate(data['Link']):
        pagex = requests.get(i)
        soupx = BeautifulSoup(pagex.content, 'html.parser')
        x = [i for i in soupx.find_all('li') if 'year' in str(i)]
        #print(index)
        year.append(years(x)[0])
        content.append(years(x)[1])
    return year, content

def year_clean(data):
    dura = []
    for i in data.Year:
        if len(i) > 1:
            if int(i[1]) == 0:
                dura.append(str(i[0])+str(i[1]))
            else:
                dura.append(str(i[0]) +"-"+str(i[1]))
        else:
            if i != []:
                dura.append(i[0])
            else:
                dura.append(0)
    return dura

def content(data):
    edu = []
    for val in data['Content']:
        for i in val:
            for j in i:
                edu.append(j)
    me = []
    for val in edu[:len(data.Content)]:
        if '<li>' in str(val):
                me.append(str(val).split('>')[1].split('<')[0])
        else:
            me.append(val)
    #print(len(me) - len(data.Content))

    if len(me) < len(data.Content):
      data = data.iloc[:len(me)]
      data['Content'] = me

    else:
      data['Content'] = me

    return data

def location(data):
    locat = []
    for index, url in enumerate(data['Link']):
        pagey = requests.get(url)
        soupy = BeautifulSoup(pagey.content, 'html.parser')
        loc = [i for i in soupy.find_all('p') if 'location' in str(i).lower()]
        if loc != []:
            mee = [i for i in BeautifulSoup(str(loc[0]),features="lxml").get_text().split('\n') if 'location' in i.lower()][0].split('\r')[0].split(':')[-1]
            locat.append(mee)
        else:
            locat.append('No Location')
    return locat

def update_lc(data):
    lc = []
    for val in data['Location']:
        if 'abuja' in val.lower():
            lc.append('Abuja')
        elif 'lagos' in val.lower():
            lc.append('Lagos')
        else:
            lc.append('No Location')
    return lc


def description(data):
    desc = []
    for index, url in enumerate(data['Link']):
        yy = []
        cv = []
        page = requests.get(url).text
        soup = BeautifulSoup(page, features="lxml")
        des = soup.find("div", {"class":"mycase4"})

        for i in des.find_all('ul'):
            yy.append(str(i).replace('<li>', '** ').replace('</li>', '').replace('</ul>', '').replace('<ul>', ''))

        for i in des.find_all('p'):
            cv.append(str(i).replace('<p>', '** ').replace('</p>', '').replace('</strong>', '').replace('<strong>', '').replace('<br/>', ' '))
        yy.append(cv[0])
        
        desc.append(yy[0])
        #print(index)
        
    return desc

def data_config():
    num = int(input('Enter the number of pages you would want to scrape: '))

    col = ['Title', 'Link', 'Content', 'Location', 'Job Information']
    new_df = pd.DataFrame(columns=col)

    for i in range(num):
        url = f'https://www.hotnigerianjobs.com/role/350/{i}/'
        load = 'data_' + str(i)
        load = web_scraper(url)
        new_df = pd.concat([new_df, load]).reset_index(drop=True)
        print(f'{100*((i+1)/num)}% of Data Loaded')
        print(100*'=' + '\n')
    new_df = new_df[col]
    print('We have completed web scraping')
    return new_df


def data_saver(dataframe):
    print('Time to save our Data')
    name = input("Enter the name you want to save your file with: ")
    dataframe.to_csv(f'{name}.csv', index=False)
    print('Dataset has been saved to present working directory')

if __name__ == '__main__':
    dataset = data_config()
    data_saver(dataset)
