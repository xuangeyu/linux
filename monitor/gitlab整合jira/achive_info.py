#encoding=utf8
# auther: yubb
#本文件接收gitlab_webhooks发送的数据并将其解析
#将解析的数据调用change_jira文件的方法发送给jira接口

import simplejson    #pip install simplejson
import re
from change_jira import change_jira

def re_bug_id(desc):
    bug_patt = r'(?<=#).*?(?=\s)'
    bug_pattern = re.compile(bug_patt)
    bug_id = bug_pattern.findall(desc)
    return bug_id
def re_all_id(desc):
    #iss_patt = r'AM-[0-9]+'
    iss_patt = r'AM-[0-9]+'
    iss_pattern = re.compile(iss_patt)
    all_id = iss_pattern.findall(desc)
    return all_id

class achive_info:
    def __init__(self,data):
        self.commit_status=''
        self.commit_id=''
        self.commit_title=''
        self.commit_desc=''
        self.commit_url=''
        self.bug_id=[]
        self.iss_id=[]
        self.data=data
    def check_status(self):
        data=simplejson.loads(self.data, strict=False)
        self.commit_status=data['object_attributes']['state']
        if self.commit_status == "merged":
            self.commit_id=data['object_attributes']['merge_commit_sha']
            self.commit_title=data['object_attributes']['title']
            self.commit_desc=data['object_attributes']['description']
            self.commit_url=data['object_attributes']['url']
            self.bug_id=re_bug_id(self.commit_desc)
            all_id=re_all_id(self.commit_desc)
            self.iss_id=list(set(all_id)-set(self.bug_id))
            print self.bug_id,self.iss_id
            change_jira(self.iss_id,self.bug_id,self.commit_id,self.commit_title,self.commit_desc,self.commit_url)

#以下为测试数据
#a=achive_info('{"object_kind":"merge_request","user":{"name":"于兵兵","username":"yubingbing","avatar_url":"http://www.gravatar.com/avatar/fcbf6c486a21a1f1326debe099c74024?s=80\u0026d=identicon"},"project":{"name":"redking_test","description":"","web_url":"http://git.xing-ai.net/root/redking_test","avatar_url":null,"git_ssh_url":"git@git.xing-ai.net:root/redking_test.git","git_http_url":"http://git.xing-ai.net/root/redking_test.git","namespace":"root","visibility_level":20,"path_with_namespace":"root/redking_test","default_branch":"master","homepage":"http://git.xing-ai.net/root/redking_test","url":"git@git.xing-ai.net:root/redking_test.git","ssh_url":"git@git.xing-ai.net:root/redking_test.git","http_url":"http://git.xing-ai.net/root/redking_test.git"},"object_attributes":{"id":5788,"target_branch":"master","source_branch":"bran","source_project_id":36,"author_id":75,"assignee_id":null,"title":"奥术大师多","created_at":"2019-08-26 09:38:13 UTC","updated_at":"2019-08-26 09:38:19 UTC","milestone_id":null,"state":"merged","merge_status":"can_be_merged","target_project_id":36,"iid":28,"description":"AM-16 AM-11 #AM-14 #AM-15 1.修改任务状态；2.修改bug状态","position":0,"locked_at":null,"updated_by_id":null,"merge_error":null,"merge_params":{"force_remove_source_branch":null},"merge_when_build_succeeds":false,"merge_user_id":null,"merge_commit_sha":"b38a60d222d770cb8c37c00038303ef0af436fe1","deleted_at":null,"source":{"name":"redking_test","description":"","web_url":"http://git.xing-ai.net/root/redking_test","avatar_url":null,"git_ssh_url":"git@git.xing-ai.net:root/redking_test.git","git_http_url":"http://git.xing-ai.net/root/redking_test.git","namespace":"root","visibility_level":20,"path_with_namespace":"root/redking_test","default_branch":"master","homepage":"http://git.xing-ai.net/root/redking_test","url":"git@git.xing-ai.net:root/redking_test.git","ssh_url":"git@git.xing-ai.net:root/redking_test.git","http_url":"http://git.xing-ai.net/root/redking_test.git"},"target":{"name":"redking_test","description":"","web_url":"http://git.xing-ai.net/root/redking_test","avatar_url":null,"git_ssh_url":"git@git.xing-ai.net:root/redking_test.git","git_http_url":"http://git.xing-ai.net/root/redking_test.git","namespace":"root","visibility_level":20,"path_with_namespace":"root/redking_test","default_branch":"master","homepage":"http://git.xing-ai.net/root/redking_test","url":"git@git.xing-ai.net:root/redking_test.git","ssh_url":"git@git.xing-ai.net:root/redking_test.git","http_url":"http://git.xing-ai.net/root/redking_test.git"},"last_commit":{"id":"9e016eb14974d383a7f00b036687545dd4b4eac3","message":"sadaskd;akd;awowk;j;aldjjlsajdlajd.\n","timestamp":"2019-08-26T17:37:27+08:00","url":"http://git.xing-ai.net/root/redking_test/commit/9e016eb14974d383a7f00b036687545dd4b4eac3","author":{"name":"root","email":"bingbing.yu@2339.com"}},"work_in_progress":false,"url":"http://git.xing-ai.net/root/redking_test/merge_requests/28","action":"merge"},"repository":{"name":"redking_test","url":"git@git.xing-ai.net:root/redking_test.git","description":"","homepage":"http://git.xing-ai.net/root/redking_test"}}')
#a=achive_info('{"object_kind":"merge_request","event_type":"merge_request","user":{"name":"Administrator","username":"root","avatar_url":"https://www.gravatar.com/avatar/e64c7d89f26bd1972efa854d13d7dd61?s=80\u0026d=identicon"},"project":{"id":2,"name":"jira","description":"jira test","web_url":"http://192.168.231.129:8888/root/jira","avatar_url":null,"git_ssh_url":"git@192.168.231.129:root/jira.git","git_http_url":"http://192.168.231.129:8888/root/jira.git","namespace":"Administrator","visibility_level":0,"path_with_namespace":"root/jira","default_branch":"master","ci_config_path":null,"homepage":"http://192.168.231.129:8888/root/jira","url":"git@192.168.231.129:root/jira.git","ssh_url":"git@192.168.231.129:root/jira.git","http_url":"http://192.168.231.129:8888/root/jira.git"},"object_attributes":{"assignee_id":null,"author_id":1,"created_at":"2019-08-23 04:09:09 UTC","description":"MMMJ-32 MMMJ-31 看四大行的地位，数据库的客户宽度，啊大家都来吉大，三打两建大垃圾袋，了大家胜利大街爱；阿萨德卡号地块","head_pipeline_id":null,"id":10,"iid":10,"last_edited_at":null,"last_edited_by_id":null,"merge_commit_sha":"259a49b04c994bd71a810b475ec5c1e3ffdee9e5","merge_error":null,"merge_params":{"force_remove_source_branch":"0"},"merge_status":"can_be_merged","merge_user_id":null,"merge_when_pipeline_succeeds":false,"milestone_id":null,"source_branch":"bran","source_project_id":2,"state":"merged","target_branch":"master","target_project_id":2,"time_estimate":0,"title":"MMMJ-32 MMMJ-31","updated_at":"2019-08-23 04:09:13 UTC","updated_by_id":null,"url":"http://192.168.231.129:8888/root/jira/merge_requests/10","source":{"id":2,"name":"jira","description":"jira test","web_url":"http://192.168.231.129:8888/root/jira","avatar_url":null,"git_ssh_url":"git@192.168.231.129:root/jira.git","git_http_url":"http://192.168.231.129:8888/root/jira.git","namespace":"Administrator","visibility_level":0,"path_with_namespace":"root/jira","default_branch":"master","ci_config_path":null,"homepage":"http://192.168.231.129:8888/root/jira","url":"git@192.168.231.129:root/jira.git","ssh_url":"git@192.168.231.129:root/jira.git","http_url":"http://192.168.231.129:8888/root/jira.git"},"target":{"id":2,"name":"jira","description":"jira test","web_url":"http://192.168.231.129:8888/root/jira","avatar_url":null,"git_ssh_url":"git@192.168.231.129:root/jira.git","git_http_url":"http://192.168.231.129:8888/root/jira.git","namespace":"Administrator","visibility_level":0,"path_with_namespace":"root/jira","default_branch":"master","ci_config_path":null,"homepage":"http://192.168.231.129:8888/root/jira","url":"git@192.168.231.129:root/jira.git","ssh_url":"git@192.168.231.129:root/jira.git","http_url":"http://192.168.231.129:8888/root/jira.git"},"last_commit":{"id":"94c321ce9349c2aacc78673ee7fb79791b1dd7e1","message":"什么也不写都可以，也可以随便写\n","timestamp":"2019-08-23T12:08:52+08:00","url":"http://192.168.231.129:8888/root/jira/commit/94c321ce9349c2aacc78673ee7fb79791b1dd7e1","author":{"name":"root","email":"bingbing.yu@2339.com"}},"work_in_progress":false,"total_time_spent":0,"human_total_time_spent":null,"human_time_estimate":null,"assignee_ids":[],"action":"merge"},"labels":[],"changes":{"state":{"previous":"locked","current":"merged"},"updated_at":{"previous":"2019-08-23 04:09:13 UTC","current":"2019-08-23 04:09:13 UTC"},"total_time_spent":{"previous":null,"current":0}},"repository":{"name":"jira","url":"git@192.168.231.129:root/jira.git","description":"jira test","homepage":"http://192.168.231.129:8888/root/jira"}}')
#a.check_status()
