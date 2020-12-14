import pandas as pd
from bs4 import BeautifulSoup
import requests
import os
from splinter import Browser
from flask import Flask, render_template


# Set up browser
def init_browser():
    executable_path = {"executable_path": 'C:\ChromeDriver\chromedriver.exe'}
    return Browser("chrome", executable_path, headless=False)



# Master scrape function to move everything to Mongo
def scrape():

    master_scrape_dict = {}

    master_scrape_dict["mars_news"] = mars_news()
    master_scrape_dict["jpl_image"] = jpl_image()
    master_scrape_dict["mars_facts"] = mars_facts()
    master_scrape_dict["mars_hemi"] = mars_hemi()

    return master_scrape_dict





# Mars News - for more detail see jupyter notebook
def mars_news():
    browser = init_browser()
    results_dict = {}

    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    results = soup.find("div", class_="list_text")
    results_dict["news_title"] = results.find("div", class_="content_title").get_text()
    results_dict["news_p"] = results.find("div", class_="article_teaser_body").get_text()

    return results_dict



# JPL Mars Space Image - for more detail see jupyter notebook
def jpl_image():
    browser = init_browser()
    
    url_jpl = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_jpl)

    html_jpl = browser.html
    soup_jpl = BeautifulSoup(html_jpl, 'html.parser')

    results_jpl = soup_jpl.find("div", class_="carousel_container")
    results_jpl_v2 = results_jpl.find("article", class_="carousel_item")["style"].replace('background-image: url(','').replace(');', "")[1:-1]
    featured_image_url = "https://www.jpl.nasa.gov" + results_jpl_v2

    return featured_image_url



# Mars Facts - for more detail see jupyter notebook
def mars_facts():
    browser = init_browser()

    url_facts = 'https://space-facts.com/mars/'
    tables = pd.read_html(url_facts)

    mars_facts_df = tables[0]
    mars_facts_df.columns = ["Description", "Mars"]
    mars_facts_df = mars_facts_df.set_index("Description")
    html_table = mars_facts_df.to_html()
    mars_facts_fin = html_table.replace('\n', '')

    return mars_facts_fin


# Mars Hemispheres - for more detail see jupyter notebook
def mars_hemi():
    browser = init_browser()

    url_hemi = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_hemi)

    html_hemi = browser.html
    soup_hemi = BeautifulSoup(html_hemi, 'html.parser')
    results_hemi = soup_hemi.find_all("div", class_="item")

    hemi_list = []

    for qtr in results_hemi:
        title = qtr.find("h3").text
        hemi_link = "https://astrogeology.usgs.gov" + qtr.find("a", class_="itemLink product-item")["href"]
        browser.visit(hemi_link)
        html_hemi_link = browser.html
        soup_hemi_link = BeautifulSoup(html_hemi_link, 'html.parser')
        hemi_link_v2 = soup_hemi_link.find("div", class_="downloads")
        img_url = hemi_link_v2.find("a")["href"]
        hemi_list.append({"title": title, "img_url": img_url})

    return hemi_list


