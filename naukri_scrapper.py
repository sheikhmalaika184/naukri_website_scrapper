import requests 
import csv

# do not change these values 
BASE_URL = 'https://www.naukri.com'
APP_ID = '109'
SYSTEM_ID = '109'
HEADERS = {
    'appid': APP_ID,
    'systemid': SYSTEM_ID
}

#can change these values
KEYWORD = 'solar'
LOCATION = 'india'
job_per_page = 20
jobs_threshold = 50


def make_request(url):
    response = requests.get(url, headers=HEADERS)
    data = response.json()
    return data


def fetch_jobs():
    jobs = []
    page_no = 0
    url = f'https://www.naukri.com/jobapi/v3/search?noOfResults={job_per_page}&searchType=adv&keyword={KEYWORD}&location={LOCATION}&pageNo={page_no}&sort=r'
    data = make_request(url)
    total_jobs = data['noOfJobs']
    extracted_jobs = 0
    if jobs_threshold <= total_jobs:
        while extracted_jobs <= jobs_threshold :
            extracted_jobs = extracted_jobs + len(data['jobDetails']) 
            jobs.extend(data['jobDetails'])
            page_no = page_no +1
            url = f'https://www.naukri.com/jobapi/v3/search?noOfResults={job_per_page}&searchType=adv&keyword={KEYWORD}&location={LOCATION}&pageNo={page_no}&sort=r'
            data = make_request(url)
        return jobs
    
    else:
        print(f"Total no of jobs is {total_jobs} less than total threshold {jobs_threshold}")
    
def extract_jobs_info(jobs):
    csvFile = open('naukri.csv', 'w')
    try:
        writer = csv.writer(csvFile)
        #columns names
        writer.writerow(('Sr','Job Title', 'Company Name','Key Skills','Experience','Salary','Location','Education','Industry','Functional Area','Employment Type','Job Url'))
        for i in range(0,jobs_threshold):
            # title,company name,key skills
            print("Job Title: "+jobs[i].get('title'))
            print("Company Name: " + jobs[i].get('companyName'))
            print("Key Skills: "+jobs[i].get('tagsAndSkills'))
        
            # experience, salary, location
            place_holders = jobs[i].get('placeholders')
            print("Experience: "+place_holders[0].get('label'))
            print("Salary: "+place_holders[1].get('label'))
            print("Location: "+place_holders[2].get('label'))
        
            #further details 
            job_id= jobs[i].get('jobId')
            url = f'https://www.naukri.com/jobapi/v4/job/{job_id}?src=jobsearchDesk'
            detailed_data = make_request(url)
            education_list = detailed_data['jobDetails']['education']['ug']
            print("Education: "+ modify_education_list(education_list))
            print("Industry: "+detailed_data['jobDetails']['industry'])
            print("Employment Type: " + detailed_data['jobDetails']['employmentType'])
            print("Functional Area: " + detailed_data['jobDetails']['functionalArea'])
            print("Job Url: "+ BASE_URL+jobs[i].get('jdURL'))
            print(" ")
            writer.writerow((i+1,jobs[i].get('title'),jobs[i].get('companyName'),jobs[i].get('tagsAndSkills'),place_holders[0].get('label'),place_holders[1].get('label'),place_holders[2].get('label'),modify_education_list(education_list),detailed_data['jobDetails']['industry'],detailed_data['jobDetails']['functionalArea'],detailed_data['jobDetails']['employmentType'],BASE_URL+jobs[i].get('jdURL')))
            
    except Exception as e:
        print(e)
        
    finally:
        csvFile.close()
        

        
def modify_education_list(education_list):
    edu_str = ""
    if(len(education_list)>0):
        for i in range(0,len(education_list)):
            edu_str = edu_str+education_list[i]+","
            
    else:
        edu_str = "None,"
    
    edu_str = edu_str[:-1]
    return edu_str
  

def main():
    jobs = fetch_jobs()
    extract_jobs_info(jobs)
    
#main function
if __name__ == '__main__':
    main()