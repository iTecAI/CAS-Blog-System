from json import load, loads
from htc import Element, CSS
from github import Github
from threading import Thread
import sys

def run_instance(settings):
    if settings['token']:
        git = Github(settings['token'])
    else:
        git = Github(settings['username'],settings['password'])
    
    repo = git.get_repo(settings['repo-name'])
    logs = loads(repo.get_contents(settings['site']['md-dir']+'/log.json').decoded_content)
    print(logs)

if __name__ == '__main__':
    with open('config.json','r') as f:
        settings = load(f)

    threads = []
    for i in settings['instances']:
        t = Thread(name=i['name'],target=run_instance,args=[i])
        t.start()
        threads.append(t)
    
    input('Press enter to quit.')
    sys.exit(0)

