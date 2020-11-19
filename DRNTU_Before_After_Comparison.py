from selenium import webdriver
from PIL import Image
from openpyxl import load_workbook
from tkinter import Tk, messagebox
from tkinter.filedialog import askopenfilename
import os

def generate_image(URL, savepath):
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument('window-size=1280x800') # otherwise set_window_size() below does not work
    driver = webdriver.Chrome('./chromedriver', options=options)
    driver.get(URL)
    total_width = driver.execute_script("return document.body.offsetWidth")
    total_height = driver.execute_script("return document.body.parentNode.scrollHeight")
    driver.set_window_size(total_width, total_height)
    driver.find_element_by_tag_name("body").screenshot(savepath)
    driver.quit()

def combine_image(path1, path2, path3):
    old_site_png = Image.open(path1)
    new_site_png = Image.open(path2)
    combined_width = old_site_png.size[0] + new_site_png.size[0]
    max_height = max(old_site_png.size[1], new_site_png.size[1])
    combined_png = Image.new('RGB',(combined_width, max_height),color='white')
    combined_png.paste(old_site_png, (0,0))
    combined_png.paste(new_site_png, (old_site_png.size[0],0))
    combined_png.save(path3, 'pdf')
    os.remove(path1)
    os.remove(path2)


root = Tk()
root.withdraw()
filepath = askopenfilename()
wb = load_workbook(filepath)
ws = wb.active
counter = 1
for row in ws.values:
    try:
        generate_image(row[0], f'{counter}_old.png')
        generate_image(row[1], f'{counter}_new.png')
        combine_image(f'{counter}_old.png', f'{counter}_new.png', f'./Output/{counter}.pdf')
        counter += 1
    except Exception as e:
        messagebox.showerror('Error', e)





