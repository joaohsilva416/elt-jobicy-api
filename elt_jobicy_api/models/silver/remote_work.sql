-- Import data: extract data from source
with sources as (
    select
        "jobTitle",
        "companyName",
        "jobType",
        "jobGeo",
        "jobLevel",
        "annualSalaryMin",
        "annualSalaryMax",
        "salaryCurrency",
    from {{ source('ELT_JOBICY', 'remote_works') }}
),

-- Renamed: insert all transforms
renamed as (
    select
        "jobTitle" as job_title,
        "companyName" as company_name,
        "jobType" as job_type,
        "jobGeo" as work_location,
        "jobLevel" as seniority,
        cast("annualSalaryMin" as float) as annual_salary_min,
        cast("annualSalaryMax" as float) as annual_salary_max,
        "salaryCurrency" as currency,
    from sources
),

-- Final: select final
final as (
    select
        job_title,
        company_name,
        job_type,
        work_location,
        seniority,
        (annual_salary_min/12) as monthly_salary_min,
        annual_salary_min,
        (annual_salary_max/12) as monthly_salary_max,
        annual_salary_max,
        currency
    from renamed
)

select * from final