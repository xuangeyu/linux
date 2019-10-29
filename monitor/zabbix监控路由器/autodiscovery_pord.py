#coding=utf-8
# auther: yubb

#import re
import ConfigParser
import netsnmp
from sender_info import zabbix_sender
#根据snmp获取路由器信息，并发送给zabbix服务器。（包括自动发现启用的端口<有配置ip>,发送进入流量和出口流量信息）

cp=ConfigParser.SafeConfigParser()
cp.read('conf.ini')
zab_ser = cp.get("zabbix",'host')
zab_por = int(cp.get("zabbix",'port'))
ver = cp.get("route",'version')
com = cp.get("route",'public')
hosts  = ["10.0.1.1","10.0.1.3","192.168.1.1"]  #路由器ip
port_types = ["wan","lan","WAN","LAN"]  #路由器端口类型

#定义类获取SNMP数据
class achive_info:
    def __init__(self,snmp_host,snmp_ver,snmp_com,oid):
        self.snmp_host  = snmp_host
        self.snmp_ver = int(snmp_ver)
        self.snmp_com = snmp_com
        self.snmp_oid=oid
    @property
    def achive_snmpdata(self):
        result=netsnmp.snmpwalk(self.snmp_oid,DestHost=self.snmp_host,Version=self.snmp_ver,Community=self.snmp_com)
        return result
#根据主机，所需数据oid和对应的id的oid获取字典
def achive_data(host,data_oid,id_oid):
    info_tuble=achive_info(host,ver,com,data_oid)
    id_tuble=achive_info(host,ver,com,id_oid)
    tmp_dict=dict(zip(info_tuble.achive_snmpdata,id_tuble.achive_snmpdata))
    return tmp_dict
#过滤端口类型
def achive_type_name(host):
    name_id=dict()
    name_id_tmp=achive_data(host,'ifDescr','ifIndex')
    for type in port_types:
        for port_type in name_id_tmp.keys():
            if type in port_type:
                name_id[port_type]=name_id_tmp[port_type]
    return name_id
#发送数据至zabbix服务器
def send_name_ip(namedict,ipdict,in_trafficdict,out_trafficdict,host):
    for name_id in namedict.values():
        for ip_id in ipdict.values():  #对应zabbix发现key的探索规则，发送数据使zabbix自动创建key
            if name_id == ip_id:        #根据同一个id获取对应的端口名字和端口所配ip
                new_name=list(namedict.keys())[list(namedict.values()).index(name_id)] #根据字典的value获取key
                new_ip=list(ipdict.keys())[list(ipdict.values()).index(ip_id)]
                name_ip=str(new_name)+"_"+str(new_ip)
                key='port_name'
                value='{"data":[{"{#NAME_IP}":"%s"}]}' % name_ip
                #调用zabbix发送数据方法将
                zabbix_send=zabbix_sender(zab_ser,zab_por)
                zabbix_send.adddata(host,key,value)
                response=zabbix_send.send()
                print response
                for traffic_id in in_trafficdict.values():   #获取in流量
                    if traffic_id == ip_id:
                        new_in_traffic=list(in_trafficdict.keys())[list(in_trafficdict.values()).index(traffic_id)]
                        key='in_traffic[%s]' % name_ip
                        value=new_in_traffic
                        zabbix_send=zabbix_sender(zab_ser,zab_por)
                        zabbix_send.adddata(host,key,value)
                        response=zabbix_send.send()
                        print response
                for traffic_id in out_trafficdict.values():   #获取out流量
                    if traffic_id == ip_id:
                        new_in_traffic=list(out_trafficdict.keys())[list(out_trafficdict.values()).index(traffic_id)]
                        key='out_traffic[%s]' % name_ip
                        value=new_in_traffic
                        zabbix_send=zabbix_sender(zab_ser,zab_por)
                        zabbix_send.adddata(host,key,value)
                        response=zabbix_send.send()
                        print response

def main():
    for host in hosts:
        name_dict=achive_type_name(host)
        ip_dict=achive_data(host,'ipAdEntAddr','ipAdEntIfIndex')
        in_traffic_dict=achive_data(host,'ifInOctets','ifIndex')
        out_traffic_dict=achive_data(host,'ifOutOctets','ifIndex')
        send_name_ip(name_dict,ip_dict,in_traffic_dict,out_traffic_dict,host)
if __name__ == '__main__':
    main()



'''
def achive_name(host):
        #tmp_dict=dict()
        name_id=dict()
        name_tuble=achive_info(host,ver,com,'ifDescr')
        id_tuble=achive_info(host,ver,com,'ifIndex')
        tmp_dict=dict(zip(name_tuble.achive_snmpdata,id_tuble.achive_snmpdata))
        for type in port_types:
            for port_type in tmp_dict.keys():
                if type in port_type:
                    name_id[port_type]=tmp_dict[port_type]
        return name_id
def achive_ip(host):
    #ip_id=dict()
    ip_tuble=achive_info(host,ver,com,'ipAdEntAddr')
    id_tuble=achive_info(host,ver,com,'ipAdEntIfIndex')
    ip_id=dict(zip(ip_tuble.achive_snmpdata,id_tuble.achive_snmpdata))
    return ip_id
def send_name_ip(namedict,ipdict,host):
    for name_id in namedict.values():
        for ip_id in ipdict.values():
            if name_id == ip_id:
                new_name=list(namedict.keys())[list(namedict.values()).index(name_id)]
                new_ip=list(ipdict.keys())[list(ipdict.values()).index(ip_id)]
                key='port_name'
                value='{"data":[{"{#NAME_IP}":"%s"}]}' % (str(new_name)+"_"+str(new_ip),)
                zabbix_send=zabbix_sender(zab_ser,zab_por)
                zabbix_send.adddata(host,key,value)
                response=zabbix_send.send()
                print response
def main():
    for host in hosts:
        name_dict=achive_name(host)
        ip_dict=achive_ip(host)
        send_name_ip(name_dict,ip_dict,host)
if __name__ == '__main__':
    main()

'''
'''
import Queue
host_queues=Queue.Queue()
data_queues=Queue.Queue()
class achive_info:
    def __init__(self,snmp_host,snmp_ver,snmp_com,snmp_port_type,oid):
        self.snmp_host  = snmp_host
        self.snmp_ver = int(snmp_ver)
        self.snmp_com = snmp_com
        self.snmp_port_type = snmp_port_type
        self.snmp_oid=oid
    def achive_host(self):
        for route_ip in self.snmp_host:
            host_queues.put((route_ip))
    def achive_type(self):
        for port_type in self.snmp_port_type:
            return port_type
    @property
    def achive_snmpdata(self):
        self.achive_host()
        while True:
            try:
                self.snmp_host=host_queues.get(block=False)
                result=netsnmp.snmpwalk(self.snmp_oid,DestHost=self.snmp_host,Version=self.snmp_ver,Community=self.snmp_com)
                print result
            except Queue.Empty:
                break
'''