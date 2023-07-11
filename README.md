# Recipe_Finder

# Background
Do you ever have trouble picking out a recipe for dinner? Are you tired of cooking the same things over and over again? Have you ever wondered if your pulled pork recipe is the best one out there?

Well look no further! The goal of this project is to use web scraping to find the best recipes on the web and return them to you for easy access. Want to bake a coconut cake but not sure which recipe to choose? Just enter 'coconut cake' and get a list of the top recipes delievered right to your screen! All in a (relatively) short amount of time!

# In Action
* User is prompted to enter a search term and then the program scapes all recipes related to that term
 ![image](https://github.com/StanJohn04/Recipe_Finder/assets/121142680/33917a55-9459-45c7-9d6d-35e37e7b69b7)

* All top-rated recipes are stored in a df and the user is asked to enter the index of the desired recipe
* the program then prints out the ingredients and cooking instructions
![image](https://github.com/StanJohn04/Recipe_Finder/assets/121142680/dd38d62d-4ec7-4163-b5b4-649666314ad3)


# HouseKeeping
* The functions in [funcs.py](https://github.com/StanJohn04/Recipe_Finder/blob/main/funcs.py) import all their dependencies, so as long as you have them installed the   program should work fine.
  * Python version 3.10.11 was used for development
  * The following python libraries are used:
    * bs4 - [docs](https://pypi.org/project/bs4/)
    * splinter - [docs](https://splinter.readthedocs.io/en/latest/)
    * pandas - [docs](https://pandas.pydata.org/docs/)
    * time - [docs](https://docs.python.org/3/library/time.html)

* Currently a work in progress. The jupyter notebook SHOULD run fine, but bugs are bound to be found ;)

* recipe_app.py
  * The next step is to try and put together an API that will return the same output as the jupyter notebook

* Eventually
  * I envision a dashboard that displays all the information in an aesthetically pleasing way
  * Have recipe_search() return all recipes in df as well as the top_recipes_df
    * allow user to choose which df to search (all_recipes or top_recipes)
