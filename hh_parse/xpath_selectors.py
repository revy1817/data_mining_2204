xpath_selectors = {
    'pagination': '//div[@class="bloko-gap bloko-gap_top"]//a[@data-qa="pager-next"]/@href',
    'vacancy': '//div[@class="vacancy-serp"]'
               '//a[@data-qa="vacancy-serp__vacancy-title"]/@href',
}
xpath_data_selectors = {
    "title": '//div[@class="vacancy-title"]//h1[@data-qa="vacancy-title"]/text()',
    "salary": '//p[@class="vacancy-salary"]//span[@data-qa="bloko-header-2"]/text()',
    "skills": '//div[@class="bloko-tag-list"]//span[@data-qa="bloko-tag__text"]/text()',
    "description": '//div[@class="vacancy-section"]//div[@data-qa="vacancy-description"]//p/text() | '
                   '//div[@class="vacancy-section"]//div[@data-qa="vacancy-description"]//ul//li/text() | '
                   '//div[@class="vacancy-section"]//div[@data-qa="vacancy-description"]//strong/text()',
    "company": '//div[@class="vacancy-company__details"]//a[@data-qa="vacancy-company-name"]/@href',
}
xpath_company_data_selectors = {
    "title": "//div[@class='company-header']//h1//text()",
    "website": "//a[@data-qa='sidebar-company-site']/@href",
    "activity": "//div[@class='employer-sidebar-block']/p/text()",
    "description": "//div[@data-qa='company-description-text']//text()",
    "vacancies": "//a[@data-qa='vacancy-serp__vacancy-title']/@href",
}
