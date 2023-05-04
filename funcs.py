# takes recipe_name as arguement, 
# searches recipe_text_df for recipe_name
def get_recipe(recipe_name, recipe_text_df, top_recipes_df):
    
    #pulling the ingredient data from the dictionaries stored in recipe_text_df['recipe']
    ingredient_list = recipe_text_df[recipe_text_df['title'] == recipe_name]['recipe']\
                                                    .values[0]['Ingredients']
    
    print(f"Url: \n{top_recipes_df[top_recipes_df['title'] == recipe_name].values[0][2]}\n")
    print("----------------------")
    #print the ingredient list to the screen
    print("Ingredients:")
    print("----------------------")
    for ingredient in ingredient_list:
        print(ingredient)
    print()

    # pull the cooking instructions data from the dictionaires stored in recipe_text_df['recipe]    
    steps = recipe_text_df[recipe_text_df['title'] == recipe_name]['recipe']\
                                            .values[0]['Instructions']
    
    #print out the cooking steps to the screen
    for x in range(len(steps)):
        step = x + 1
        print(f"\nStep {step}:")
        print("----------------------")
        print(steps[x][f"Step {step}"])
        print("----------------------")


# takes two variables (recipe url, browser) defined in recipe_search() as arguements,
# returns dictionary of recipe data for use in get_recipe()
def recipe_scrape(url,browser):
    from bs4 import BeautifulSoup
    from splinter import Browser
    import pandas as pd
    
    browser.visit(url)
    
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    
    # pull ingredient list elements from html soup
    ingredient_tags = soup.find_all('li', class_ = "mntl-structured-ingredients__list-item")
    ingredient_list = []

    #loop through all list elements and pull out igredient text
    for ingredient in ingredient_tags:

        #span tags hold the text, usually three [quantity, units, name]
        # try except clauses handle exceptions that occur if a li element doesnt have three children elements
        span_tags = ingredient.find_all('span')
        try:
            quantity = span_tags[0].text
        except:
            print('No quantity value -- skipping ingredient')
            break

        try:
            unit = span_tags[1].text
        except:
            # print('No unit value')
            ingredient = f"{quantity}"

        try:
            name = span_tags[2].text
        except:
            # print('No name value for ')
            ingredient = f"{quantity} {unit}"
        
        # store ingredient as string and add it to the list
        ingredient = f"{quantity} {unit} {name}"
        ingredient_list.append(ingredient)

    # pull cooking steps from html soup   
    cooking_instructions = soup.find_all('li', class_ = "comp mntl-sc-block-group--LI mntl-sc-block mntl-sc-block-startgroup")
    

    instr_list = []
    step = 1
    #loop through instructions and pull out the text
    for instructions in cooking_instructions:
        #store current step (step 1, step 2, etc.)
        step_label = f"Step {step}"
        instr_dict = {}
        #get <p> text from each step
        cooking_instructions_text = instructions.find('p').text.strip()
        # add step to dictionary
        instr_dict[step_label] = cooking_instructions_text
        # append the dict to list
        instr_list.append(instr_dict)
        # keep track of cooking step
        step += 1
    # create dict of ingredient list and cooking instructions for recipe
    dict = {}
    dict['Ingredients'] = ingredient_list
    dict['Instructions'] = instr_list
    
    
    return dict


#takes a recipe search phrase and the number of pages to be search on allrecipes.com
# example:  recipe_search('pad thai',3)
def recipe_search(search_string,num_of_pages):
    from splinter import Browser
    from bs4 import BeautifulSoup
    import pandas as pd
    import time
    import funcs
    
    # create lists for storing data
    recipe_list = []
    title_list = []
    recipe_text_list = []

    #replace spaces for url
    string = search_string.replace(' ','+')
    url = f'https://www.allrecipes.com/search?q={string}'
    
    # open automated browser and go to url
    browser = Browser('chrome')
    browser.visit(url)
    
    # set variable for page count
    pages = range(num_of_pages)
    recipe_total_count = 0
    # loop through pages and pull recipe information
    for page in pages:
        print("-------------------")
        print(f"Starting scrape for page {page+1}")
        print(browser.url)
        print("-------------------")
        
        #variable to count recipes and total elements
        recipe_count = 0
        element_count = 0
        # create BeautifulSoup object
        html = browser.html
        article_soup = BeautifulSoup(html, 'html.parser')
        
        # pull all recipe links from webpage
        links = article_soup.find_all('a', class_='comp mntl-card-list-items mntl-document-card mntl-card card card--no-image')

        # loop through all links
        for link in links:
            # check to see if the article has ratings,
            # this identifies a recipe over an article
            ratings = link.find_all('div', class_ = 'comp recipe-card-meta')
            if len(ratings) > 0:
                # create empty dicts for storing recipe information
                recipe_dict = {}
                recipe_text_dict = {}
                # print('found recipe')
                # print('storing recipe...')
                
                title = link.find(class_ = 'card__title-text').text
                rating = len(link.find_all(class_ = 'icon icon-star'))
                recipe_url = link.get('href')
                
                recipe_dict['title'] = title
                recipe_dict['rating'] = rating
                recipe_dict['url'] = recipe_url

                recipe_count += 1
                recipe_total_count += 1
                element_count +=1
                if element_count % 5 == 0:
                    print(f"{element_count} elements searched of {len(links)}")


                if title in title_list:
                    print('Recipe already found in dictionary')
                else:
                    title_list.append(title)
                    
                    recipe_text_dict['title'] = title
                    recipe_text_dict['recipe'] = funcs.recipe_scrape(recipe_url,browser)
                    recipe_text_list.append(recipe_text_dict)
                    
                recipe_list.append(recipe_dict)
            
            else:
                # print('article found..skipping')
                element_count += 1
                if element_count % 5 == 0:
                    print(f"{element_count} elements searched of {len(links)}")
                
        browser.visit(url)   



        if page == len(pages)-1:
            print("-------------------")
            print(f"{recipe_count} recipes found on page {page+1}")
            print("-------------------")
            print('Reached the last page...')
            print('All recipes scraped and stored...')
            print(f"{recipe_total_count} total recipes found")
            print("-------------------")
        else:
            try:
                print("-------------------")
                print("Moving to next page")
                print("-------------------")

                time.sleep(2)
                browser.links.find_by_partial_text('Next').click()
                time.sleep(2)
                
                print(f"{recipe_count} recipes found on page {page+1}")
               

                
                # print(browser.url)
                url = browser.url
            except:
                print("-------------------")
                print('Reached Except Clause for Next Button...')
                print('All recipes scraped and stored...')
                # print(f"{recipe_count} total recipes found")
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


# USE THIS CELL TO PULL SPECIFIC RECIPE TITLE
def recipe_select(top_recipes_df):   
    go = True
    #enter row index for row_index variable
    while go:  
        row_index = int(input('Enter the row index for the recipe you wish to see: '))
        try:
            recipe_title = top_recipes_df.iloc[row_index,0]
            go = False
        except:
            print('Error occured with index value, please check to make sure the index exists in the table and try again.')
            
    return recipe_title