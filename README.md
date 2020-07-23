# msi-azure-functions-linux
Code example : how to use managed service identity authentication for python worker for azure functions linux to connect with ODBC driver
Our team is successfully using Azure, Python, Linux, and ODBC Driver 17 for SQL Server to connect to Azure databases using Managed Service Identities.
We aren't using `Authentication=ActiveDirectoryMsi` in the connection string to do this.
Instead we are pulling in the `"MSI_SECRET` and `MSI_ENDPOINT` environment variables to retrieve and access token.
and we include that token with the connection string.

Steps :

1. Create function app in azure 
2. enable Identity for the function app inside settings
3. Add your function app to database user using :
    CREATE USER [FUnctionApp_ENV_MyFunctionApp] FROM EXTERNAL PROVIDER
    ALTER ROLE cb_datareader ADD MEMBER [FUnctionApp_ENV_MyFunctionApp]
    Note: you might want to give db onwer rights depending on operations needed
4. use the msi method block with your database string 
