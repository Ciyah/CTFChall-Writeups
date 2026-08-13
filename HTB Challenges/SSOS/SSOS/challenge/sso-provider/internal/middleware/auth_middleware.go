package middleware

import (
	"net/http"
	"net/url"
	"sso-service/internal/auth"

	"github.com/gin-gonic/gin"
)

func AuthRequired() gin.HandlerFunc {
	return func(c *gin.Context) {
		token, err := c.Cookie("token")
		if err != nil {
			c.Redirect(http.StatusSeeOther, "/login?redirect="+url.QueryEscape(c.Request.URL.String()))
			return
		}

		claims, err := auth.ValidateToken(token)
		if err != nil {
			c.Redirect(http.StatusSeeOther, "/login?redirect="+url.QueryEscape(c.Request.URL.String()))
			return
		}

		c.Set("userID", claims.UserID)
		c.Set("email", claims.Email)
		c.Set("name", claims.Name)
		c.Next()
	}
}
