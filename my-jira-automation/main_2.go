package main

import (
	jira "ca.cricri/m/v2/my-jira-automation/client"
	"fmt"
	"log"
	"os"
	"time"
)

// TODO : setup Tempo
func main() {
	// update tempo
	tempo := os.Getenv("TEMPO_API_KEY")
	projectAccountId := os.Getenv("JIRA_ACCOUNT_ID")

	startDate := "startDate"
	timeSpentSeconds := 27000

	baseURL := os.Getenv("JIRA_BASE_URL")
	username := os.Getenv("JIRA_USERNAME")
	projectID := os.Getenv("JIRA_PROJECT_ID")
	apiToken := os.Getenv("JIRA_API_TOKEN")

	// Create ticket
	jiraClient := jira.NewJiraClient(baseURL, username, apiToken, projectID)

	ticket, err := jiraClient.GetTicket("BDEP-21")
	if err != nil {
		log.Fatal(err)
	}

	authorAccountId := projectAccountId
	log.Printf("authorAccountId - %s", authorAccountId)

	issueId := ticket["id"].(string)
	log.Printf("issueId - %s", issueId)

	println(startDate)
	println(timeSpentSeconds)
	println(tempo + ";")
	println(projectAccountId + ";")
	workDayOfWeek, err := getWorkDaysFromDate("")
	if err != nil {
		return
	}

	for index, workDay := range workDayOfWeek {
		fmt.Printf("Index: %d, CurrentWorkDay: %s\n", index, workDay)
	}

}

// Function to return all weekdays (Monday to Friday) of the week of the given date
// Thanks chatgpt
func getWorkDaysFromDate(inputDate string) ([]string, error) {
	if inputDate == "" {
		todayDate := time.Now()
		inputDate = todayDate.Format("02-01-2006")
	}
	// Parse the input date string
	date, err := time.Parse("02-01-2006", inputDate)
	if err != nil {
		return nil, err
	}

	// Create a slice to store the ordered set of workdays
	workDaysOrderedSet := []string{}

	// Find the week's Monday for the given date
	offset := int(time.Monday - date.Weekday())
	if offset > 0 {
		offset = -6 // If the date is Sunday, go back 6 days to get the last Monday
	}
	monday := date.AddDate(0, 0, offset)

	// Add weekdays (Monday to Friday) to the slice
	for i := 0; i < 5; i++ {
		day := monday.AddDate(0, 0, i)
		workDaysOrderedSet = append(workDaysOrderedSet, day.Format("02-01-2006"))
	}

	return workDaysOrderedSet, nil
}
