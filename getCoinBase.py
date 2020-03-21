from urllib import request
import re
from bs4 import BeautifulSoup

saveNowPagePath = "./nowPage.txt"
saveCoinBasePath = "./blockChainCoinBase.txt"
nowPage = 0;
okFlag = "OK";

def readNowPage():
	global nowPage;
	fr = open(saveNowPagePath,'r', encoding='utf-8');
	nowPage = int(fr.readlines()[0]);
	#print(nowPage)
	fr.close();

def saveNowPage():
	fw = open(saveNowPagePath,'w', encoding='utf-8');
	fw.write(str(nowPage));
	fw.close();
	
def saveCoinBase(strCoinBase):
	fw = open(saveCoinBasePath,'a+', encoding='utf-8');
	fw.write(strCoinBase);
	fw.close();
	
def getCoinBase(req):
	global nowPage;
	global okFlag;
	try:
		with request.urlopen(req,timeout=15) as f:
			okFlag = f.reason
			print(f.reason+" "+str(nowPage)+":\t\t",end = "")
			if(f.reason == "OK"):
				soup = BeautifulSoup(f.read().decode("utf-8"),"html.parser")
				soupList = soup.find_all('textarea', class_='form-control-sm block__textarea')
				for item in soupList:
					print(item.string)
					saveCoinBase(f.reason+" "+str(nowPage)+":\t\t"+item.string+"\n")
					nowPage = nowPage+1;
					saveNowPage();
	except BaseException as e:
		print("网络超时，重新继续");
		
		
def getCoinBaseReq(page):
	url = "https://blockchair.com/bitcoin/block/"+str(page);
	req = request.Request(url)
	req.add_header("User-Agent","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36");
	return req;
	
def main():		
	while(okFlag=="OK"):
		readNowPage();
		getCoinBase(getCoinBaseReq(nowPage));
	print("更新完成");

	
main();
