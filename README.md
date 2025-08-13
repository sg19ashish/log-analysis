Solution Approach for application traffic: 
The IIS logs are available at E:\\IISLogs in production servers.
Logs are getting saved for one week only.
#Fields:  shows the filed that would be printed in logs and its sequence. 
‘cs-uri-stem’ gives the URI of the application which the request is hitting. This is the field we are interested in. 
Created a Python script to cycle through all logs and capture “date” and “cs-uri-stem” in multiple CSV files. (Due to high number of log files and its size) 
Created second python script to combine all CSV files. This will give “cs-uri-stem”  and number of times it was called. Also, it will split t he URI to make it easier to filter.
