package main

import (
	jira "ca.cricri/m/v2/my-jira-automation/client"
	openai "ca.cricri/m/v2/my-jira-automation/client"
	"ca.cricri/m/v2/my-jira-automation/helper"
	"encoding/json"
	"fmt"
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

	myJira := &helper.JiraAutomationConfigYaml{}
	jiraConf := myJira.GetMyJiraPromptConf()

	// Print the data loaded from the YAML file
	log.Printf("API Version: %s\n", jiraConf.APIVersion)
	devOpsPrompt := jiraConf.Jira.Prompt[1].DevOps
	dataEngineerPrompt := jiraConf.Jira.Prompt[0].DataEngineer

	// prompt chatgpt
	chatGPTResult, err := openai.RequestChatGPT(
		openAIAPIKey,
		chooseRandomBetween([]string{devOpsPrompt, dataEngineerPrompt}),
	)

	llmOutputResult := &helper.LLMOutputResult{}
	parsedChatGPTResult := llmOutputResult.BuildLLMOutputResult(chatGPTResult)

	// Create ticket
	jiraClient := jira.NewJiraClient(baseURL, username, apiToken, projectID)

	log.Printf("create first ticket")
	ticketFirst := jiraClient.CreateTicket(
		parsedChatGPTResult.JiraTicketsInfo[0].Title,
		parsedChatGPTResult.JiraTicketsInfo[0].Description,
	)

	log.Printf("create second ticket")
	ticketSecond := jiraClient.CreateTicket(
		parsedChatGPTResult.JiraTicketsInfo[1].Title,
		parsedChatGPTResult.JiraTicketsInfo[1].Description,
	)

	jsonFirstTicket, err := json.Marshal(ticketFirst)
	jsonSecondTicket, err := json.Marshal(ticketSecond)

	if err != nil {
		fmt.Println(err)
	}
	log.Printf("first ticket created: %s", jsonFirstTicket)
	log.Printf("second ticket created: %s", jsonSecondTicket)

	// update tempo
	tempo := os.Getenv("TEMPO_API_KEY")
	log.Printf(tempo)
}

func chooseRandomBetween(arrayString []string) string {
	log.Printf("select random prompt input to picked in config:")
	s := rand.NewSource(time.Now().Unix())
	r := rand.New(s) // initialize local pseudorandom generator
	randomValuePicked := arrayString[r.Int()%len(arrayString)]
	log.Printf("%s", randomValuePicked)
	return randomValuePicked
}
