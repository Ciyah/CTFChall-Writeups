package database

import (
	"log"
	"os"
	"sso-service/internal/models"

	"golang.org/x/crypto/bcrypt"
	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
)

var DB *gorm.DB

func InitDB(clientSecret string) error {
	var err error
	DB, err = gorm.Open(sqlite.Open("sso.db"), &gorm.Config{})
	if err != nil {
		return err
	}

	err = DB.AutoMigrate(&models.User{})
	if err != nil {
		return err
	}
	err = DB.AutoMigrate(&models.OAuthClient{})
	if err != nil {
		return err
	}
	err = DB.AutoMigrate(&models.OAuthAuthorization{})
	if err != nil {
		return err
	}
	err = DB.AutoMigrate(&models.OAuthAccessToken{})
	if err != nil {
		return err
	}
	err = DB.AutoMigrate(&models.OAuthApproval{})
	if err != nil {
		return err
	}

	log.Println("[+] Database initialization")

	clientID := "1a2abb8b-9bb5-4463-8f74-d7b129bb7040"
	client := models.OAuthClient{
		ClientID:     clientID,
		ClientSecret: clientSecret,
		Name:         "edulearn",
		RedirectURI:  "http://edulearn.htb:1337/oauth/callback",
		Active:       true,
	}
	if DB.Where("client_id = ?", clientID).First(&client).Error != nil {
		log.Println("[+] Creating client: ", clientID)
		DB.Create(&client)
	}
	
	// Initialize teacher accounts
	initTeacherAccounts()
	
	return nil
}

// initTeacherAccounts creates default teacher accounts if they don't exist
func initTeacherAccounts() {
	// Get password from environment variable
	teacherPassword := os.Getenv("TEACHER_PASSWORD")
	if teacherPassword == "" {
		log.Println("[!] WARNING: TEACHER_PASSWORD not set, using default")
		teacherPassword = "teacher123"
	}
	
	teachers := []struct {
		Email    string
		Name     string
		Password string
	}{
		{"teacher@edulearn.htb", "Dr. Sarah Johnson", teacherPassword},
	}
	
	for _, t := range teachers {
		var existingUser models.User
		if DB.Where("email = ?", t.Email).First(&existingUser).Error != nil {
			// Teacher doesn't exist, create it
			// Hash password using bcrypt (same as registration)
			hashedPassword, err := hashPassword(t.Password)
			if err != nil {
				log.Printf("[!] ERROR: Failed to hash password for %s", t.Email)
				continue
			}
			
			teacher := models.User{
				Email:    t.Email,
				Name:     t.Name,
				Password: hashedPassword,
				Role:     "teacher",
			}
			
			if err := DB.Create(&teacher).Error; err != nil {
				log.Printf("[!] ERROR: Failed to create teacher account %s: %v", t.Email, err)
			} else {
				log.Printf("[+] Created teacher account: %s", t.Email)
			}
		}
	}
}

// hashPassword hashes a plain text password using bcrypt
func hashPassword(password string) (string, error) {
	hashedBytes, err := bcrypt.GenerateFromPassword([]byte(password), bcrypt.DefaultCost)
	if err != nil {
		return "", err
	}
	return string(hashedBytes), nil
}
