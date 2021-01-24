


## Description
A news aggregator API



- Users can get and search for neews from multiplee APIs





## Technology Stack

- FastAPI
- Redis

## Swagger Docs
http://127.0.0.1:8000/docs

###  Setting Up For Local Development

-   Check that python 3 is installed:

    ```
    python --version
    >> Python 3.7.0
    ```

-   Clone the news repo and cd into it:

    ```
    git clone https://github.com/tonyguesswho/favorite-things.git
    ```

-   Install dependencies from requirements.txt file:

    ```
    pip install -r requirements.txt
    ```

-   Make a copy of the .env.sample file in the app folder and rename it to .env and update the variables accordingly:

    ```
    DJANGO_KEY=generate a random django key # https://www.miniwebtool.com/django-secret-key-generator/
    DB_NAME=dbname
    DB_USER=dbuser
    DB_PASSWORD=secretpassword

    ```

-   Activate a virtual environment:

    ```

*   Run the application with the command

    ```
    python main.py
    ```
*  Start Redis
	- redis-server

Note - I created test accounts on Reditt to enable easy testing withoit needing to fill out enviromental varaibles




## Adding other API SOURCES

- create a class that inherits the source class in api/services/news_service.py providing a url and source name

- Add a get method to your class
- The get method makes use of the parent class send method to reach out to the external API and gets results
- Clean up result depending on fields and get a list of artlicles
	e.g 
	```
	[
		{
        "topic": "'The problem is Putin': protesters throng Russia's streets to support jailed Navalny",
        "link": "https://www.theguardian.com/world/2021/jan/23/the-problem-is-putin-protesters-throng-the-streets-to-support-navalny",
    	},
		....
	]
	```
- Pass the result to the parent map_fields method to return a mapped result
- Add your class to the list of sources


# further improvements 
- testing
- Optimization
- further error handling
- use a .env







I will appreciate any feedback on this project :)
