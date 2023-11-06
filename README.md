<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
<!--

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/wvanelteren/rotterdam-the-hague-airport-pipeline">
    <img src="assets/images/RTHA_logo.jpg" alt="Logo" width="480" height="230">
  </a>

<h2 align="center">Rotterdam The Hague Flight Schedule Serverless Data Pipeline</h2>

  <p align="center">
    <small> This project is NOT affiliated with, funded, or in any way associated with RTHA (Rotterdam the Hague Airport) or any other subsidiary of the Schiphol Group
    </small>
    </a>
    <br>
  </p>
</div>

<!-- ABOUT THE PROJECT -->
## About The Project

### Motivation
Transavia is one of the most underrated airlines in Western Europe. They are technically a low cost carrier, but the experience in flying with them puts the economy class experience of many major airlines to shame. Furthermore, they are super developer friendly, especially compared to other budget airlines such as Ryan air and Whizz air (just check out their [developer portal](https://developer.transavia.com/)!)

If you have the chance to fly with them, there is a good chance you have to fly from/to Rotterdam The Hague Airport (RTHA), one of their two hubs in the Netherlands (the other one is the far more popular Schiphol airport, in Amsterdam). Just like Transavia, this airport is massively underrated. RTHA is a small yet great airport. Some of its perks:
* Recently renovated
* Fast customs, don't have to take your liquids out of your bag
* Easy to get to
* Queues were suprisingly okay during the 2022 summer when Schiphol and Eindhoven airport had queues straight out of hell.

I really like flying from/to RTHA with Transavia. Sadly, most people I know seem to not consider flights from RTHA for their vacation, only Schiphol and Eindhoven (some even didn't know RTHA existed!). Therefore, I thought it was time to give this airport a little more love by making their flight data the subject of this data pipeline.

### The Data Pipeline

This is a serverless ETL pipeline that scrapes and preprocesses flight schedule data from [RTHA website]() and pulls weather data from [Openweather API]() to explore the effect of weather conditions on flight delay. A delayed flight is understood as a flight that lands/takes off >15 minutes later than the scheduled flight time.

**Data Pull** \
Scrapes flights arrivals and departures txt data from [RTHA website]() and pulls weather data from the [Openweather API]() via AWS Lambdas and loads both into S3 buckets as JSON Array objects

**ETL** \
ETL is handled by AWS Glue Spark
*Extracts* all the responses from data pull lambdas and merges them into their respective dataframe. \
*Transforms* rows in dataframe using Spark; schema changes, feature engineering, etc. \
*Loads* dataframe into datalake (S3 + Parquet + AWS Data Catalog).

**Analysis** \
Create table of arrivals, departures and weather data with AWS Athena; query to create final dataset that adds the current weather conditions to the scheduled flight time. Query stored in S3 as .csv file to download and perform statistical analysis on and visualise (once I have enough data :D)

**Visualise** \
Todo, probably Google Data Studio as it is free. AWS quicksight makes most sense since it natively integrates with AWS, but $24/month is too much for this broke student :(

**Scheduler** \
I use AWS Eventbridge Scheduler to orchestrate the data pipeline as follows:
* Flight data pull: every hour
* Weather data pull: every 5 mins
* ETL jobs: every month
* Athena query: on demand.

### Architecture Diagram

  <a href="https://github.com/wvanelteren/rotterdam-the-hague-airport-pipeline">
    <img src="assets/images/architecture_diagram.png" alt="diagram" width="950" height="340">
  </a>

## Getting Started

### Prerequisites

Components to acquire/install to run the project.

**Accounts**
* [AWS account](https://aws.amazon.com/account/)
* [Openweather account](https://home.openweathermap.org/users/sign_up) - To acquire an Openweather API key (free)

**Software:**
* [Python 3.10](https://www.python.org/downloads/) - Note: AWS glue 4.0 currently (06/11/2023) does not support > Python 3.10.
* [Poetry](https://python-poetry.org/docs/#installation) - For dependency management and installing requirements
* [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) - For managing AWS (needs to be configured)
* [Terraform](https://developer.hashicorp.com/terraform/downloads) - For setting up cloud infrastructure
* [Docker](https://www.docker.com/products/docker-desktop/) - For local glue development

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/wvanelteren/rotterdam-the-hague-airport-pipeline.git
   ```
2. Install requirements
   ```sh
   poetry install
   ```
3. Configure AWS CLI
   ```sh
   aws configure
   ```
4. Change variables in [variables.tf](https://github.com/wvanelteren/rotterdam-the-hague-airport-pipeline/blob/main/terraform/variable.tf) to specify AWS credentials, default region, etc.

5. Run Terraform to create AWS resources
    ```sh
   terraform init
   terraform plan
   terraform apply
   ```
6. Setup AWS Eventbridge Scheduler in the AWS Management Console (Terraform currently not supported) to orchestrate the pipeline to your liking

### Testing

Unit tests:
```sh
poetry run python -m pytest tests\unit
```

Integration tests:
```sh
poetry run python -m pytest tests\integration
```

<!-- ROADMAP -->
## Roadmap

- Waiting for more data to visualise and maybe do some ML :)
- CI/CD

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


<!-- LICENSE -->
<p align="right">(<a href="#readme-top">back to top</a>)</p>
