
import rpa as r
import pyautogui as pag

address = pag.prompt('Enter address')
screenshotname = pag.prompt('Screenshot name')
try:
	r.init(visual_automation=True,chrome_browser=True)
	r.url('http://10.13.218.247/go360rogersviewer/')
	r.type('//*[@id="username"]','craig.huckson')

	r.type('//*[@id="password"]','locates1')

	r.click('//*[@id="loginform"]/div[3]/div[2]/div/button')
	r.wait(5)
	r.hover('search.png')
	r.click('//*[@id="form_marqueezoom_btn"]')
	r.click('//*[@id="form_btn"]') #search button

	r.click('//*[@id="addressSearchInput"]')
	r.type('//*[@id="addressSearchInput"]',address) # address search input

	r.click('//*[@id="id_search_div"]/div[1]/table/tbody/tr[2]/td[4]/a') #address search icon

	r.wait(3)

	r.snap(page,f'{screenshotname}.png')

	r.ask('Done. Press any key to finish')


finally:
	r.close()