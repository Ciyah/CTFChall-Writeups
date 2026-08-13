package handlers

import (
	"fmt"
	"net"
	"net/http"
	"net/url"
	"sso-service/internal/database"
	"sso-service/internal/models"
	"sso-service/utils"
	"strings"
	"time"

	"github.com/gin-gonic/gin"
)

func validateRedirectURI(provided, registered, requestHost string) error {
	providedURL, err := url.Parse(provided)
	if err != nil {
		return fmt.Errorf("invalid redirect_uri format")
	}

	registeredURL, err := url.Parse(registered)
	if err != nil {
		return fmt.Errorf("server configuration error")
	}

	if providedURL.Scheme != registeredURL.Scheme {
		return fmt.Errorf("scheme mismatch")
	}

	if !strings.HasPrefix(providedURL.Path, registeredURL.Path) {
		return fmt.Errorf("invalid callback path")
	}

	_, requestPort, _ := net.SplitHostPort(requestHost)
	if requestPort == "" {
		requestPort = "80"
	}

	providedPort := providedURL.Port()
	if providedPort == "" {
		providedPort = "80"
	}

	if providedPort != requestPort {
		return fmt.Errorf("port mismatch")
	}

	if providedURL.Hostname() != registeredURL.Hostname() {
		return fmt.Errorf("invalid hostname")
	}

	return nil
}

type OAuthHandler struct{}

func NewOAuthHandler() *OAuthHandler {
	return &OAuthHandler{}
}

func (h *OAuthHandler) createAuthorizationCode(c *gin.Context, clientID, scope, redirectURI, state string) {
	// Generate authorization code
	code := utils.GenerateRandomString(32)

	// Store authorization
	auth := models.OAuthAuthorization{
		UserID:      c.GetUint("userID"),
		ClientID:    clientID,
		Code:        code,
		RedirectURI: redirectURI,
		ExpiresAt:   time.Now().Add(10 * time.Minute),
		Scope:       scope,
		State:       state,
	}

	if err := database.DB.Create(&auth).Error; err != nil {
		c.HTML(http.StatusInternalServerError, "error.tmpl", gin.H{
			"error": "Failed to create authorization",
		})
		return
	}

	// Redirect back to client
	redirectURL := redirectURI + "?code=" + code
	if state != "" {
		redirectURL += "&state=" + state
	}

	c.Redirect(http.StatusFound, redirectURL)
}

func (h *OAuthHandler) Authorize(c *gin.Context) {
	clientID := c.Query("client_id")
	responseType := c.Query("response_type")
	redirectURI := c.Query("redirect_uri")
	scope := c.Query("scope")
	state := c.Query("state")

	// Validate required parameters
	if clientID == "" || responseType == "" || redirectURI == "" {
		c.HTML(http.StatusBadRequest, "error.tmpl", gin.H{
			"error": "Missing required parameters",
		})
		return
	}

	// Validate response_type
	if responseType != "code" {
		c.HTML(http.StatusBadRequest, "error.tmpl", gin.H{
			"error": "Invalid response type",
		})
		return
	}

	// Validate client
	var client models.OAuthClient
	if err := database.DB.Where("client_id = ? AND active = ?", clientID, true).First(&client).Error; err != nil {
		c.HTML(http.StatusBadRequest, "error.tmpl", gin.H{
			"error": "Invalid client",
		})
		return
	}

	if err := validateRedirectURI(redirectURI, client.RedirectURI, c.Request.Host); err != nil {
		c.HTML(http.StatusBadRequest, "error.tmpl", gin.H{
			"error": "Invalid redirect URI",
		})
		return
	}

	// Check if user has already approved this client with the same or broader scope
	userID := c.GetUint("userID")
	var approval models.OAuthApproval
	uniqueApproval := fmt.Sprintf("%d:%s:%s", userID, clientID, scope)

	if err := database.DB.Where("unique_approval = ?", uniqueApproval).First(&approval).Error; err == nil {
		// User has already approved, create authorization code and redirect
		h.createAuthorizationCode(c, clientID, scope, redirectURI, state)
		return
	}

	// If not previously approved, show the authorization page
	c.HTML(http.StatusOK, "oauth/authorize.tmpl", gin.H{
		"clientName":  client.Name,
		"clientID":    clientID,
		"scope":       scope,
		"state":       state,
		"redirectURI": redirectURI,
		"scopes":      strings.Split(scope, " "),
	})
}

func (h *OAuthHandler) HandleAuthorize(c *gin.Context) {
	clientID := c.PostForm("client_id")
	scope := c.PostForm("scope")
	redirectURI := c.PostForm("redirect_uri")
	state := c.PostForm("state")
	approved := c.PostForm("approved")

	// Check if user approved
	if approved != "true" {
		redirectURL := redirectURI + "?error=access_denied"
		if state != "" {
			redirectURL += "&state=" + state
		}
		c.Redirect(http.StatusFound, redirectURL)
		return
	}

	// Validate client
	var client models.OAuthClient
	if err := database.DB.Where("client_id = ? AND active = ?", clientID, true).First(&client).Error; err != nil {
		c.HTML(http.StatusBadRequest, "error.tmpl", gin.H{
			"error": "Invalid client",
		})
		return
	}

	if err := validateRedirectURI(redirectURI, client.RedirectURI, c.Request.Host); err != nil {
		c.HTML(http.StatusBadRequest, "error.tmpl", gin.H{
			"error": "Invalid redirect URI",
		})
		return
	}

	// Store user approval
	userID := c.GetUint("userID")
	uniqueApproval := fmt.Sprintf("%d:%s:%s", userID, clientID, scope)
	approval := models.OAuthApproval{
		UserID:         userID,
		ClientID:       clientID,
		Scope:          scope,
		UniqueApproval: uniqueApproval,
	}

	if err := database.DB.Create(&approval).Error; err != nil {
		c.HTML(http.StatusInternalServerError, "error.tmpl", gin.H{
			"error": "Failed to store approval",
		})
		return
	}

	// Create authorization code and redirect
	h.createAuthorizationCode(c, clientID, scope, redirectURI, state)
}

func (h *OAuthHandler) Token(c *gin.Context) {
	grantType := c.PostForm("grant_type")
	clientID := c.PostForm("client_id")
	clientSecret := c.PostForm("client_secret")
	code := c.PostForm("code")
	redirectURI := c.PostForm("redirect_uri")

	// Validate grant type
	if grantType != "authorization_code" {
		c.JSON(http.StatusBadRequest, gin.H{
			"error":             "unsupported_grant_type",
			"error_description": "Only authorization_code grant type is supported",
		})
		return
	}

	// Validate client credentials
	var client models.OAuthClient
	if err := database.DB.Where("client_id = ? AND active = ?", clientID, true).First(&client).Error; err != nil {
		c.JSON(http.StatusUnauthorized, gin.H{
			"error":             "invalid_client",
			"error_description": "Invalid client credentials",
		})
		return
	}

	// Validate client secret
	if client.ClientSecret != clientSecret {
		c.JSON(http.StatusUnauthorized, gin.H{
			"error":             "invalid_client",
			"error_description": "Invalid client credentials",
		})
		return
	}

	// Validate authorization code
	var auth models.OAuthAuthorization
	if err := database.DB.Where(
		"code = ? AND client_id = ? AND used = ? AND expires_at > ?",
		code, clientID, false, time.Now(), redirectURI,
	).First(&auth).Error; err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error":             "invalid_grant",
			"error_description": "Invalid authorization code",
		})
		return
	}

	// Mark the authorization code as used
	if err := database.DB.Model(&auth).Update("used", true).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"error":             "server_error",
			"error_description": "Failed to process token request",
		})
		return
	}

	// Generate access token
	accessToken := utils.GenerateRandomString(32)
	refreshToken := utils.GenerateRandomString(32)

	token := models.OAuthAccessToken{
		UserID:       auth.UserID,
		ClientID:     auth.ClientID,
		Token:        accessToken,
		RefreshToken: refreshToken,
		ExpiresAt:    time.Now().Add(time.Hour * 24),
		Scope:        auth.Scope,
	}

	if err := database.DB.Create(&token).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"error":             "server_error",
			"error_description": "Failed to create access token",
		})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"access_token":  accessToken,
		"token_type":    "Bearer",
		"expires_in":    int(time.Hour * 24 / time.Second),
		"refresh_token": refreshToken,
		"scope":         auth.Scope,
	})
}

func (h *OAuthHandler) UserInfo(c *gin.Context) {
	accessToken := strings.Split(c.GetHeader("Authorization"), " ")[1]
	if accessToken == "" {
		c.JSON(http.StatusUnauthorized, gin.H{"error": "Missing access token"})
		return
	}

	var token models.OAuthAccessToken
	if err := database.DB.Where("token = ?", accessToken).First(&token).Error; err != nil {
		c.JSON(http.StatusUnauthorized, gin.H{"error": "Invalid access token"})
		return
	}
	userID := token.UserID
	scope := strings.Split(token.Scope, " ")

	var user models.User
	if err := database.DB.Where("id = ?", userID).First(&user).Error; err != nil {
		c.JSON(http.StatusUnauthorized, gin.H{"error": "User not found"})
		return
	}
	userInfo := gin.H{}
	for _, s := range scope {
		switch s {
		case "profile":
			userInfo["name"] = user.Name
			userInfo["email"] = user.Email
			userInfo["role"] = user.Role // Include role in profile
		case "email":
			userInfo["email"] = user.Email
		case "name":
			userInfo["name"] = user.Name
		}
	}
	// Always include role for authorization purposes
	userInfo["role"] = user.Role
	c.JSON(http.StatusOK, userInfo)
}
