# PokemonSystem

This project is a Pokemon System API designed to handle various operations related to Pokemon species, trainers, and images. The API is built with a microservices architecture, consisting of four main services:

1.  **Gateway**: Acts as the entry point for all API requests and routes them to the appropriate services.
2.  **external_api**: Fetches data and images from an external Pokémon API.
3.  **pokemon_img_server**: Manages Pokemon images, storing and retrieving them from MongoDB.
4.  **pokemon_server**: Handles core features using MySQL, such as adding Pokemon species, managing trainers, and evolving Pokemon.
5.  Redis Cache: Provides caching for frequently accessed data to improve performance and reduce load on the database.

## Getting Started

These instructions will help you set up the project on your local machine for development and testing purposes.
### Prerequisites
-   Docker
### Installing
1. Clone the repository:
 ```bash
 git clone https://github.com/muhammadser1/PokemonSystem.git
 cd PokemonSystem
  ```
2. Set up environment variables:
	* Create a `.env` file in the root directory and add the necessary environment variables:
		```
		.env/
		MYSQL_DATABASE=xxxx
		MYSQL_USER=yyyy
		MYSQL_PASSWORD=zzzz
		MYSQL_ROOT_PASSWORD=zzzz
		MYSQL_PORT=xxxx (Default 3306)
		MYSQL_HOST=bbbb
		```
	*	create a 'sqlConfig.py' in pokemon_server:
		```
		sqlConfig/
		MYSQL_DATABASE='xxxx'
		MYSQL_USER='yyyy'
		MYSQL_PASSWORD='zzzz'
		MYSQL_ROOT_PASSWORD='zzzz'
		MYSQL_PORT=xxxx (Default 3306)
		MYSQL_HOST='bbbb' 
		```
3. Build and run the Docker containers:
```python
docker-compose up --build
```


## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.
