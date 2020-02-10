# -*- coding: utf-8 -*-
# @Time    : 2020-02-08 18:51
# @Author  : jinhang
# @File    : data_split.py

text_string = "Ingredients: 6 ounces penne 2 cups Beechers Flagship Cheese Sauce (recipe follows) 1 ounce Cheddar, grated (1/4 cup) 1 ounce Gruyere cheese, grated (1/4 cup) 1/4 to 1/2 teaspoon chipotle chili powder (see Note) 1/4 cup (1/2 stick) unsalted butter 1/3 cup all-purpose flour 3 cups milk 14 ounces semihard cheese (page 23), grated (about 3 1/2 cups) 2 ounces semisoft cheese (page 23), grated (1/2 cup) 1/2 teaspoon kosher salt 1/4 to 1/2 teaspoon chipotle chili powder 1/8 teaspoon garlic powder (makes about 4 cups) Instructions: Preheat the oven to 350 F. Butter or oil an 8-inch baking dish. Cook the penne 2 minutes less than package directions. (It will finish cooking in the oven.) Rinse the pasta in cold water and set aside. Combine the cooked pasta and the sauce in a medium bowl and mix carefully but thoroughly. Scrape the pasta into the prepared baking dish. Sprinkle the top with the cheeses and then the chili powder. Bake, uncovered, for 20 minutes. Let the mac and cheese sit for 5 minutes before serving. Melt the butter in a heavy-bottomed saucepan over medium heat and whisk in the flour. Continue whisking and cooking for 2 minutes. Slowly add the milk, whisking constantly. Cook until the sauce thickens, about 10 minutes, stirring frequently. Remove from the heat. Add the cheeses, salt, chili powder, and garlic powder. Stir until the cheese is melted and all ingredients are incorporated, about 3 minutes. Use immediately, or refrigerate for up to 3 days. This sauce reheats nicely on the stove in a saucepan over low heat. Stir frequently so the sauce doesnt scorch. This recipe can be assembled before baking and frozen for up to 3 monthsjust be sure to use a freezer-to-oven pan and increase the baking time to 50 minutes. One-half teaspoon of chipotle chili powder makes a spicy mac, so make sure your family and friends can handle it! The proportion of pasta to cheese sauce is crucial to the success of the dish. It will look like a lot of sauce for the pasta, but some of the liquid will be absorbed."
print(text_string)
data_dict = {}
data = text_string.split("Ingredients:")
text_string = data[1].strip()
data = text_string.split("Instructions:")
Ingredients = data[0].strip()
Instructions = data[1].strip()
data_dict['Ingredients'] = Ingredients
data_dict['Instructions'] = Instructions

print(data_dict)

