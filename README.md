Random Notes:
---------------------------------------------

Run main.py to use this program

Currently, keyword libraries are .txt files that you must modify directly

Numerical parameters such as "bad_word_tolerance," "good_word_tolerance," and "min_years_exp" are hard-coded into the initializer of class BasicBot

Any new filtering methods can be included in BasicBot

Changes to Job class effect secretary_bot's filters, basic_bot's filters, statistics(), [site]_bot extraction methods

You have delete the job cache if any changes were made to the Job class (it will reinitialize

You have to recompile the program for filter additions/subtractions changes to take place

SUGGESTION: When first tuning the bot, set good_word_tolerance to 0
            uncomment URL outputs in the filtering methods to manually spot check rejected job posts
