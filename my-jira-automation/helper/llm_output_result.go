package helper

import (
	"encoding/json"
	"log"
)

type LLMOutputResult struct {
	JiraTicketsInfo []struct {
		Title       string `json:"title"`
		Description string `json:"description"`
		Day         int    `json:"day"`
	} `json:"jira_tickets_info"`
}

func (llm *LLMOutputResult) BuildLLMOutputResult(jsonLLMResponse string) *LLMOutputResult {
	err := json.Unmarshal([]byte(jsonLLMResponse), &llm)
	if err != nil {
		log.Fatal(err)
	}
	return llm
}
