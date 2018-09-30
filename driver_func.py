# -*- coding: utf-8 -*-
from selenium.webdriver.common.keys import Keys


def pulllowfunc(btn, times):
    for i in range(1, times):
        btn.send_keys(Keys.DOWN)
        btn.send_keys(Keys.DOWN)
        btn.send_keys(Keys.DOWN)
        btn.send_keys(Keys.DOWN)

    #with open('./page_source', 'wb') as f:
    #f.write(str(self.browser.page_source).encode('utf-8'))



