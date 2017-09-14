import xlwt  
import requests  
import urllib  
import math  
import re  
import json  
  
#通过request获取返回时间  
def get_time(coordinate,mode):  
    api_addr="http://api.map.baidu.com/direction/v1?mode="+mode+"&origin="+coordinate+"&destination=39.905556,116.424722&origin_region=%E5%8C%97%E4%BA%AC&destination_region=%E5%8C%97%E4%BA%AC&output=json&coord_type=wgs84&ak=你的密匙"  
    req=requests.get(api_addr)  
    content=req.content  
    sjson=json.loads(content)  
    if sjson.has_key("result"):  
        #print sjson["status"]  
        if sjson["status"]==0:  
            if mode=="transit":  
                if sjson["result"].has_key("routes"):  
                    if sjson["result"]["routes"][0].has_key("scheme"):  
                        time=sjson["result"]["routes"][0]["scheme"][0]["duration"]  
                    else:  
                        time=sjson["result"]["routes"][0]["duration"]  
                else:  
                    time=0  
            else:  
                if sjson["result"].has_key("routes"):  
                    if sjson["result"]["routes"]==None:  
                        time=0  
                    else:  
                        time=sjson["result"]["routes"][0]["duration"]  
                else:  
                    time=0  
        else:  
            time=0  
    else:  
        time=0  
    print coordinate,time  
    return time  
  
  
def run():  
    #mode是模式driving（驾车）、walking（步行）、transit（公交）、riding（骑行）  
    mode="driving"  
  
    #data 是输入的表格  
    data=xlrd.open_workbook('data0428.xlsx')  
    rtable=data.sheets()[0]  
    nrows=rtable.nrows  
    values=rtable.col_values(0)  
  
    workbook=xlwt.Workbook()  
    #新建输出表格  
    wtable=workbook.add_sheet('driving_zxd_p',cell_overwrite_ok=True)  
    row=0  
      
    for i in range(nrows):  
        s1=str(rtable.row_values(i)[2])+","+str(rtable.row_values(i)[1])  
        time=get_time(s1,mode)  
        wtable.write(row,0,rtable.row_values(i)[0])  
        wtable.write(row,1,rtable.row_values(i)[1])  
        wtable.write(row,2,rtable.row_values(i)[2])  
        wtable.write(row,3,time)  
        row=row+1  
    #保存输出表格  
    workbook.save('driving_zxd_p.xls')  
  
  
if __name__=='__main__':  
    run()  