"""
Selenium + pytest тесты для сайта https://www.python.org

Проверяем базовые пользовательские сценарии:
- главная страница открывается и имеет правильный заголовок;
- работает поиск по сайту;
- работает переход в раздел Downloads;
- работает переход в раздел Documentation;
- на главной странице присутствует блок последних новостей.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BASE_URL = "https://www.python.org"


def wait(driver, timeout=10):
    return WebDriverWait(driver, timeout)


def test_homepage_loads_with_correct_title(driver):
    driver.get(BASE_URL)
    assert "Python" in driver.title
    assert "python.org" in driver.current_url


def test_search_returns_results(driver):
    driver.get(BASE_URL)
    search_box = wait(driver).until(
        EC.presence_of_element_located((By.ID, "id-search-field"))
    )
    search_box.clear()
    search_box.send_keys("pytest")
    search_box.send_keys(Keys.RETURN)

    wait(driver).until(EC.url_contains("/search/"))
    results = wait(driver).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.list-recent-events li"))
    )
    assert len(results) > 0


def test_downloads_navigation(driver):
    driver.get(BASE_URL)
    downloads_link = wait(driver).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#downloads > a"))
    )
    downloads_link.click()

    wait(driver).until(EC.url_contains("/downloads/"))
    assert "Download" in driver.title


def test_documentation_navigation(driver):
    driver.get(BASE_URL)
    docs_link = wait(driver).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#documentation > a"))
    )
    docs_link.click()

    wait(driver).until(EC.url_contains("/doc"))
    assert "Documentation" in driver.title


def test_homepage_has_latest_news_section(driver):
    driver.get(BASE_URL)
    news_header = wait(driver).until(
        EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Latest News')]"))
    )
    assert news_header.is_displayed()
