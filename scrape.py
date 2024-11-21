from playwright.sync_api import sync_playwright

target = "https://grep.app/search?q=Chart.yaml&case=true&filter[lang][0]=YAML&filter[path][0]=charts/"

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(target)
    page.wait_for_load_state("domcontentloaded")

    # Click the load more button
    while page.query_selector(".ant-btn.ant-btn-block"):
        page.click(".ant-btn.ant-btn-block")

    # Note: The query should return 72 elements, however the len(result_container) seems to always be a factor of 10 so I manually added the last 2 to the out.txt

    result_container = page.query_selector_all(
        ".sui-results-container .sui-result__title .result-repo > a"
    )

    links = list({"".join([el.get_attribute("href"), "\n"]) for el in result_container})

    with open("out.txt", "a+") as f:
        f.writelines(links)

    browser.close()
