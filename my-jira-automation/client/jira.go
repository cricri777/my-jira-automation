package client

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
	BaseURL   string
	Username  string
	APIToken  string
	ProjectID string
}

// NewJiraClient is the constructor function for JiraClient
func NewJiraClient(baseURL, username, apiToken, projectID string) *JiraClient {
	return &JiraClient{
		BaseURL:   baseURL,
		Username:  username,
		APIToken:  apiToken,
		ProjectID: projectID,
	}
}

func (c *JiraClient) CreateTicket(accountID string) {
	postUrl := fmt.Sprintf("%s/rest/api/2/issue/%s", c.BaseURL)

	body := []byte(`{
		"title": "Post title",
		"body": "Post description",
		"userId": 1
	}`)

	request, err := http.NewRequest("POST", postUrl, bytes.NewBuffer(body))
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

	post := &Post{}
	derr := json.NewDecoder(res.Body).Decode(post)
	if derr != nil {
		log.Fatal(derr)
	}

	if res.StatusCode != http.StatusCreated {
		log.Fatal(res.Status)
	}

	fmt.Println("Id:", post.Id)
	fmt.Println("Title:", post.Title)
	fmt.Println("Body:", post.Body)
	fmt.Println("UserId:", post.UserId)

}

// GetTicket get a ticket from Jira
func (c *JiraClient) GetTicket(ticketKey string) (map[string]interface{}, error) {
	url := fmt.Sprintf("%s/rest/api/2/issue/%s", c.BaseURL, ticketKey)

	// Create a new HTTP request
	req, err := http.NewRequest("GET", url, nil)
	if err != nil {
		return nil, err
	}

	// Set the authentication header
	req.SetBasicAuth(c.Username, c.APIToken)
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
