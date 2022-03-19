
# SEC Filing Analyzer
*SEC Filing Analyzer* is an app for analysing EDGAR SEC filing data.

Submission for the Inter-IIT Tech Meet's High Prep event: Digital Alpha's SEC Filing Analyzer for SaaS Companies

Team : HP_DA_T13



## Deployment

To deploy this project run

- Step 1 - Clone the repository
    ```
    git clone https://github.com/joetho786/SEC_file_analyzer.git
    ```
- Step 2 - make a virtual environment to run the code unhindered
    ```
    virtualenv venv
    ```
- Step 3 - activate virtual environment
    ```
    source venv/bin/activate
    ```
- Step 4 - change the directory
    ```
    cd SEC_filing_analyser
    ```
- Step 5 - install all dependencies and make Migration
    ```
    - pip install -r requirements.txt
    - python manage.py makemigrations
    - python manage.py migrate
    ```
- Step 6 - Run server
    ```
    python manage.py runserver
    ```
- Step 7 - Integrate the data
    ```
    - go to http://127.0.0.1:8000/import-csv/
    - Then upload the dataset.csv file and submit
    - Again go to http://127.0.0.1:8000/
    ```
- Now the Dashboard is Complete and ready to use.
## Guidelines Completions
### Dashboard
![main](main.jpg)
![second](seconf.jpg)

### Table of Contents
- We displayed links of the filings of 10-K, 10-Q and 8-K in the dashboard.

### Machine Learning implementation
We used Amazon based AWS SageMaker API and used inbuilt `NLPScorer()`, `JaccardSummarizerConfig()`, `KMedoidsSummarizerConfig()`, `SECXMLFilingParser()` functions to do the sentiment Analysis which resulted in getting positivity, negativity, certainity, uncertainity, risk, safe, litigous, fraud, sentiment, polarity, readability.

### Dataset Formation through Single call API
- We used single call API provided by SageMaker named `EDGARDatasetConfig()` and `DataLoader()` for making dataset of numerous companies thorugh their tickers or CIK numbers.
- After that, we converted the datset into CSV file and stored it on S3 bucket.

### Graphs and Charts
![third](third.jpg)
![fourth](fourth.jpg)


### Hosting 
We hosted our website in a EC2 instance in AWS.

### Web scraping
* We used selenium to automate browser to excel file for every CIK number by searching that CIK number on `https://www.sec.gov/edgar/searchedgar/companysearch.html`.
* These files were merged together to one by using `pandas` python package in format of CIK number v/s year of filing for displaying the links on the dashboard.
