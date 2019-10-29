#coding=utf-8
# auther: yubb
from jira.client import JIRA
issue=['MMMJ-32','MMMJ-36']
describe='来自python的测试'
flow_id='431'
jira = JIRA('http://jira.m.com/',basic_auth=('gitlab','123kaibola'))
for issue_id in issue:
    jira.add_comment(issue_id,describe)
    transitions = jira.transitions(issue_id)
    print transitions
    print [(t['id'], t['name']) for t in transitions]
    jira.transition_issue(issue_id,flow_id)
    jira.add_simple_link(issue_id,{"url":"http://www.2339.com/","title":"1234"})

