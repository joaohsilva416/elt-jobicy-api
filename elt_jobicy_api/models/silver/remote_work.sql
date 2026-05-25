-- Import data: extract data from source
with sources as (
    select
        "jobTitle",
        "companyName",
        "jobType",
        "jobGeo",
        "jobLevel",
        "salaryMin",
        "salaryMax",
        "salaryCurrency",
    from {{ source("ELT_JOBICY", "remote_works") }}
),

-- Renamed: insert all transforms
renamed as (
    select
        "jobTitle" as job_title,
        "companyName" as company_name,
        "jobType" as job_type,
        "jobGeo" as work_location,
        "jobLevel" as seniority,
        try_cast(nullif("salaryMin", 'NaN') as float) as annual_salary_min,
        try_cast(nullif("salaryMax", 'NaN') as float) as annual_salary_max,
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
        round(annual_salary_min/12, 2) as monthly_salary_min,
        annual_salary_min,
        round(annual_salary_max/12, 2) as monthly_salary_max,
        annual_salary_max,
        currency
    from renamed
    where annual_salary_min is not null
    or annual_salary_max is not null
)

select * from final