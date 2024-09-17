package main

import (
	jira "ca.cricri/m/v2/my-jira-automation/client"
	openai "ca.cricri/m/v2/my-jira-automation/client"
	"ca.cricri/m/v2/my-jira-automation/helper"
	"log"
	"math/rand"
	"os"
	"time"
)

// TODO create ticket for each prompt (see todo below)
// TODO cleanup logs
// TODO unit test
func main() {
	baseURL := os.Getenv("JIRA_BASE_URL")
	username := os.Getenv("JIRA_USERNAME")
	projectID := os.Getenv("JIRA_PROJECT_ID")
	openAIAPIKey := os.Getenv("OPENAI_API_KEY")
	apiToken, isJiraTokenProvided := os.LookupEnv("JIRA_API_TOKEN")

	log.Printf("connecting to JIRA url %s project id %s with username %s token <REDACTED>", baseURL, projectID, username)

	if isJiraTokenProvided {
		log.Println("Jira token provided by env variable")
	} else {
		log.Fatal("no Jira token provided")

	}

	// Create an instance of JiraAutomationConfigYaml Configuration
	myJira := &helper.JiraAutomationConfigYaml{}

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

	// for testing purposes
	//chatGPTResult := "[{\"title\":\"my_title1\",\"description\":\"my description1\",\"day\":1},{\"title\":\"my_title2\",\"description\":\"my description2\",\"day\":2},{\"title\":\"my_title3\",\"description\":\"my description3\",\"day\":3},{\"title\":\"my_title4\",\"description\":\"my description4\",\"day\":4},{\"title\":\"my_title5\",\"description\":\"my description5\",\"day\":5}]"
	log.Printf("chatgptprompt: [%s]", chatGPTResult)
	// TODO create ticket for each prompt
	llmOutputResult := &helper.LLMOutputResult{}
	parsedChatGPTResult := llmOutputResult.BuildLLMOutputResult(chatGPTResult)

	// TODO: fix this compile issue
	log.Printf("first title%s", parsedChatGPTResult[0].Title)
	log.Printf("second title%s", parsedChatGPTResult[0].Title)
	log.Printf("first title %s")
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
