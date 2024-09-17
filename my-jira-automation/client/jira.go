package jira

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
)

// JiraClient represents the Jira API client
type JiraClient struct {
	baseUrl   string
	userName  string
	apiToken  string
	projectID string
}

// NewJiraClient is the constructor function for JiraClient
func NewJiraClient(baseURL, userName, apiToken, projectID string) *JiraClient {
	return &JiraClient{
		baseUrl:   baseURL,
		userName:  userName,
		apiToken:  apiToken,
		projectID: projectID,
	}
}

func (c *JiraClient) CreateTicket(summary string, description string) string {
	postUrl := fmt.Sprintf("%s/rest/api/2/issue/%s", c.baseUrl)

	body := fmt.Sprintf(`{
	  "fields": {
		"issuetype": {
		  "name": "Story"
		},
		"parent": {
		  "key": "BDEP-2"
		},
		"project": {
		  "key": "BDEP"
		},
		"summary": "%s"
		"description": "%s",
	  }
	}`, summary, description)

	bodyByte := []byte(body)
	request, err := http.NewRequest("POST", postUrl, bytes.NewBuffer(bodyByte))

	if err != nil {
		log.Fatal(err)
	}

	request.Header.Add("Content-Type", "application/json")

	client := &http.Client{}
	res, err := client.Do(request)
	if err != nil {
		log.Fatal(err)
	}

	defer res.Body.Close()

	readBodyResponse, err := io.ReadAll(res.Body)
	if err != nil {
		log.Println("Error reading response body:", err)
	}

	if res.StatusCode == http.StatusCreated || res.StatusCode == http.StatusOK {
		log.Println("Ticket created successfully!")
	} else {
		log.Printf("Failed to create ticket. Status: %s\n", res.Status)
	}
	return string(readBodyResponse)
}

// GetTicket get a ticket from Jira
func (c *JiraClient) GetTicket(ticketKey string) (map[string]interface{}, error) {
	url := fmt.Sprintf("%s/rest/api/2/issue/%s", c.baseUrl, ticketKey)

	// Create a new HTTP request
	req, err := http.NewRequest("GET", url, nil)
	if err != nil {
		return nil, err
	}

	// Set the authentication header
	req.SetBasicAuth(c.userName, c.apiToken)
	req.Header.Set("Content-Type", "application/json")

	// Execute the request
	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	// Check if the request was successful
	if resp.StatusCode != http.StatusOK {
		bodyBytes, _ := io.ReadAll(resp.Body)
		return nil, fmt.Errorf("failed to get ticket: %s", string(bodyBytes))
	}

	// Parse the response body into a map
	var result map[string]interface{}
	if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
		return nil, err
	}

	return result, nil
}
