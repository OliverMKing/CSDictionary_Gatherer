import wikipediaapi
import re
import requests
import mysql.connectormydb = mysql.connector.connect(host="", user="", passwd="", database="")
mc = mydb.cursor()sql="insert into techTerms (term, explaination, url) values (%s, %s, %s)"dict = {}def print_categorymembers(categorymembers, level=0, max_level=10):
   for c in categorymembers.values():
       try:
           print('Category: %s', categorymembers)
           print('entry level: %s', level)
           if not regex.search(c.title):
               name = re.sub(r'\(([^\)]+)\)', '', c.title)
               if dict.get(name) == None:
                   # Primary Key (name)
                   print(name)
                   # Definition
                   definition = c.summary.replace('== References ==', '')
                   print(definition)
                   dict[name] = definition
                   # Page URL
                   url = c.fullurl
                   print(url)
                   mc.execute("select term from techTerms")
                   terms = mc.fetchall()
                   if name not in terms:
                       if len(name) <=255 and len(definition) <= 65535 and len(url) <= 1000:
                           val=(name, definition, url)
                           mc.execute(sql, val)
                           mydb.commit()
                       try:
                           params = {
                               'action': "query",
                               'format': "json",
                               'titles': c.title,
                               'prop': "redirects",
                               'rdprop': "title"
                           }
                           response = requests.get(url="https://en.wikipedia.org/w/api.php", params=params).json()
                           for id in response['query']['pages']:
                               for redirects in response['query']['pages'][id]['redirects']:
                                   # Alternative name
                                   print(redirects['title'])
                                   if requests['title'] not in terms:
                                       if len(redirects['title']) <=255 and len(definition) <= 65535 and len(url) <= 1000:
                                           val=(redirects['title'], definition, url)
                                           mc.execute(sql, val)
                                           mydb.commit()
                       except:
                           print('There are no redirects')
       except:
           print('invalid title or something failed')
       if c.ns == wikipediaapi.Namespace.CATEGORY and level < max_level:
           print_categorymembers(c.categorymembers, level=level + 1, max_level=max_level)wikipedia = wikipediaapi.Wikipedia('en')
regex = re.compile(r'Category|[cC]omparison|List of|Outline of|Template:|Glossary of|Portal:')
category = wikipedia.page("Category:Computing")
print_categorymembers(category.categorymembers)
print("done")
exit()
