from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier

import numpy as np


url = 'https://game-tournaments.com/overwatch/team/ex-oblivione'
word = 'ExO'
pages = 7

def win_procent(url,word,pages):
    win = []
    loss = []
    for i in range(1,pages+1):
        try:
            ua = dict(DesiredCapabilities.CHROME)
            options = webdriver.ChromeOptions()
            options.add_argument('headless')
            options.add_argument('window-size=1920x935')
            driver = webdriver.Chrome(chrome_options=options)
            driver.get(url)
            driver.find_element(By.LINK_TEXT, str(i)).click()
            html = driver.page_source.encode("utf-8").decode()

            soup = BeautifulSoup(html, 'lxml')

            span = soup.find_all('span', class_='mbutton tresult')

            href = soup.find_all('a',class_='mlink')

            def scores(span,gets):
                score = []
                for i in span:
                    score.append(i.get(gets))
                
                return score

            score = scores(span,'data-score')
            title = scores(href,'title')

            def alling(title,word):
                all = []
                for i in range(len(title)):
                    titles = title[i].split()
                    if titles[1] != word:
                        a = titles[1]
                        b = titles[-1]
                        all.append((b,a))
                    else:
                        all.append((titles[1],titles[-1]))
                return all

            titles = alling(title,word)

            def going(score,yes=False):
                win = []
                loss = []
                for i in range(len(titles)):
                    try:
                        scores = score[i].split(':')
                        
                        if yes == True:
                            scores.sort(reverse=True)
                        
                        win.append(int(scores[0]))
                        loss.append(int(scores[1]))
                    except:
                        None
                return (win,loss)

            one, two = going(score,True)

            for i in range(len(one)):
                win.append(one[i])
                loss.append(two[i])
        except:
            break

    clf = RandomForestClassifier(20,max_depth=10,min_samples_leaf=2,min_samples_split=10,random_state=0)
    knn = MultiOutputClassifier(clf,n_jobs=2)
    knn.fit(np.array([win]),np.array([loss]))

    predict = knn.predict(np.array([win]))
    output = round((sum(predict[0])/sum(win+loss))*100,2)
    return (f'{output} %')

print(win_procent(url,word,pages))