# RenPy-Docs-Discord-Bot
A simple Python Discord bot to fetch documentation pages from https://www.renpy.org/doc/html/ based on a search query submitted to custom Google search engine.

## Info
This is a simple template for a utility Discord bot to take keywords submitted via the `docs` command, submit the query via a Google custom search engine, and return the first result. The `next` command fetches the next result for the last query submitted, and can be submitted until there are no more results (should typically be 10 maximum).

## How To
Firstly, create your [custom Google search engine](https://programmablesearchengine.google.com/controlpanel/all).  
In the "Sites to search" section, add one webpage:
`www.renpy.org/doc/html/*`

Next, simply create a `.env` file in the project's directory, and fill out the following information:
* `TOKEN` - Your Discord bot's token (found [here](https://discord.com/developers/applications))
* `RENPY_SEARCH_API_KEY` - Your custom Google search engine API key (found [here](https://developers.google.com/custom-search/v1/overview#api_key))
* `SEARCH_ENGINE_ID` - Your search engine ID (found [here](https://programmablesearchengine.google.com/controlpanel/all))

## Adding To Your Own Bot
Alternatively, you may add the commands to your bot by adding the relevant pieces of code to your own Discord.py bot.
* Functions:
  * renpy_docs_query()
* Commands:
  * docs()
  * next()
* Global variables:
  * RENPY_SEARCH_API_KEY
  * SEARCH_ENGINE_ID
  * googleapi_link
  * last_query
  * illegal_characters
