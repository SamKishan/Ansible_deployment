import yaml
import csv
import time 
import os
from netmiko import ConnectHandler

device_1={
    'device_type': 'cisco_ios',
    'ip':'198.51.100.3',
    'username':'netman',
    'password':'netman',
}

device_2={
    'device_type':'cisco_ios',
    'ip':'198.51.100.4',
    'username':'netman',
    'password':'netman',
}

device_3={
    'device_type':'cisco_ios',
    'ip':'198.51.100.5',
    'username':'netman',
    'password':'netman',
}

routers=[device_1,device_2,device_3]
hosts=[]
b={}
with open("convertcsv.csv","rb") as csvfile:
    read=csv.reader(csvfile,delimiter=",")
    for row in read:
        if row[0] not in hosts:
            hosts.append(row[0])
            if("/24" in row[3]):
                netmask="255.255.255.0"
            elif("/32" in row[3]):
                netmask="255.255.255.255"
            elif("/16" in row[3]):
                netmask="255.255.255.255"
            else:
                netmask="255.255.255.0"
            ip_end=row[3].find("/")
            ip=row[3][:ip_end]
            if 'routers' not in b.keys():
                b['routers']=[]
                b['routers'].append({'hostname':row[0],'interfaces':[{'name':row[1]+row[2],'ip':str(ip)+" "+str(netmask),}],'ospf':[{'process_id':row[5],'networks':[{'area':row[6],'ip':str(ip)+" "+str(netmask),}],},],})
            else:
                b['routers'].append({'hostname':row[0],'interfaces':[{'name':row[1]+row[2],'ip':str(ip)+" "+str(netmask),}],'ospf':[{'process_id':row[5],'networks':[{'area':row[6],'ip':str(ip)+" "+str(netmask),}],},],})
            print(str(type(b['routers'])))            
        else:

            if("/32" in row[3]):
                netmask="255.255.255.0"
            elif("/16" in row[3]):
                netmask="255.255.0.0"
            else:
                netmask="255.255.255.0"
            ip_end=row[3].find("/")
            ip=row[3][:ip_end]
            index=0
            
            for i in range(len(b['routers'])):
                if(row[0]==b['routers'][i]['hostname']):
                    index=i
                    break        
            b['routers'][index]['interfaces'].append({'name':row[1]+row[2],'ip':str(ip)+" "+str(netmask),})
            b['routers'][index]['ospf'][0]['networks'].append({'area':row[6],'ip':str(ip)+" "+str(netmask)})
#b={'routers':[{'hostname':'R1','interfaces':[{'name':'Fa0/0','ip':'198.51.100.3 255.255.255.0',},{'name':'Fa1/0','ip':'198.51.101.3 255.255.255.0', },{'name':'loopback1','ip':'10.0.0.1 255.255.255.255', }],'ospf':[{'process_id':1,'networks':[{'area':1,'ip':'198.51.100.3 255.255.255.0',},{'area':1,'ip':'198.51.101.3 255.255.255.0',},{'area':1,'ip':'10.0.0.1 255.255.255.255',}],}],}]}
with open('/etc/ansible/roles/lab9_routers/vars/main.yml', 'w') as outfile:
     yaml.dump(b, outfile, default_flow_style=False)

print("Let's execute the ansible script! Make sure the necessary directories are created. This program does NOT create direcotires")
os.system("ansible-playbook saki8093_lab9.yml --ask-pass")

time.sleep(10)

for i in range(1,4):
    with open("/etc/ansible/configs/lab9/R"+str(i)+".txt") as f:
        net_connect=ConnectHandlder(**routers[i-1])
        for line in f:
            output=net_connect.send_config_command(line)
        
