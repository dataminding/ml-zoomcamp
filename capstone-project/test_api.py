import random
import sys
import requests

AWS_URL = "http://mlzoomcamp-fake-job-detector-dev.eu-west-1.elasticbeanstalk.com"
LOCAL_URL = "http://localhost:9911"

TEST_DATA = [{'title': 'Ruby on Rails Programmer',
  'department':"",
  'salary_range':"",
  'company_profile':"",
  'description': 'Ruby on Rails Web Engineer (RoR)Now Hiring\xa0Ruby on Rails Web Engineer\xa0for one of our client in\xa0Long Beach, CAJob Role :\xa0Ruby on Rails DeveloperJob Function :\xa0Web DeveloperJob Industry :\xa0Financial ServicesJob Type :\xa0Full-TimeJob Level :\xa0Mid - SeniorJob Location :\xa0Long Beach, CASkills and Experience Required/PreferredDesired Skills &amp; ExperienceObject-oriented background5+ yearsexperience with full lifecycle software development5+ yearsexperience with validatingHTML2+ yearsexperience with Ruby on Rails5+ yearsexperience with CSSExperience with Red-Green-Refactor development (TDD)Knowledge on PostgresSQL and T-SQLExperience with any of the NoSQL variant, preferably RedisPreferred Skills:Development for a high-traffic, mission-critical websiteWorking knowledge of SEOResponsive web and mobile web developmentThe Compensation:Best in IndustryNote:\xa0For U.S. Citizens / Green Card / EAD / Visa Candidates Only.Interested professionals please apply for the job with your updated resume.',
  'requirements':"",
  'benefits':"",
  'telecommuting': 0,
  'has_company_logo': 0,
  'has_questions': 0,
  'employment_type': 'Full-time',
  'required_experience': 'Mid-Senior level',
  'required_education':"",
  'industry': 'Information Technology and Services',
  'function':"",
  'country': 'US',
  'state': ' CA',
  'city': ' Long Beach'},
 {'title': 'Trainer/Recuiter Specialist',
  'department': 'customer service',
  'salary_range':None,
  'company_profile':None,
  'description': 'We are a Health Benefits company. Helping people save money when they cant afford insurance.2 positons available.Request an Interview and see if you qualitfy for a job.Daily and monthly pay checks',
  'requirements':None,
  'benefits': 'DentalHealthAmeriDocvision',
  'telecommuting': 0,
  'has_company_logo': 0,
  'has_questions': 0,
  'employment_type': 'Full-time',
  'required_experience': 'Not Applicable',
  'required_education': 'Unspecified',
  'industry': 'Consumer Services',
  'function':None,
  'country': 'US',
  'state': ' MS',
  'city': ' oxford'},
 {'title': 'Writers',
  'department':None,
  'salary_range':None,
  'company_profile':None,
  'description': 'We are a company looking for qualified individuals to help out withwriting tasks such as:- Short stories- Movie scripts- Sales scripts- Articles- News feeds- PR websites-Blog posts... and more.Job Duties Include:- Draft and create consumer content for lifestyle and health related websites- Research new products and services with the relation to the consumers- Create projects for blogs and other new media- Brand messages with reaching a large online audienceYou\'ll have the opportunity to work big name companies and popular websites in several niches from news, geography, sports, entertainment, travel, and others.Qualifications:- High-school Graduate or GED qualified with an interest in writing for blogs, stories, and other publications- Experience in Journalism, English, Communications or other related fields- Strong written communication skills with ability to proofread effectively- Ability to manage multiple projects- Experience with Microsoft Office (Word, PowerPoint, Outlook, Excel)- Internet acces / Online access (THIS IS A MUST)This is a part-time and full-time job, depending on you availability.Hours are flexible from 10 to 40 hours per week.Travel is not required. Pay is discussed via communication after application process.Please email "#EMAIL_d9fc2207d30a7b527f02e9d8d3fd4a932e9035642431db6343c0db6cd21a2804#" with your full name and resume. We will contact you shortly after within 24 hours',
  'requirements':None,
  'benefits':None,
  'telecommuting': 0,
  'has_company_logo': 0,
  'has_questions': 0,
  'employment_type':None,
  'required_experience':None,
  'required_education':None,
  'industry':None,
  'function':None,
  'country': 'US',
  'state': 'unknown',
  'city': 'unknown'},
 {'title': 'CASH JOBS, Part Time Workers Needed.',
  'department':None,
  'salary_range':None,
  'company_profile':None,
  'description': "CASH JOBS, Part Time Workers Needed.Work Minimum 1-2 Hours Per Day Anytime.Won't Required Experience For This Job.You Can Earn $350 to $450 Everyday.Suitable For Both Male And Female.Totally Free To Join, Visit Here:-#URL_1e08499380b02eb73650d95cb71317582e70b55b5eeb4a23ec873c11442f38b0#",
  'requirements': 'Work Minimum 1-2 Hours Per Day Anytime.',
  'benefits': 'Suitable For Both Male And Female.',
  'telecommuting': 0,
  'has_company_logo': 0,
  'has_questions': 0,
  'employment_type': 'Part-time',
  'required_experience':None,
  'required_education':None,
  'industry':None,
  'function':None,
  'country': 'AU',
  'state': ' NSW',
  'city': ' Sydney'},
 {'title': 'Software Engineer - ASP.NET',
  'department':None,
  'salary_range':None,
  'company_profile': 'Enozom is a leading software development company, offering custom software development, software products, offshore software development, professional outsourcing and software consultancy',
  'description': 'ResponsibilitiesThe right candidate will work with system analysts to determine business requirements, prepares technical design forms and builds new software through existing or newly developed codes.Build systems with .NET 4.0 / #URL_01a736d89d2f0b19de700923d2c312837e180465650804d0f84105352812bf9a# / SQL Server \xa0/ MVCDevelop new functionality on our existing software products.QualificationsEducation: Bachelor Degree preferably Computer Engineering.Experience: 2+ years in the same field.SkillsAbility to quickly learn new concepts and software is necessary.Deep knowledge of the .NET 3.5/4.0 Framework, including Visual Studio 2008, VB.NET, #URL_01a736d89d2f0b19de700923d2c312837e180465650804d0f84105352812bf9a#.ASMX and WCF Web Services, and #URL_de16367b05c5ad8d662bcb494e7f33613767a6a8881ee57a6328b09d250602b9#.Strong knowledge of software implementation best practices.Strong experience designing and working with n-tier architectures (UI, Business Logic Layer Data Access Layer) along with some experience with service-oriented architectures (SOA).Ability to design and optimise SQL Server 2008 stored procedures.Experience with JQuery or similar technologies.Hand coded XML, XHTML and CSS.',
  'requirements':None,
  'benefits':None,
  'telecommuting': 0,
  'has_company_logo': 1,
  'has_questions': 0,
  'employment_type':None,
  'required_experience':None,
  'required_education':None,
  'industry':None,
  'function':None,
  'country': 'EG',
  'state': ' ALX',
  'city': ' Alexandria'}]

def is_aws_app_available():
    awsresp = requests.get(AWS_URL)
    if awsresp.status_code == 200:
        return True
    else:
        return False


def get_prediction(data, url):
    presp = requests.post(f"{url}/detect", json=data)
    presp.raise_for_status()
    return presp.json()


if __name__ == "__main__":

    if is_aws_app_available():
        url = AWS_URL
    else:
        url = LOCAL_URL

    # server URL can be given as input param (e.g. when different port as 9911 is used)
    if len(sys.argv) > 1:
        url = sys.argv[1]

    print(f"Running a test for Fake Job Posting Prediction using {url} as server....\n")

    test_data = random.choice(TEST_DATA)

    print(
        f"Detecting fraudlent job posting for the following input parameters:\n{test_data}\n...."
    )

    prediction = get_prediction(data=test_data, url=url)

    print(
        f"Prediction for the job >> {prediction['job_title']} <<: "
        f"Is it fraud?: {prediction['is_job_posting_fraudlent']}"
        f"\nThanks for using the service und Tschüss!"
    )
