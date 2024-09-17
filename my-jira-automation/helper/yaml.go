package helper

import (
	"gopkg.in/yaml.v2"
	"log"
	"os"
)

type MyJiraAutomation struct {
	APIVersion string `yaml:"apiVersion"`
	Jira       struct {
		Prompt []struct {
			DataEngineer string `yaml:"dataEngineer,omitempty"`
			DevOps       string `yaml:"devOps,omitempty"`
		} `yaml:"prompt"`
	} `yaml:"jira"`
}

func (c *MyJiraAutomation) GetMyJiraPromptConf() *MyJiraAutomation {
	yamlFile, err := os.ReadFile("resources/jira_ticket_prompt.yaml")
	if err != nil {
		log.Printf("yamlFile.Get err   #%v ", err)
	}
	err = yaml.Unmarshal(yamlFile, c)
	if err != nil {
		log.Fatalf("Unmarshal: %v", err)
	}

	return c
}
