from selenium.webdriver.common.by import By

IMPORTANT_TAGS = {
    "button", "input", "a",
    "select", "textarea",
    "img", "label"
}

ATTRIBUTES = {
    "id", "class", "name",
    "type", "placeholder",
    "role", "aria-label",
    "href", "src"
}


def scrape_all_elements(driver):
    return driver.find_elements(By.XPATH, "//*")


def clean_element(element):
    attributes = {}

    for attr in ATTRIBUTES:
        value = element.get_attribute(attr)
        if value:
            attributes[attr] = value

    return {
        "tag": element.tag_name,
        "text": element.text.strip(),
        "attributes": attributes,
        "visible": element.is_displayed(),
        "enabled": element.is_enabled(),
        "location": element.location,
        "size": element.size
    }


def filter_element(cleaned_element):
    return cleaned_element["tag"] in IMPORTANT_TAGS
