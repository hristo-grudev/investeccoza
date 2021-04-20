import json

import scrapy

from scrapy.loader import ItemLoader
from w3lib.html import remove_tags

from ..items import InvesteccozaItem
from itemloaders.processors import TakeFirst
import requests

url = "https://www.investec.com/bin/search/elasticsearch?r=chSingleArticleListingArticles"

payload="{\"id\":\"dotcom-articles\",\"params\":{\"sortby\":\"datearticle\",\"sortorder\":\"\",\"from\":0,\"size\":9999,\"localefilter\":\"en_za\",\"sitesourcefilter\":\"\",\"pagetypefilter\":\"\",\"tagsfilter\":[\"dotcom:content-hub-tags/content-hub-category/investing\",\"dotcom:content-hub-tags/content-hub-category/markets-and-economy\"],\"tagsandfilter\":[],\"datecreated.min\":\"\",\"datecreated.max\":\"\",\"includepath\":[\"/content/dotcom/en_za/focus\"],\"excludetags\":[\"dotcom:content-hub-tags/newsletter/brexit\"],\"tagsort\":{},\"highlightsarticle\":[\"\"],\"excludedocs\":[],\"excludepages\":[\"/content/dotcom/en_za.html\",\"/content/microsites/impact/en_za.html\",\"/content/microsites/ifacontent/en_za.html\"],\"returnedfields\":[\"_id\",\"tagtitles\",\"imagedesktop\",\"imageeditorspick\",\"excerpt\",\"imagelisting\",\"video\",\"podcast\",\"includedate\",\"read\",\"displaydatearticle\",\"podcasthours\",\"podcastminutes\",\"videohours\",\"videominutes\",\"readhours\",\"readminutes\",\"highlightsarticle\",\"author\",\"type\",\"pageurl\",\"datecreated\",\"sitesource\",\"pagetype\",\"tags\",\"imageurl\",\"content\",\"locale\",\"title\",\"displaydatecreated\",\"rawtags\",\"tagtitles\",\"externalsite\",\"toplines\",\"primarytagtitle\",\"dcheading\",\"primarytag\"],\"sourcefields\":[],\"getsuggest\":true,\"gethighlight\":true,\"getaggregations\":true,\"pinarticlefilter\":[\"\"],\"editorspickfilter\":[\"\"],\"pinseriesfilter\":false,\"highlightsarticlefilter\":[\"\"]}}"
headers = {
  'authority': 'www.investec.com',
  'pragma': 'no-cache',
  'cache-control': 'no-cache',
  'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
  'accept': 'application/json, text/plain, */*',
  'sec-ch-ua-mobile': '?0',
  'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36',
  'content-type': 'application/json',
  'origin': 'https://www.investec.com',
  'sec-fetch-site': 'same-origin',
  'sec-fetch-mode': 'cors',
  'sec-fetch-dest': 'empty',
  'referer': 'https://www.investec.com/en_za.html',
  'accept-language': 'en-US,en;q=0.9,bg;q=0.8',
  'cookie': 's_ecid=MCMID%7C36646105356360524191322424761042891896; _ga=GA1.2.619859221.1615878421; _fbp=fb.1.1615878423770.999134707; _gcl_au=1.1.459747009.1615878426; __cfduid=d84f6a8b0184484d9cf4a12011ba6b7791618476279; _gid=GA1.2.347549241.1618918614; _gat=1; AMCVS_38AC7FBA57E2AF467F000101%40AdobeOrg=1; AMCV_38AC7FBA57E2AF467F000101%40AdobeOrg=870038026%7CMCIDTS%7C18738%7CMCMID%7C36646105356360524191322424761042891896%7CMCAAMLH-1619523414%7C6%7CMCAAMB-1619523414%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1618925814s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C5.0.0; s_dfa=invbnkdigitalprod; s_vnum=1621068282087%26vn%3D4; s_invisit=true; s_cc=true; s_ppn=DotCom_en_za%2Ffocus%2Fmoney%2Fretirement-reforms-impact-on-your-provident-fund_EN_prod; s_getNewRepeat=1618918644488-Repeat; s_ptc=0.01%5E%5E0.00%5E%5E0.00%5E%5E0.00%5E%5E0.33%5E%5E0.01%5E%5E4.09%5E%5E0.04%5E%5E4.49; s_ppvl=DotCom_en_za%2C61%2C61%2C2981%2C1352%2C977%2C1920%2C1080%2C1%2CP; s_ppv=DotCom_en_za%2Ffocus%2Fmoney%2Fretirement-reforms-impact-on-your-provident-fund_EN_prod%2C11%2C11%2C977%2C1920%2C977%2C1920%2C1080%2C1%2CP'
}


class InvesteccozaSpider(scrapy.Spider):
	name = 'investeccoza'
	start_urls = ['http://www.investec.co.za/']

	def parse(self, response):
		response = requests.request("POST", url, headers=headers, data=payload)
		data = json.loads(response.text)
		for post in data['hits']['hits']:
			date = post['fields']['datecreated'][0]
			title = post['fields']['title'][0]
			description = remove_tags(post['fields']['content'][0])

			item = ItemLoader(item=InvesteccozaItem(), response=response)
			item.default_output_processor = TakeFirst()
			item.add_value('title', title)
			item.add_value('description', description)
			item.add_value('date', date)

			yield item.load_item()