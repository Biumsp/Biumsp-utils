import git
import sys
from biumsputils.print import print


class GitWrapper():
    def __init__(self, path):
        self.path = path
        try:
            self.repo = git.Repo(path)
            try:
                self.origin = self.repo.remote("origin")
            except:
                print(f'No remote repository set in {path}\nAdd a remote called "origin" to be able to push', color='orange')

        except git.exc.InvalidGitRepositoryError:
            print(f'Directory "{path}" is not a git repository: initializing', color='orange')
            self.repo = git.Repo.init(path)
            print('Successfully initialized git repository', color='green')
            print(f'No remote repository set in {path}\nAdd a remote called "origin" to be able to push', color='orange')


    def add_(self, file):
        '''Add the specified file'''
        
        try: self.repo.index.add([file])
        except:
            try: 
                self.repo.git.add(all=True)
            except:
                print(f'Git Error: cannot add {file}')
                sys.exit(1)


    def commit(self, file, message):
        '''Add and commit'''
        
        self.add_(file)
        
        try:
            self.repo.index.commit(message)
            message = message.split(sep="\n")[0]
            print(f'Git: commit successful: {message}')
        except:
            print('Git Error: unable to commit')
            sys.exit(1)


    def pull(self, force=False):
        '''Pull from remote'''
        print(f'Git: pull not implemented')


    def push(self):
        '''Push to remote'''

        try:
            self.repo.git.push(self.origin, self.repo.head.ref)
            print('Git: successfully pushed refs to origin')
        except:
            print('Git Error: unable to push to origin')
            sys.exit(1)
