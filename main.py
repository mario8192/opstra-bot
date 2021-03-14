import time
import pickle
import datetime
import pprint
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# from sheet import work
# driver = webdriver.Chrome()


def setup_login():
    driver.wait = WebDriverWait(driver, 10)
    driver.get("https://opstra.definedge.com")
    # # get cookie
    #
    # with open('cookie.txt', 'wb') as fp:
    #     pickle.dump(driver.get_cookies(), fp)
    with open('cookie.txt', 'rb') as fp:
        loadedCookie = pickle.load(fp)
    for cookie in loadedCookie:
        # print(cookie)
        try:
            cookie['expiry'] = round(cookie['expiry'])
        except:
            pass
        driver.add_cookie(cookie)
    driver.get("https://opstra.definedge.com/options-simulator")
    driver.wait.until(EC.title_contains("Options Simulator"))
    # driver.wait.until(EC.presence_of_element_located(
    #     (By.CSS_SELECTOR, "span.chip__content > a.black--text")))


def next_week(old_date):
    new_date = old_date + datetime.timedelta(7)
    return new_date


month_to_int = {
    "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12
}
int_to_month = {
    1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun", 7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"
}


def select_date_in_datepicker(current_date):
    # click date input
    driver.wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "div.v-menu > div > div > div > div > div> input"))).click()
    time.sleep(0.5)
    # click month header;
    # click year header;
    for i in range(0, 2):
        driver.find_element_by_css_selector(
            "div.v-date-picker-header__value > div > button").click()
        time.sleep(0.5)
    # find and click year
    years = driver.find_elements_by_css_selector("ul.v-date-picker-years > li")
    for i in range(0, len(years)):
        if int(years[i].get_attribute("innerHTML")) == current_date.year:
            # print(current_date.year)
            years[i].click()
            break
    time.sleep(0.5)
    # find and click month
    months = driver.find_element_by_css_selector(
        "div.v-date-picker-table.v-date-picker-table--month.theme--light > table > tbody")
    months = months.find_elements_by_class_name("v-btn__content")
    for i in range(0, len(months)):
        if month_to_int[months[i].get_attribute("innerHTML")] == current_date.month:
            months[i].click()
            break
    time.sleep(0.5)
    # find and click day
    days = driver.find_element_by_css_selector(
        "div.v-date-picker-table.v-date-picker-table--date.theme--light > table > tbody")
    days = days.find_elements_by_class_name("v-btn__content")
    for i in range(0, len(days)):
        if int(days[i].get_attribute("innerHTML")) == current_date.day:
            days[i].click()
            break
    time.sleep(0.5)
    return


def select_stock(stock_name):
    driver.wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "div.layout.fluid.row.wrap.ma-3 > div > div > div.v-input__control"))).click()
    # collect all stock names
    stocks = driver.wait.until(EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, "div.v-select-list.v-card.theme--light > div > div > a > div > div.v-list__tile__title")))
    # search stocks list
    for i in range(0, len(stocks)):
        if stocks[i].get_attribute("innerHTML") == stock_name:
            stocks[i].click()
            break
    return


def datetime_to_expiry_string(current_date):
    new_day = str(current_date.day) if current_date.day > 9 else (
        "0" + str(current_date.day))
    string_date = new_day + \
        int_to_month[current_date.month].upper() + str(current_date.year)
    return string_date


def select_expiry_date(current_date):
    driver.wait.until(EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, "div.layout.fluid.row.wrap.ma-3 > div > div > div.v-input__control")))[1].click()
    # driver.find_elements_by_css_selector(
    #     "div.layout.fluid.row.wrap.ma-3 > div > div > div.v-input__control")[1].click()
    # third_div = driver.wait.until(EC.presence_of_element_located(
    #     (By.CSS_SELECTOR, "div.v-menu__content.theme--light.menuable__content__active.v-autocomplete__content > div.v-select-list.v-card.theme--light"))).find_elements_by_css_selector("div")[2]
    # scroll to show all values
    driver.execute_script(
        'list = document.querySelector("div.v-menu__content.theme--light.menuable__content__active.v-autocomplete__content"); let oldHeight = 0; while (oldHeight != list.scrollHeight) {oldHeight = list.scrollHeight; list.scrollTo(0, list.scrollHeight); }')
    expiry_dates = driver.wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "div.v-menu__content.theme--light.menuable__content__active.v-autocomplete__content > div.v-select-list.v-card.theme--light > div"))).find_elements_by_css_selector("div.v-list__tile__title")
    # expiry_dates = driver.find_elements_by_css_selector("div.v-select-list.v-card.theme--light")[
    #     1].find_elements_by_css_selector("div.v-list__tile__title")
    dest_expiry = datetime_to_expiry_string(current_date)
    print(dest_expiry)
    for i in range(0, len(expiry_dates)):
        print(expiry_dates[i].get_attribute("innerHTML"))
        if expiry_dates[i].get_attribute("innerHTML") == dest_expiry:
            expiry_dates[i].click()
            break
    return


def display_all_rows():
    driver.find_element_by_css_selector(
        "div.v-datatable__actions__select > div > div").click()
    rows = driver.find_elements_by_css_selector(
        "div.v-select-list.v-card.theme--light > div.v-list.theme--light")[0].find_elements_by_class_name("v-list__tile__title")
    for i in range(0, len(rows)):
        if rows[i].get_attribute("innerHTML") == "All":
            rows[i].click()
    return


def fetch_table():
    table_rows = driver.find_elements_by_css_selector(
        "table.v-datatable.v-table.theme--light > tbody > tr")
    spot_price = driver.find_element_by_css_selector(
        "div.layout.fluid.row.wrap.ma-3 > div > span.v-chip.v-chip--label.theme--light.green.lighten-4 > span").get_attribute("innerHTML").split(": ")[1].split("\n")[0]
    datetime_str = driver.find_element_by_css_selector(
        "div.flex.title.text-xs-center.xs12.md2.mt-2.mr-2").get_attribute("innerHTML").strip().split()
    table = []
    for i in range(0, len(table_rows)):
        row = []
        table_columns = table_rows[i].find_elements_by_css_selector("td")
        row.append(table_columns[1].get_attribute("innerHTML"))
        row.append(table_columns[2].get_attribute("innerHTML"))
        a = table_columns[3].get_attribute("innerHTML")
        # # with delta sign
        # row.append(a[0:a.find("<")] + a[a.find(">")+1:a.rfind("<")])
        # row.append(table_columns[4].get_attribute("innerHTML"))
        # a = table_columns[5].get_attribute("innerHTML")
        # row.append(a[0:a.find("<")] + a[a.find(">")+1:a.rfind("<")])
        # without delta sign
        row.append(a[0:a.find("<")])
        row.append(table_columns[4].get_attribute("innerHTML"))
        a = table_columns[5].get_attribute("innerHTML")
        row.append(a[0:a.find("<")])
        row.append(table_columns[6].get_attribute("innerHTML"))
        row.append(table_columns[7].get_attribute("innerHTML"))
        row.append(datetime_str[0])
        row.append(datetime_str[1])
        row.append(spot_price)
        # append date, time, spot price
        table.append(row)
    return table


# CallLTP, CallIV, CallDelta, Strikes, PutDelta, PutIV, PutLTP, Date, Time, Spotprice


def save_to_csv(array_2D):
    with open("array.csv", "a") as my_csv:
        newarray = csv.writer(my_csv, delimiter=',')
        newarray.writerows(array_2D)
    return


def click_5_min():
    driver.find_element_by_css_selector(
        "div.layout.row.wrap.justify-space-around.fill-height.hidden-sm-and-down").find_elements_by_css_selector("button")[4].click()
    return


def get_option_chain():
    driver.find_element_by_css_selector(
        "div.layout.justify-end > button > div.v-btn__content").click()
    return


def wait_for_load():
    # driver.find_element_by_css_selector(
    #     "div.vld-overlay.is-active.is-full-page")
    print("waiting....")
    time.sleep(0.5)
    while driver.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.vld-overlay"))).get_attribute("style") != "display: none;":
        # while driver.wait.until(EC.presence_of_element_located(
        #         (By.XPATH, "/html/body/div/div[21]/main/div/div/div/div/div[2]/div[1]"))).get_attribute("style") == "display: none;":
        # print(".")
        continue
    time.sleep(0.5)
    print("continue")
    return


def loop(start_date, end_date):
    current_date = datetime.date.fromisoformat(start_date)
    # compare datepicker's selected date
    # datepicker_date = driver.find_element_by_css_selector(
    #     "div.v-menu > div > div > div > div > div> input").get_attribute("value").split("-")
    select_stock("BANKNIFTY")
    wait_for_load()
    # while current_date < end_date
    while current_date <= datetime.date.fromisoformat(end_date):
        select_date_in_datepicker(current_date)
        wait_for_load()
        select_expiry_date(current_date)
        wait_for_load()
        for i in range(0, 74):
            # <-------fetch stats-------->
            display_all_rows()
            table = fetch_table()
            # plug in sheet
            work(current_date.isoformat(), table)
            # go next
            try:
                click_5_min()
                get_option_chain()
                wait_for_load()
            except:
                pass
        current_date = next_week(current_date)
        pass


def csv_loop():
    for i in range(0, 74):
        get_option_chain()
        wait_for_load()
        save_to_csv(fetch_table())
        click_5_min()


# if __name__ == "__main__":
#     start_date = "2020-03-12"
#     end_date = "2020-03-26"
#     wait_for_load()
#     loop(start_date, end_date)
