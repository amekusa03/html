# Gmail PDF Unlocker

2026/04/28  Python / VM

Automatic email processing using virtual machines

## About this Project

This is a project that sends an email, and if the email meets the set conditions, the attached PDF file is saved in Google Drive with the password removed.

## System Configuration & Workflow

By using Python instead of Google Apps Script (GAS), we are able to respond flexibly to changes in specifications. 


- ***iaas: **Google Compute Engine (GCE)
                            Free tier (e2-micro) 
- ***Language: **Python 
- ***Target emails: **Unread emails from specific senders 
- ***Processing details: **Automatically remove password protection of attached PDF 
- ***Save destination: **Specified folder in Google Drive 
- ***Post-processing: **Add processed label and mark as read 
By using GCE's `e2-micro ` instance, you can always operate it for free. *1 


- **Gmail API: **Search and retrieve unread emails from a specific sender. 
- **Python (pypdf): **Securely remove PDF passwords in memory. 
- **Google Drive API: **Automatically save to specified folder. 
*1 Please be careful not to confuse it with f1-micro, which was previously eligible for the free tier. e2-micro is currently eligible for the free tier.

## Setup

#### 1. Setting up your GCP project


1. Enable Gmail API and Google Drive API. 
2. Set up the OAuth consent screen and create an "OAuth client ID" as a desktop app. 
3. Get `credentials.json `. 

#### 2. Installation and deployment


```
`git clone <your-repo-url>
cd unlockpdf
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt `
```

## Usage

#### First execution (authentication)

The first time you run it, your browser will start and you will be asked to log in to your Google account. Once the authentication is complete, `token.json ` will be generated in your working directory. 


```
`python unlock_and_save.py `
```

#### Service (systemd)

Register it as a background process using Linux's `systemd ` to keep it running 24 hours a day, 365 days a year. This allows the program to automatically recover when the program terminates abnormally or when the server is restarted. 


```
`# /etc/systemd/system/unlockpdf.service
[Service]
ExecStart=/path/to/venv/bin/python /path/to/unlock_and_save.py
Restart=always
User=your-user-name `
```

## Deployment (Google Compute Engine)

In order to optimize (minimize) costs, we will operate on GCE's free tier (e2-micro). 


1. **Instance creation: **Create `e2-micro ` in the free tier target region (us-west1, us-central1, etc.). (⚠️I created it using f1-micro and was charged. Fee calculation is delayed for several hours, so the fee will increase for a while even after it is stopped.) 
2. **File Transfer: Upload **`unlock_and_save.py `, `credentials.json `, `token.json `. *Since the server does not have a GUI, it is necessary to transfer the `token.json ` generated in the local environment. 


3. **Always on configuration: **`systemd ` Create a unit file and enable/start the service.

## Security Considerations

***Important: Protecting your credentials**

Please never include the following confidential information in public repositories such as GitHub. We strongly recommend using environment variables. 


- `credentials.json ` (app key) 
- `token.json ` (account access rights) 
- `PDF_PASSWORD ` (raw password) 
If you have accidentally made your credentials public, please immediately disable the relevant credentials and issue new ones.

## Development Environment

- Google Compute Engine 
- Python 3.x 
- Gmail & Drive API 
- pypdf

## Precautions & Resources

Please note **Google Cloud Platform pricing**. If you operate outside of the free tier (e2-micro), you will be charged. 

The materials are published on GitHub. You are welcome to reuse it for personal study or small projects. 

[View on GitHub](https://github.com/amekusa03/AskGeminibyemail)

## Best Practices for 24/7 Operation

#### 1. Process management (systemd)

It is most robust to create a service with `systemd `, so that it will automatically restart when the OS starts or crashes. 


```
`[Service]
Restart=always
RestartSec=5
ExecStart=/path/to/venv/bin/python main.py `
```

#### 2. Robust Python code


- **Exception handling: **Wrap the main loop in `try-except ` to avoid stopping on temporary errors. 
- **Logging: **`logging ` library, using Google Cloud Logging
                                allows you to check the status remotely. 

#### 3. Infrastructure stabilization


- **Memory monitoring: **e2-micro has a small amount of memory (1GB), so you need to be careful about stopping it due to OOM Killer. 
- **Static IP: **For stable communication, we recommend reserving a static external IP address. 
- **Automatic updates: **Automate security patch application with GCE's OS configuration management function. 

#### 4. Considering containerization

With an eye toward future environment migration and scaling, you can minimize problems with dependencies by deploying Docker containers.
