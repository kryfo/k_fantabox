import json,os


def init_invalidListBuilder():
	datas=["Maya/hq_maya/scripts/fantabox/__init__invalidListBuilder",
		"Maya/hq_maya/scripts/fantabox/test"]
	data_json= json.dumps( datas, indent=4,encoding='GBK')
	file = open(str(os.path.dirname(__file__))+r'\__init__invalidList.json', 'w')
	file.write(data_json)
	file.close()


def py_ListBuilder():
	datas=["/Maya/hq_maya/scripts/userSetup.py",
		"/Maya/hq_maya/scripts/initialmaya.py"]
	data_json= json.dumps( datas, indent=4,encoding='GBK')
	file = open(str(os.path.dirname(__file__))+r'\py_List.json', 'w')
	file.write(data_json)
	file.close()

#build __init__invalidList.json
init_invalidListBuilder()


#buld py_List.json
py_ListBuilder()

