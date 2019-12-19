from json import *
from htc import Element, CSS
from github import Github
from threading import Thread
import sys
import time
from markdown2 import markdown
from bs4 import BeautifulSoup, NavigableString

def run_instance(settings):
    if settings['token']:
        git = Github(settings['token'])
    else:
        git = Github(settings['username'],settings['password'])
    
    repo = git.get_repo(settings['repo-name'])
    try:
        lcf = repo.get_contents(settings['site']['md-dir']+'/log.json')
        logs = loads(lcf.decoded_content)
    except:
        print('Log file doesn\'t exist, creating...')
        repo.create_file(settings['site']['md-dir']+'/log.json','Automated creation of log file',dumps({'logs':[]}))
        lcf = repo.get_contents(settings['site']['md-dir']+'/log.json')
        logs = loads(lcf.decoded_content)

    while True:
        files = repo.get_contents(settings['site']['md-dir'])
        for f in files:
            if f.name == 'log.json':
                pass
            elif f.name in logs['logs']:
                pass
            else:
                data = markdown(f.decoded_content)
                cont = repo.get_contents(settings['site']['path-to-index'])
                htmldoc = cont.decoded_content
                soup = BeautifulSoup(htmldoc,'html.parser')
                post_div_tag = soup.select(settings['site']['post-div'])[0]
                post = soup.new_tag('div',attrs={'class':'post-box'})
                post.string = data
                post_div_tag.insert(0,post)
                unpretty = soup.prettify()
                unpretty = unpretty.replace('&lt;','<')
                doc = unpretty.replace('&gt;','>')
                print(doc)
                repo.update_file(settings['site']['path-to-index'],'Automated update - '+str(time.time()),doc,cont.sha)
                logs['logs'].append(f.name)
                repo.update_file(settings['site']['md-dir']+'/log.json','Update completed entries',dumps(logs),lcf.sha)

        time.sleep(settings['check-interval'])
    
        

if __name__ == '__main__':
    with open('config.json','r') as f:
        settings = load(f)

    threads = []
    for i in settings['instances']:
        t = Thread(name=i['name'],target=run_instance,args=[i])
        t.start()
        threads.append(t)
    
    input('Press enter to quit.')
    exit(0)

