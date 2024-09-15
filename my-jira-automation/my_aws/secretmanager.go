package my_aws

import (
	"context"
	"github.com/aws/aws-sdk-go-v2/aws"
	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/secretsmanager"
	"log"
)

// SecretManagerClient AWS Secret Manager Client
type SecretManagerClient struct {
	SMClient *secretsmanager.Client
}

// NewAwsSMClient is the constructor function for JiraClient
func NewAwsSMClient(region string) *SecretManagerClient {
	if region == "" {
		region = "ca-central-1"
	}

	awsSMConfig, err := config.LoadDefaultConfig(context.TODO(), config.WithRegion(region))
	if err != nil {
		log.Fatal(err)
	}

	// Create Secrets Manager client
	return &SecretManagerClient{
		SMClient: secretsmanager.NewFromConfig(awsSMConfig),
	}
}

func (s *SecretManagerClient) GetSecretValue(secretName string) string {
	if secretName == "" {
		secretName = "my-jira-automation/mdc"
	}

	input := &secretsmanager.GetSecretValueInput{
		SecretId:     aws.String(secretName),
		VersionStage: aws.String("AWSCURRENT"),
	}

	result, err := s.SMClient.GetSecretValue(context.TODO(), input)
	if err != nil {
		log.Fatal(err.Error())
	}

	return *result.SecretString
}
