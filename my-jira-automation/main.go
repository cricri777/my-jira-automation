package main

import (
	jira "ca.cricri/m/v2/my-jira-automation/client"
	openai "ca.cricri/m/v2/my-jira-automation/client"
	"ca.cricri/m/v2/my-jira-automation/helper"
	"ca.cricri/m/v2/my-jira-automation/my_aws"
	"log"
	"math/rand"
	"os"
	"time"
)

// TODO create ticket for each prompt (see todo belowK)
// TODO cleanup logs
// TODO unit test
func main() {
	baseURL := os.Getenv("JIRA_BASE_URL")
	username := os.Getenv("JIRA_USERNAME")
	projectID := os.Getenv("JIRA_PROJECT_ID")
	openAIAPIKey := os.Getenv("OPENAI_API_KEY")
	apiToken, isTokenProvided := os.LookupEnv("JIRA_API_TOKEN")

	log.Printf("connecting to JIRA url %s project id %s with username %s token <REDACTED>", baseURL, projectID, username)

	if isTokenProvided { // TODO test
		log.Println("token provided by env variable")
	} else { // TODO test
		log.Println("token provided by SSM")
		SMC := my_aws.NewAwsSMClient("ca-central-1")
		apiToken = SMC.GetSecretValue("my-jira-automation/mdc")
	}

	log.Println("get JIRA api ticket")

	// GET resources configuration
	// Create an instance of MyJiraAutomation
	myJira := &helper.MyJiraAutomation{}

	jiraConf := myJira.GetMyJiraPromptConf()

	// Print the data loaded from the YAML file
	log.Printf("API Version: %s\n", jiraConf.APIVersion)
	devOpsPrompt := jiraConf.Jira.Prompt[1].DevOps
	dataEngineerPrompt := jiraConf.Jira.Prompt[0].DataEngineer

	log.Printf("devops prompt [%s]", devOpsPrompt)
	log.Printf("dataengineer prompt [%s]", dataEngineerPrompt)

	// prompt chatgpt
	chatGPTResult, err := openai.RequestChatGPT(
		openAIAPIKey,
		chooseRandomBetween([]string{devOpsPrompt, dataEngineerPrompt}),
	)
	log.Printf("chatgptprompt: [%s]", chatGPTResult)
	// TODO create ticket for each prompt

	// GetJiraTicket
	jiraClient := jira.NewJiraClient(baseURL, username, apiToken, projectID)

	ticket, err := jiraClient.GetTicket("BDEP-15")
	if err != nil {
		log.Fatal(err)
		return
	}

	log.Printf("get ticket %s", ticket)
}

func chooseRandomBetween(arrayString []string) string {
	log.Printf("select random value to pick between %s", arrayString)
	s := rand.NewSource(time.Now().Unix())
	r := rand.New(s) // initialize local pseudorandom generator
	randomValuePicked := arrayString[r.Int()%len(arrayString)]
	log.Printf("randomeValuePicked %s", randomValuePicked)
	return randomValuePicked
}
