package main

import (
	"ca.cricri/m/v2/my-jira-automation/my_aws"
	"log"
	"os"
)

func main() {
	baseURL := os.Getenv("JIRA_BASE_URL")
	username := os.Getenv("JIRA_USERNAME")
	projectID := os.Getenv("JIRA_PROJECT_ID")
	accountID := os.Getenv("JIRA_ACCOUNT_ID")

	log.Printf("connecting to JIRA url %s project id %s with username %s token <REDACTED>", baseURL, projectID, username)

	apiToken, isTokenProvided := os.LookupEnv("JIRA_API_TOKEN")

	if isTokenProvided {
		log.Println("token provided by env variable")
	} else {
		log.Println("token provided by SSM")
		SMC := my_aws.NewAwsSMClient("ca-central-1")
		apiToken = SMC.GetSecretValue("my-jira-automation/mdc")
	}

	log.Println("get JIRA api ticket")
	jiraClient := client.NewJiraClient(baseURL, username, apiToken, projectID)

	ticket, err := jiraClient.CreateTicket(accountID)
	if err != nil {
		log.Fatal(err)
		return
	}

	log.Println(ticket)
}
