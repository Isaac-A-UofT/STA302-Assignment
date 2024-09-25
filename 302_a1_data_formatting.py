import requests
import pandas as pd
import numpy as np

api_key = 'eCU6CkESG62Cb3nRBXCedO8BOiMo3rWwFYdlcfsI'
base_url = 'https://api.data.gov/ed/collegescorecard/v1/schools'

fields = (
    'latest.school.name,'
    'latest.student.size,'
    'latest.school.endowment.end,'
    'latest.cost.tuition.in_state,'
    'latest.earnings.2_yr_after_completion.median,'
    'latest.completion.consumer_rate,'
    'latest.admissions.admission_rate.overall,'
    'latest.school.carnegie_undergrad,'
    'latest.school.carnegie_size_setting,'
    'latest.admissions.sat_scores.average.overall,'
    'latest.school.locale,'
    'latest.student.demographics.student_faculty_ratio,'
    'latest.student.demographics.men,'
    'latest.student.demographics.women,'
    'latest.student.demographics.race_ethnicity.asian,'
    'latest.student.demographics.race_ethnicity.black,'
    'latest.student.demographics.race_ethnicity.white,'
    'latest.student.demographics.race_ethnicity.hispanic,'
    'latest.student.demographics.race_ethnicity.aian,'
    'latest.student.demographics.race_ethnicity.nhpi'
)

# Initialize an empty list to collect all results
all_schools = []
page = 1

while True:
    url = f"{base_url}?api_key={api_key}&fields={fields}&page={page}&per_page=100"
    
    # Making the request
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        
        # Extracting relevant information
        schools = data.get('results', [])
        all_schools.extend(schools)  # Append the results to the list
        
        # Check if there are more pages
        metadata = data.get('metadata', {})
        total_pages = metadata.get('total', 0) // metadata.get('per_page', 1)
        
        print(f'getting data on page {page} of {total_pages}')

        if page >= total_pages:
            break  # Exit loop if we've reached the last page
        page += 1  # Move to the next page
    else:
        print(f"Error: {response.status_code}, {response.text}")
        break

# Creating a DataFrame from all collected data
df = pd.DataFrame(all_schools)

# Renaming columns
df = df.rename(columns={
    'latest.school.name': 'School Name',
    'latest.school.endowment.end': 'Endowment',
    'latest.earnings.1_yr_after_completion.median': 'Median Salary (2 Years After Graduation)',
    'latest.student.size': 'Student Size',
    'latest.cost.tuition.in_state': 'In-State Tuition',
    'latest.completion.consumer_rate': 'Completion Rate',
    'latest.admissions.admission_rate.overall': 'Overall Admission Rate',
    'latest.school.carnegie_undergrad': 'Carnegie Classification (Undergraduate)',
    'latest.school.carnegie_size_setting': 'Carnegie Size Setting',
    'latest.admissions.sat_scores.average.overall': 'Average SAT Score',
    'latest.school.locale': 'School Locale',
    'latest.student.demographics.student_faculty_ratio': 'Student-Faculty Ratio',
    'latest.student.demographics.race_ethnicity.asian': 'Asian Enrollment',
    'latest.student.demographics.race_ethnicity.black': 'Black Enrollment',
    'latest.student.demographics.race_ethnicity.white': 'White Enrollment',
    'latest.student.demographics.race_ethnicity.hispanic': 'Hispanic Enrollment',
    'latest.student.demographics.race_ethnicity.aian' : 'Native American Enrollment',
    'latest.student.demographics.race_ethnicity.nhpi' : 'Native Hawaiian Enrollment',
    'latest.student.demographics.men': 'Percent Male Enrollment',
    'latest.student.demographics.women': 'Percent Female Enrollment'
})

# Filtering out unwanted rows
df = df[
    (df['Student Size'] > 0) &
    (df['Carnegie Classification (Undergraduate)'] != -2) &
    (df['Carnegie Size Setting'] != -2) &
    df['Overall Admission Rate'].notnull() &
    (df['Median Salary (2 Years After Graduation)'] > 0) &
    df['Average SAT Score'].notnull()
]


# Calculate Simpson's Diversity Index considering percentages
def calculate_sdi(row):
    # Convert percentages to proportions
    p_asian = row['Asian Enrollment']
    p_black = row['Black Enrollment']
    p_white = row['White Enrollment']
    p_hispanic = row['Hispanic Enrollment']
    p_aian = row['Native American Enrollment']
    p_nhpi = row['Native Hawaiian Enrollment']

    # Simpson's Diversity Index Calculation
    sdi = 1 - (p_asian**2 + p_black**2 + p_white**2 + p_hispanic**2 + p_aian**2 + p_nhpi**2)
    return sdi

# Calculate Shannon Diversity Index for gender ratios
def calculate_shannon_gender(row):
    p_male = row['Percent Male Enrollment']
    p_female = row['Percent Female Enrollment']
    
    # Ensure non-zero proportions to avoid log(0)
    if p_male > 0 and p_female > 0:
        shannon_index = -(p_male * np.log(p_male) + p_female * np.log(p_female))
        return shannon_index / np.log(2)  # Normalize to a 0-1 scale by dividing by log(2)
    else:
        return 0  # If one group has no representation

# Apply the functions to each row in the DataFrame
df['Diversity Index'] = df.apply(calculate_sdi, axis=1)
df['Gender Shannon Index'] = df.apply(calculate_shannon_gender, axis=1)

# Saving to Excel
df.to_excel('school_data.xlsx', index=False)

print("Data saved to 'school_data.xlsx'.")
