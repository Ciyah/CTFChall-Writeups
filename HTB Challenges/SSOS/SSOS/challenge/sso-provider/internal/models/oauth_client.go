package models

import "gorm.io/gorm"

type OAuthClient struct {
	gorm.Model
	ClientID     string `gorm:"unique;not null" json:"client_id"`
	ClientSecret string `gorm:"not null" json:"-"`
	Name         string `gorm:"not null" json:"name"`
	RedirectURI  string `gorm:"not null" json:"redirect_uri"`
	Active       bool   `gorm:"not null;default:true" json:"active"`
}
