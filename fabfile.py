from fabric.api import local,run, env,sudo
import logging

sp_root_dir = 'cd ~/oildexgitsource/supplier-portal/ &&'
spr_root_dir = 'cd ~/oildexgitsource/supplier-portal-rest/ &&'
env.user = 'sprasad'
env.hosts = ['odx.tecnics.com']
tqa_root_dir = 'cd ~/oildexdist/ &&'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Supplier Portal Deployment....

def pullSP(git_branch):
  logger.info('pulling latest code from git....')
  local(sp_root_dir + 'git fetch origin && git checkout '+git_branch +'&& git pull origin '+ git_branch)

def packSP():
  logger.info ('packing supplier portal for deployment...')
  local(sp_root_dir + ' ng build --prod --aot --environment=tqa --base-href /supplier/')

def zipSP():
  local(sp_root_dir + 'tar -cvzf sp.tar.zip dist/*')  

def copySPtoTQA():
  logger.info ('sending supplier portal to TQA.........')
  local(sp_root_dir + 'scp sp.tar.zip tqa:oildexdist && rm -r dist *.zip')

def unzipSP():
  logger.info ('extracting supplier portal at TQA....')
  run(tqa_root_dir + 'rm -rf dist && tar -xvzf sp.tar.zip && rm -rf sp.tar.zip')

def deploySP():
  logger.info ('finally deploying supplier portal to TQA.......')
  run(tqa_root_dir + 'rm -rf deploy/sp/* && cp -r dist/*  deploy/sp/')
  logger.info ('Deployed To TQA ------Thank God.....IT DOESNT SUCKS !!!')      




#Supplier Portal Rest Deployment......

def pullSPR(git_branch):
  local(spr_root_dir+'rm -rf target/universal/* && git fetch origin && git checkout '+git_branch +'&& git pull origin '+git_branch)

def packSPR():
  local(spr_root_dir+'~/opt/play-2.5.10/bin/activator dist')

def copySPRtoTQA():
  local(spr_root_dir+'scp target/universal/*.zip tqa:oildexdist')

def unzipSPR():
  run(tqa_root_dir+'unzip *.zip -d spr')

def deploySPR():
  sudo('sudo supervisorctl stop spr')
  run(tqa_root_dir+'rm -rf deploy/spr/*')
  run(tqa_root_dir+'cd spr && cd supp* && cp -r *'+tqa_root_dir+'deploy/spr/')
  sudo('sudo supervisorctl start spr')
  print 'DONE..........'



# Main Deploy...

def sp(git_branch):
  pullSP(git_branch)
  packSP()
  zipSP()
  copySPtoTQA()
  unzipSP()
  deploySP()
  

def spr(git_branch):
  pullSPR(git_branch)
  packSPR()
  copySPRtoTQA()
  unzipSPR()
  #deploySPR()






