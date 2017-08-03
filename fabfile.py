from fabric.api import local,run, env,sudo
import logging

sp_root_dir = 'cd ~/oildexgitsource/supplier-portal/ &&'
spr_root_dir = 'cd ~/oildexgitsource/supplier-portal-rest/ &&'

# env.user = 'sprasad'
# env.hosts = ['odx.tecnics.com']

 
tqa_root_dir = 'cd ~/oildexdist/ &&'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def hqa():
    env.user = 'oildexqaadmin'
    env.hosts = ['172.16.3.191']
    env.alias = 'hqa'
    logger.info("Selcted Environment ::: "+env.alias)

def tqa():
    env.user = 'sprasad'
    env.hosts = ['odx.tecnics.com']
    env.alias ='tqa'
    logger.info("Selcted Environment ::: "+env.alias)


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
  local(sp_root_dir + 'scp sp.tar.zip'+env.alias+':oildexdist && rm -r dist *.zip')

def unzipSP():
  logger.info ('extracting supplier portal at TQA....')
  run(tqa_root_dir + 'rm -rf dist && tar -xvzf sp.tar.zip && rm -rf sp.tar.zip')

def deploySP():
  logger.info ('finally deploying supplier portal to TQA.......')
  run(tqa_root_dir + 'rm -rf deploy/sp/* && cp -r dist/*  deploy/sp/')
  logger.info ('Deployed To TQA  !!')      




#Supplier Portal Rest Deployment......

def pullSPR(git_branch):
  local(spr_root_dir+'rm -rf target/universal/* && git fetch origin && git checkout '+git_branch +'&& git pull origin '+git_branch)
  logger.info('deploying SPR to TQA...')

def packSPR():
  local(spr_root_dir+'~/opt/play-2.5.10/bin/activator dist')
  logger.info('packaging SPR with SBT...')

def copySPRtoTQA():
  local(spr_root_dir+'scp target/universal/*.zip '+env.alias+':oildexdist')
  logger.info('Copying SPR to TQA...')

def unzipSPR():
  run(tqa_root_dir+'unzip *.zip -d sprTemp/')
  logger.info('Extracting SPR ..')

def deploySPR():
  stopSPR()
  logger.info('Stopping SPR ...')
  run(tqa_root_dir+'rm -rf deploy/spr/*')
  run(tqa_root_dir+'cd sprTemp && cd supp* && cp -r * ~/oildexdist/deploy/spr/')
  sudo('sudo supervisorctl start spr')
  logger.info('Stopping SPR ...')
  logger.info('SPR deployed ...!!')
  
def cleanTQA():
	sudo(tqa_root_dir + 'rm -rf *.zip sprTemp/*')

def stopSPR():
	sudo('sudo supervisorctl stop spr')


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
  cleanTQA()
  copySPRtoTQA()
  unzipSPR()
  deploySPR()
  





