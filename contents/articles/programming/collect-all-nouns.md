---
title: Collect all nouns in hungarian
tags: web, hack, python, search
date: 2015-10-24
collection: articles
layout: article.html
snippet: I had to create a searchable noun list in hungarian without any publicly available word list that I can easily download.
---


Hopefully, there is a <a href="https://hu.wiktionary.org/wiki/Kategória:magyar_főnevek" target="_blank">hungarian wiki dictionary</a>
that contains all words in hungarian, and it has a noun filter. It can show the nouns breaked.
Instead of manually copying the pages content for the available 200 pages, I fired up my two favorite
python library: _BeautifulSoup4_ and _Requests_.

The nouns on the wiki page were arranged into a table, so I had to extract the words from the `<li></li>`
tags from the html file, downloaded via a web request using the _Requests_ library and created a soup
from it with _BeautifulSoup4_.

The whole process was arranged into an infinite while loop. It will run until a valid next page link
 can be found. Not the best solution, but hey, it was just a scipt :) Inside this while loop, there is a
 loop that will collect the words into a list. The delimiter for this inner loop was a common
 word (magyar szótár), that was present on every page after the last listed noun.

``` 
import requests
from bs4 import BeautifulSoup
import json

words = []

def main():
    next_link = 'https://hu.wiktionary.org/wiki/Kategória:magyar_főnevek'
    try:
        while(1):
            r = requests.get(next_link)
            if r.status_code != 200:
                break
            soup = BeautifulSoup(r.text, 'html.parser')
            extract_words_from_soup(soup)
            with open('words.json', 'w') as outfile:
                json.dump(words, outfile)
            next_link = 'https://hu.wiktionary.org' + \
                        soup.find('a', string='következő oldal')['href']
            print('Word count: {} next_link: {}'.format(len(words), next_link))
    except TypeError:
        print('\nFinished with {} words'.format(len(words)))

def extract_words_from_soup(soup):
    for li in soup.find_all('li'):
        try:
            word = li.a.string
            if word == 'magyar szótár':
                break
            if word != 'magyar főnévi alakok':
                words.append(word)
        except:
            pass

if __name__ == '__main__':
    main()
```

During the process, I printed out every next link the script was found, so I had a feedback where the script
was in the alphabet. As you can see, the last log was an exception printout, indicating that the script could
not parse the next link from the html file.

``` 
Word count: 200 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=adenokarcin%C3%B3ma#mw-pages
Word count: 400 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=agr%C3%A1rt%C3%B6rv%C3%A9ny#mw-pages
Word count: 600 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=akaszt%C3%B3fahumor#mw-pages
Word count: 800 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=alapilletm%C3%A9ny#mw-pages
Word count: 1000 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=almaexport#mw-pages
Word count: 1200 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=android#mw-pages
Word count: 1400 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=anyak%C3%B6nyv#mw-pages
Word count: 1600 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=aranymetsz%C3%A9s#mw-pages
Word count: 1800 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=assz%C3%B3#mw-pages
Word count: 2000 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=aut%C3%B3busz#mw-pages
Word count: 2200 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=bakkecske#mw-pages
Word count: 2400 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=bark%C3%B3ca#mw-pages
Word count: 2600 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=bej%C3%A1r%C3%A1s#mw-pages
Word count: 2800 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=beteg+bor#mw-pages
Word count: 3000 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=bifsztek#mw-pages
Word count: 3200 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=bodob%C3%A1cs#mw-pages
Word count: 3400 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=borocska#mw-pages
Word count: 3600 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=bujt%C3%A1s#mw-pages
Word count: 3800 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=b%C3%A1nyakavics#mw-pages
Word count: 4000 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=b%C3%A9ket%C3%B6rekv%C3%A9s#mw-pages
Word count: 4200 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=b%C3%B6lcs%C3%A9szdoktor#mw-pages
Word count: 4400 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=b%C5%B1v%C3%B6let#mw-pages
Word count: 4600 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=ciszterna#mw-pages
Word count: 4800 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=csecs#mw-pages
Word count: 5000 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=csillagt%C3%A9rk%C3%A9p#mw-pages
Word count: 5200 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=csukl%C3%A1s#mw-pages
Word count: 5400 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=cukorm%C3%A1z#mw-pages
Word count: 5600 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=darukezel%C5%91#mw-pages
Word count: 5800 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=dics%C3%A9ret#mw-pages
Word count: 6000 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=dodzsem#mw-pages
Word count: 6200 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=d%C3%A1rid%C3%B3#mw-pages
Word count: 6400 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=efavirenz#mw-pages
Word count: 6600 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=elemelked%C3%A9s#mw-pages
Word count: 6800 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=eln%C3%B6kl%C3%A9s#mw-pages
Word count: 7000 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=el%C5%91v%C3%A1lad%C3%A9k#mw-pages
Word count: 7200 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=epicillin#mw-pages
Word count: 7400 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=etil%C3%A9n#mw-pages
Word count: 7600 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=fakalap%C3%A1cs#mw-pages
Word count: 7800 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=fegyverenged%C3%A9ly#mw-pages
Word count: 8000 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=felford%C3%ADt%C3%A1s#mw-pages
Word count: 8200 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=fenntart%C3%A1s#mw-pages
Word count: 8400 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=flam%C3%B3#mw-pages
Word count: 8600 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=ford%C3%ADt%C3%B3#mw-pages
Word count: 8800 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=fuvaroz%C3%A1s#mw-pages
Word count: 9000 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=f%C3%A9rfiszab%C3%B3#mw-pages
Word count: 9200 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=f%C3%BCrd%C5%91mester#mw-pages
Word count: 9400 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=gabonap%C3%A1linka#mw-pages
Word count: 9600 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=gikszer#mw-pages
Word count: 9800 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=gusztus#mw-pages
Word count: 10000 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=gy%C3%A1szeset#mw-pages
Word count: 10200 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=g%C3%A9mkapocs#mw-pages
Word count: 10400 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=haditud%C3%B3s%C3%ADt%C3%B3#mw-pages
Word count: 10600 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=haj%C3%B3padl%C3%B3#mw-pages
Word count: 10800 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=hang#mw-pages
Word count: 11000 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=hat%C3%A1reset#mw-pages
Word count: 11200 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=herer%C3%A1k#mw-pages
Word count: 11400 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=hold%C3%A9v#mw-pages
Word count: 11600 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=husztaj#mw-pages
Word count: 11800 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=h%C3%ADmz%C5%91n%C5%91#mw-pages
Word count: 12000 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=h%C5%B1b%C3%A9ris%C3%A9g#mw-pages
Word count: 12200 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=imak%C3%B6nyv#mw-pages
Word count: 12400 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=iparcikk#mw-pages
Word count: 12600 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=izomr%C3%A1ndul%C3%A1s#mw-pages
Word count: 12800 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=juhb%C5%91r#mw-pages
Word count: 13000 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=j%C3%BCan#mw-pages
Word count: 13200 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=kantni#mw-pages
Word count: 13400 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=karrierizmus#mw-pages
Word count: 13600 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=kelmefest%C5%91#mw-pages
Word count: 13800 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=ker%C3%A9kp%C3%A1rlop%C3%A1s#mw-pages
Word count: 14000 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=kimutat%C3%A1s#mw-pages
Word count: 14200 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=ki%C3%BAt#mw-pages
Word count: 14400 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=kompasz#mw-pages
Word count: 14600 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=korm%C3%A1nyker%C3%A9k#mw-pages
Word count: 14800 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=kubista#mw-pages
Word count: 15000 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=k%C3%A1lyhab%C3%A9l%C3%A9s#mw-pages
Word count: 15200 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=k%C3%A9ssz%C3%BAr%C3%A1s#mw-pages
Word count: 15400 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=k%C3%B6lts%C3%A9g-el%C5%91ir%C3%A1nyzat#mw-pages
Word count: 15600 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=k%C3%B6sz%C3%B6r%C5%B1s#mw-pages
Word count: 15800 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=k%C3%BAria#mw-pages
Word count: 16000 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=lak%C3%A1s%C3%ADns%C3%A9g#mw-pages
Word count: 16200 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=lend%C3%BClet#mw-pages
Word count: 16400 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=limlom#mw-pages
Word count: 16600 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=l%C3%A1gy#mw-pages
Word count: 16800 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=l%C3%A9p%C3%A9s#mw-pages
Word count: 17000 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=mad%C3%A1rtej#mw-pages
Word count: 17200 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=mangalica#mw-pages
Word count: 17400 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=megfigyel%C5%91#mw-pages
Word count: 17600 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=mell%C3%A9khere+feje#mw-pages
Word count: 17800 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=methemoglobin#mw-pages
Word count: 18000 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=mongol#mw-pages
Word count: 18200 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=munkanap#mw-pages
Word count: 18400 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=m%C3%A1zol%C3%B3#mw-pages
Word count: 18600 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=m%C5%B1ipar#mw-pages
Word count: 18800 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=napelem#mw-pages
Word count: 19000 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=nevel%C5%91n%C5%91#mw-pages
Word count: 19200 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=nyirokmirigy#mw-pages
Word count: 19400 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=n%C3%A9pbolond%C3%ADt%C3%A1s#mw-pages
Word count: 19600 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=okirat-hamis%C3%ADt%C3%A1s#mw-pages
Word count: 19800 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=orrnyereg#mw-pages
Word count: 20000 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=pajzs#mw-pages
Word count: 20200 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=parkol%C3%B3#mw-pages
Word count: 20400 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=perzsa#mw-pages
Word count: 20600 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=pl%C3%A9b%C3%A1nos#mw-pages
Word count: 20800 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=prakker#mw-pages
Word count: 21000 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=puncsost%C3%A1l#mw-pages
Word count: 21200 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=p%C3%A1rt%C3%A9p%C3%ADt%C3%A9s#mw-pages
Word count: 21400 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=rabl%C3%B3barlang#mw-pages
Word count: 21600 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=relativit%C3%A1selm%C3%A9let#mw-pages
Word count: 21800 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=riad%C3%B3ztat#mw-pages
Word count: 22000 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=rudli#mw-pages
Word count: 22200 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=r%C3%B3zsabimb%C3%B3#mw-pages
Word count: 22400 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=sebhely#mw-pages
Word count: 22600 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=skorpi%C3%B3#mw-pages
Word count: 22800 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=sporttev%C3%A9kenys%C3%A9g#mw-pages
Word count: 23000 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=szaft#mw-pages
Word count: 23200 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=szecesszi%C3%B3#mw-pages
Word count: 23400 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=szerelmeslev%C3%A9l#mw-pages
Word count: 23600 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=sziszt%C3%A9ma#mw-pages
Word count: 23800 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=szulf%C3%A1t#mw-pages
Word count: 24000 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=sz%C3%A9ler%C5%91ss%C3%A9g#mw-pages
Word count: 24200 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=sz%C3%B3kapcsolat#mw-pages
Word count: 24400 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=sz%C5%91r#mw-pages
Word count: 24600 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=s%C3%B6r%C3%B6z%C5%91#mw-pages
Word count: 24800 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=tankhaj%C3%B3#mw-pages
Word count: 25000 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=tekn%C5%91sb%C3%A9kap%C3%A1nc%C3%A9l#mw-pages
Word count: 25200 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=tervsz%C3%A1m#mw-pages
Word count: 25400 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=toj%C3%A1s%C3%A9tel#mw-pages
Word count: 25600 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=tudatosul%C3%A1s#mw-pages
Word count: 25800 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=t%C3%A1vol%C3%ADt%C3%B3+ideg#mw-pages
Word count: 26000 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=t%C3%B6rt%C3%A9n%C3%A9s#mw-pages
Word count: 26200 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=t%C5%B1zolt%C3%B3osztag#mw-pages
Word count: 26400 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=uzsora#mw-pages
Word count: 26600 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=varj%C3%BAleves#mw-pages
Word count: 26800 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=veszetts%C3%A9g#mw-pages
Word count: 27000 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=vir%C3%A1gcsend%C3%A9let#mw-pages
Word count: 27200 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=vulvekt%C3%B3mia#mw-pages
Word count: 27400 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=v%C3%A9gagy#mw-pages
Word count: 27600 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=v%C3%ADzibetegs%C3%A9g#mw-pages
Word count: 27800 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=zajog#mw-pages
Word count: 28000 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=zugev%C5%91#mw-pages
Word count: 28200 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=%C3%A1gy%C3%BAnasz%C3%A1d#mw-pages
Word count: 28400 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=%C3%A1llom%C3%A1s%C3%A9p%C3%BClet#mw-pages
Word count: 28600 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=%C3%A1rny%C3%A9kol%C3%A1s#mw-pages
Word count: 28800 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=%C3%A1tlageredm%C3%A9ny#mw-pages
Word count: 29000 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=%C3%A9letnagys%C3%A1g#mw-pages
Word count: 29200 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=%C3%A9rv%C3%A9nyes%C3%ADt%C3%A9s#mw-pages
Word count: 29400 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=%C3%B3rafed%C3%A9l#mw-pages
Word count: 29600 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=%C3%B6r%C3%B6kk%C3%A9val%C3%B3s%C3%A1g#mw-pages
Word count: 29800 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=%C3%BAton%C3%A1ll%C3%B3#mw-pages
Word count: 30000 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=%C3%BCvegpoh%C3%A1r#mw-pages
Word count: 30200 next_link: https://hu.wiktionary.org/w/index.php?title=Kateg%C3%B3ria:magyar_f%C5%91nevek&pagefrom=%C5%91szap%C3%B3#mw-pages

Finished with 30248 words
```

