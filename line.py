from bs4 import BeautifulSoup
import requests
import re
import wget
from subprocess import call
import argparse
# https://sdl-stickershop.line.naver.jp/stickershop/v1/sticker/17941023/IOS/sticker_animation@2x.png
# https://sdl-stickershop.line.naver.jp/stickershop/v1/sticker/17941023/android/sticker.png
def striphtml(data):
    p = re.search(r'\(http.+\);',data)
    return p.group(0)[1:-16].replace("android/sticker.png","IOS/sticker_animation@2x.png")

def getNumber(data):
	p = re.findall(r'\d+', data)
	return p[1]

def crawl(product):
	r = requests.get('https://store.line.me/stickershop/product/' + product + '/zh-Hant')
	soup = BeautifulSoup(r.text, 'html.parser')
	imageArray = soup.findAll("span", { "class" : "mdCMN09Image" })
	i = 1
	call(["mkdir",product])
	for eachSpan in imageArray:
		imageUrl = striphtml(str(eachSpan))
		fileNumber = getNumber(str(imageUrl))
		filename = wget.download(imageUrl)
		saveFilename = filename.replace(".png","").replace("sticker_animation@2x",fileNumber) + ".gif"
		try:
			temp = call(["./apng2gif", filename,  "./" + product + "/" + saveFilename])
		except Exception, e:
			print "error"
			print e;
		print "temp"+str(temp)
		call(["rm","-rf" ,filename])
		i = i + 1

	call(['zip',"-r",product + ".zip", "./" + product])
	call(["rm","-rf" ,"./" + product])


def main():
	product = parse_args().product
	crawl(product)

def parse_args():
    parser = argparse.ArgumentParser(description='product')
    parser.add_argument("-p", "--product", help="product number", type=str, required=True) 
    args = parser.parse_args()
    return args

if __name__ == '__main__':
	main()


