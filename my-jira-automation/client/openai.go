package jira

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
)

const openaiURL = "https://api.openai.com/v1/chat/completions"

// Request OpenAIRequest Define the request payload for OpenAI
type Request struct {
	Model    string    `json:"model"`
	Messages []Message `json:"messages"`
}

// Message OpenAIMessage Define the message structure
type Message struct {
	Role    string `json:"role"`
	Content string `json:"content"`
}

// Response Define the response structure
type Response struct {
	Choices []struct {
		Message struct {
			Role    string `json:"role"`
			Content string `json:"content"`
		} `json:"message"`
	} `json:"choices"`
}

// RequestChatGPT Function to request ChatGPT
func RequestChatGPT(apiKey string, prompt string) (string, error) {
	// Create the request payload
	requestBody := Request{
		Model: "gpt-3.5-turbo", // Specify the model
		Messages: []Message{
			{
				Role:    "user",
				Content: prompt,
			},
		},
	}

	// Serialize the request to JSON
	jsonBody, err := json.Marshal(requestBody)
	if err != nil {
		return "", err
	}

	// Create a new HTTP request
	req, err := http.NewRequest("POST", openaiURL, bytes.NewBuffer(jsonBody))
	if err != nil {
		return "", err
	}

	// Set the necessary headers
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("Authorization", "Bearer "+apiKey)

	// Perform the request
	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()

	// Read the response body
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return "", err
	}

	// Parse the response JSON
	var openAIResp Response
	err = json.Unmarshal(body, &openAIResp)
	if err != nil {
		return "", err
	}

	// Extract and return the content of the first choice
	if len(openAIResp.Choices) > 0 {
		return openAIResp.Choices[0].Message.Content, nil
	}

	return "", fmt.Errorf("no response from OpenAI")
}
