#coding=utf-8
# auther: yubb
#接收数据发送到jira接口，修改相应内容

from jira.client import JIRA   #pip install jira
jira = JIRA('http://jira.m.com/',basic_auth=('gitlab','123kaibola'))
iss_flow_id='81'
bug_flow_id='31'
# issue=['AM-17',]
# describe='AM-17 AM-11 来自python的测试'
# flow_id='81'
# jira = JIRA('http://jira.m.com/',basic_auth=('gitlab','123kaibola'))
# for issue_id in issue:
#     comments='d6b283a83fbe9d3075aeeac987df94d28edada8e'+' '+describe+'http://www.2339.com/'
#     jira.add_comment(issue_id,comments)
#     transitions = jira.transitions(issue_id)
#     print transitions
#     print [(t['id'], t['name']) for t in transitions]
#     jira.transition_issue(issue_id,flow_id)
#     #jira.add_simple_link(issue_id,{"url":"http://www.2339.com/","title":"1234"})

def change_jira(iss_id,bug_id,commit_id,commit_title,commit_desc,commit_url):
    if len(iss_id):
        for issue_id in iss_id:
            comments=commit_id+' '+commit_desc
            jira.add_comment(issue_id, comments)    #增加备注信息
            jira.transition_issue(issue_id,iss_flow_id)   #修改问题流程状态
            #jira.add_simple_link(issue_id, {"url": commit_url, "title": commit_title})  #添加连接
    if len(bug_id):
        for bug_id in bug_id:
            jira.transition_issue(bug_id, bug_flow_id)