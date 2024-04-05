# README

## Installation instructions

### MacOS

- This project uses Poetry. To install Poetry do the following
  - Make sure you have `brew` installed
  - Start a terminal
  - Install poetry using `brew install poetry`

## Configuring the application

- Start a terminal
- Navigate to the `flask-recipe-app` directory
- Install the packages using `poetry install`
- Then run `poetry add <package-name>` to add packages

## Working with Docker

- Check the environment variables in `docker-compose.yml`.
- Make sure all the config variables are in place in `config.py`.
- To run the application, from the root directory run the following command `docker-compose up --build`.

### First Migration

- Run the first migration with `docker exec -it <your-container-name> poetry run flask db upgrade`.
  - Subsequent migrations after models changes can be run with `docker exec -it <your-container-name> poetry run flask db migrate -m "subsequent migrations"`.

### Running tests
- make sure all test files are places in "tests" folder in your application root directory 
- To run tests, run `docker exec -it <your-container-name> poetry run pytest`

## Utilising the tools
- This application uses below tools for improving code

### Code Formatters
- Black: Black automatically formats your Python code to ensure it adheres to a consistent style, reducing the time spent on discussing style in code reviews
  - Command: `docker exec -it <your-container-name> poetry run black .`
- isort: isort is a Python utility for sorting imports alphabetically and automatically separating them into sections to improve code readability and consistency.
  - Command: `docker exec -it <your-container-name> poetry run isort .`
### Linters
- Flake8: A wrapper around PyFlakes, pycodestyle, and Ned Batchelder’s McCabe script. It checks for coding style (PEP 8), programming errors, and complex or overly dense code. It's highly valued for its simplicity and speed.
  - Command: `docker exec -it <your-container-name> poetry run flake8 .`
### Type Checkers
- MyPy: Uses type hints (PEP 484) to perform type checking at compile time. By annotating your code with type hints, MyPy can catch various types of bugs and ensure that your codebase remains consistent and easy to understand.
  - Command: `docker exec -it <your-container-name> poetry run mypy .`
### Code Analysis and Refactoring Tools
- SonarQube: A powerful tool that provides continuous inspection of code quality. It supports Python among other languages and can detect bugs, vulnerabilities, and code smells. It also offers detailed dashboards to track code quality over time.
  - Follow the below steps to setup and run SonarQube
    1. Pull and run the SonarQube Docker image:
       - `docker run -d --name sonarqube -p 9000:9000 sonarqube`. 
       - Access SonarQube at http://localhost:9000 or http://0.0.0.0:9000 whichever works. The default credentials are admin/admin.
    2. Configure SonarQube for Python Analysis:
       - After logging in, if the project is not created it will ask for creation, please select "Create a local project". 
       - Enter project details by adding "Project Diplay Name" and hit "Next". 
       - In the next screen you can select "Use global setting" and then hit "Create Project". 
       - Once created in the same screen select "Locally" for configuring local project. 
       - Now generate token and copy the token and keep it handy and click "Continue". 
       - Select "Other (for JS, TS, Go, Python, PHP, ...)". 
       - Follow the instructions futher instructions to set up sonar-scanner. 
         - `wget https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-5.0.1.3006-macosx.zip
            unzip sonar-scanner-cli-5.0.1.3006-macosx.zip
            sudo mv sonar-scanner-5.0.1.3006-macosx /opt/sonar-scanner`
       - Note: keep this window open as the analysis is done it will auto-refresh
       - Export the below path in the ~/.zshrc or ~/.bashrc (Mac). Follow instructions for windows/linux provided on the screen
         - `export PATH="/opt/sonar-scanner/bin:$PATH"`
         - Check if sonar-scanner is working by running `sonar-scanner -v`
       - Navigate to your project and run the below command to start analysis and wait for it to complete once complete go back to the page to see the analysis.
         - `sonar-scanner \
          -Dsonar.projectKey=<your Project Diplay Name> \
          -Dsonar.sources=. \
          -Dsonar.host.url=http://0.0.0.0:9000 \
          -Dsonar.token=<your-sonar-token-generated-above>`
