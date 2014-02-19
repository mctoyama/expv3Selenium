    WebDriverWait(driver, doc['timeout']).until( lambda driver: len(driver.window_handles) > 1 )
