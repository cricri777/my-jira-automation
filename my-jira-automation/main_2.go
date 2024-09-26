package main

import (
	"bytes"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
)

// TODO : setup Tempo
func main() {
	// update tempo
	tempo := os.Getenv("TEMPO_API_KEY")

	postUrl := fmt.Sprintf("https://api.tempo.io/4/worklogs")

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
			"summary": "%s",
			"description": "%s"
		  }
		}`, summary, description)

	bodyByte := []byte(body)
	request, err := http.NewRequest("POST", postUrl, bytes.NewBuffer(bodyByte))

	// Set the authentication header
	request.SetBasicAuth(c.userName, c.apiToken)
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
		log.Printf("Failed to create ticket. Status: %s, Body: %s\n", res.Status, res.Body)
	}

}
