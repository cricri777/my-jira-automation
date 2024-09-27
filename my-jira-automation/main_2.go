package main

import (
	jira "ca.cricri/m/v2/my-jira-automation/client"
	"encoding/json"
	"log"
	"os"
)

// TODO : setup Tempo
func main() {
	// update tempo
	tempo := os.Getenv("TEMPO_API_KEY")
	projectAccountId := os.Getenv("JIRA_ACCOUNT_ID")

	authorAccountId := "authorAccountId" // authorAccountId
	issueId := "issueId"
	startDate := "startDate"
	timeSpentSeconds := "timeSpentSeconds"

	baseURL := os.Getenv("JIRA_BASE_URL")
	username := os.Getenv("JIRA_USERNAME")
	projectID := os.Getenv("JIRA_PROJECT_ID")
	apiToken := os.Getenv("JIRA_API_TOKEN")

	// Create ticket
	jiraClient := jira.NewJiraClient(baseURL, username, apiToken, projectID)

	ticket, err := jiraClient.GetTicket("BDEP-23")
	if err != nil {
		log.Fatal(err)
	}

	jsonTicket, err := json.Marshal(ticket)
	if err != nil {
		log.Fatal(err)
	}
	log.Printf("get ticket created: %s", jsonTicket)
	println(jsonTicket)
	println(authorAccountId)
	println(issueId)
	println(startDate)
	println(timeSpentSeconds)
	println(tempo + ";")
	println(projectAccountId + ";")

	//postUrl := fmt.Sprintf("https://api.tempo.io/4/worklogs")

	//bodyByte := []byte(body)
	//request, err := http.NewRequest("POST", postUrl, bytes.NewBuffer(bodyByte))
	//
	//// Set the authentication header
	//request.SetBasicAuth(c.userName, c.apiToken)
	//if err != nil {
	//	log.Fatal(err)
	//}
	//
	//request.Header.Add("Content-Type", "application/json")
	//
	//client := &http.Client{}
	//res, err := client.Do(request)
	//if err != nil {
	//	log.Fatal(err)
	//}
	//
	//defer res.Body.Close()
	//
	//readBodyResponse, err := io.ReadAll(res.Body)
	//if err != nil {
	//	log.Println("Error reading response body:", err)
	//}
	//
	//if res.StatusCode == http.StatusCreated || res.StatusCode == http.StatusOK {
	//	log.Println("Ticket created successfully!")
	//} else {
	//	log.Printf("Failed to create ticket. Status: %s, Body: %s\n", res.Status, res.Body)
	//}

}
