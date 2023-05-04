def get_recipe(recipe_name):
    
    ingredient_list = recipe_text_df[recipe_text_df['title'] == recipe_name]['recipe']\
                                                    .values[0]['Ingredients']
    print("Ingredients:")
    print("----------------------")
    for ingredient in ingredient_list:
        print(ingredient)
    print()
        
    steps = recipe_text_df[recipe_text_df['title'] == recipe_name]['recipe']\
                                            .values[0]['Instructions']
    
    for x in range(len(steps)):
        step = x + 1
        print(f"Step {step}:")
        print("----------------------")
        print(steps[x][f"Step {step}"])
        print("----------------------")
        
def recipe_scrape(url):
    browser.visit(url)
    
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    
    ingredient_tags = soup.find_all('li', class_ = "mntl-structured-ingredients__list-item")
    ingredient_list = []
    for ingredient in ingredient_tags:
        span_tags = ingredient.find_all('span')
        try:
            quantity = span_tags[0].text
        except:
            print('No quantity value')
            break
        try:
            unit = span_tags[1].text
        except:
            print('No unit value')
            break
        try:
            name = span_tags[2].text
        except:
            print('No name value')
            ingredient = f"{quantity} {unit}"
        
        ingredient = f"{quantity} {unit} {name}"
        
        ingredient_list.append(ingredient)
    cooking_instructions = soup.find_all('li', class_ = "comp mntl-sc-block-group--LI mntl-sc-block mntl-sc-block-startgroup")
    
    instr_list = []
    step = 1
    for instructions in cooking_instructions:
        step_label = f"Step {step}"
        instr_dict = {}
        cooking_instructions_text = instructions.find('p').text.strip()

        instr_dict[step_label] = cooking_instructions_text
        instr_list.append(instr_dict)
        step += 1
    
    dict = {}
    dict['Ingredients'] = ingredient_list
    dict['Instructions'] = instr_list
    
    return dict

def recipe_search(search_string,num_of_pages):
    from splinter import Browser
    from bs4 import BeautifulSoup
    import pandas as pd
    import time
    
    recipe_list = []
    title_list = []
    recipe_text_list = []
    string = search_string.replace(' ','+')
    url = f'https://www.allrecipes.com/search?q={string}'
    
    browser.visit(url)
    
    x = range(num_of_pages)
    for _ in x:
        print("-------------------")
        print(f"Starting scrape for page {_+1}")
        print("-------------------")
        
        html = browser.html


        article_soup = BeautifulSoup(html, 'html.parser')
        
        links = article_soup.find_all('a', class_='comp mntl-card-list-items mntl-document-card mntl-card card card--no-image')
        for link in links:
            ratings = link.find_all('div', class_ = 'comp recipe-card-meta')
            if len(ratings) > 0:
                recipe_dict = {}
                recipe_text_dict = {}
                print('found recipe')
                print('storing recipe...')
                
                title = link.find(class_ = 'card__title-text').text
                rating = len(link.find_all(class_ = 'icon icon-star'))
                recipe_url = link.get('href')
                
                recipe_dict['title'] = title
                recipe_dict['rating'] = rating
                recipe_dict['url'] = recipe_url
                                    
                if title in title_list:
                    print('Recipe already found in dictionary')
                else:
                    title_list.append(title)
                    
                    recipe_text_dict['title'] = title
                    recipe_text_dict['recipe'] = recipe_scrape(recipe_url)
                    recipe_text_list.append(recipe_text_dict)
                    
                recipe_list.append(recipe_dict)
            
            else:
                print('article found..skipping')
                
        browser.visit(url)       
        
        if _ == len(x)-1:
            print("-------------------")
            print('Reached the last page...')
            print('All recipes scraped and stored...')
            print("-------------------")
        else:
            try:
                print(browser.url)
                time.sleep(2)
                browser.links.find_by_partial_text('Next').click()
                time.sleep(2)
               
                print("-------------------")
                print("Moving to next page")
                print("-------------------")
                
                print(browser.url)
                url = browser.url
            except:
                print("-------------------")
                print('Reached Except Clause for Next Button...')
                print('All recipes scraped and stored...')
                print("-------------------")
                
                recipe_text_df = pd.DataFrame(recipe_text_list)
                recipe_df = pd.DataFrame(recipe_list)
                recipe_df = recipe_df.drop_duplicates()
                top_recipe_df = recipe_df[recipe_df['rating'] == 5]
                

                return top_recipe_df,recipe_text_df

    recipe_df = pd.DataFrame(recipe_list)
    try:
        recipe_df = recipe_df.drop_duplicates()
    except:
        print('no duplicates')
    top_recipe_df = recipe_df[recipe_df['rating'] == 5]
    
    
    recipe_text_df = pd.DataFrame(recipe_text_list)
    browser.quit()
    return top_recipe_df, recipe_text_df