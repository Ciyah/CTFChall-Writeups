package config

import (
	"fmt"
	"os"
)

type Config struct {
	Port         string
	JWTSecret    string
	ClientSecret string
}

func LoadConfig() (*Config, error) {
	port := os.Getenv("PORT")
	if port == "" {
		port = "3002" // default port
	}

	jwtSecret := os.Getenv("JWT_SECRET")
	if jwtSecret == "" {
		return nil, fmt.Errorf("JWT_SECRET environment variable is required")
	}

	clientSecret := os.Getenv("CLIENT_SECRET")
	if clientSecret == "" {
		return nil, fmt.Errorf("CLIENT_SECRET environment variable is required")
	}

	return &Config{
		Port:         port,
		JWTSecret:    jwtSecret,
		ClientSecret: clientSecret,
	}, nil
}
