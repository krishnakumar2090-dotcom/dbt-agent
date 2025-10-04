SELECT
    Load as-is AS Trial_ID,
    Trim spaces, convert to uppercase AS Protocol_Number,
    Take latest record AS Study_Title,
    Load as-is AS Site_ID,
    SUM(subjects_enrolled) GROUP BY trial_id, site_id AS Subject_Count,
    Load as-is AS Enrollment_Target
FROM vcv_trials
JOIN irt_enrollment ON vcv_trials.trial_id = irt_enrollment.trial_id
JOIN irt_enrollment ON vcv_sites.site_id = irt_enrollment.site_id