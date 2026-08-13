package models

import (
	"time"

	"gorm.io/gorm"
)

type OAuthAuthorization struct {
	gorm.Model
	UserID      uint      `gorm:"not null"`
	ClientID    string    `gorm:"not null"`
	Scope       string    `gorm:"not null"`
	State       string    `gorm:"not null"`
	RedirectURI string    `gorm:"not null"`
	Code        string    `gorm:"unique;not null"`
	Used        bool      `gorm:"not null;default:false"`
	ExpiresAt   time.Time `gorm:"not null"`
}

type OAuthAccessToken struct {
	gorm.Model
	UserID       uint      `gorm:"not null"`
	ClientID     string    `gorm:"not null"`
	Token        string    `gorm:"unique;not null"`
	RefreshToken string    `gorm:"unique;not null"`
	ExpiresAt    time.Time `gorm:"not null"`
	Scope        string    `gorm:"not null"`
}

type OAuthApproval struct {
	gorm.Model
	UserID   uint   `gorm:"not null"`
	ClientID string `gorm:"not null"`
	Scope    string `gorm:"not null"`
	// Composite unique index to prevent duplicate approvals
	UniqueApproval string `gorm:"uniqueIndex:idx_user_client_scope"`
}
