import json
import os
from datetime import datetime, timezone
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

REPO='Galekee/Octax'
def github_json(endpoint):
    url='https://api.github.com/repos/'+REPO+'/'+endpoint
    headers={'Accept':'application/vnd.github+json','User-Agent':'Octax-QA'}
    if os.environ.get('GITHUB_TOKEN'):
        headers['Authorization']='Bearer '+os.environ['GITHUB_TOKEN']
    with urlopen(Request(url,headers=headers),timeout=6) as response:
        return json.load(response)

@login_required
def dashboard(request):
    data={'title':'QA и CI/CD','repo':REPO,'error':'','workflow_runs':[],'deploy_count':None,'lead_time':None,'change_failure_rate':None,'mttr':None}
    try:
        workflows=github_json('actions/runs?per_page=30')
        runs=workflows.get('workflow_runs',[])
        data['workflow_runs']=[{'name':r['name'],'status':r['status'],'conclusion':r.get('conclusion'),'url':r['html_url'],'created_at':r['created_at']} for r in runs]
    except (HTTPError,URLError,TimeoutError,ValueError,KeyError) as exc:
        data['error']='GitHub API не ответил или ограничил запросы. Проверьте ссылку на репозиторий.'
    # A successful CI workflow is not a production deployment. Never substitute it for DORA metrics.
    return render(request,'delivery/dashboard.html',data)
