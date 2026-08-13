package main

import (
	"log"
	"net/http"
	"sso-service/internal/api/handlers"
	"sso-service/internal/auth"
	"sso-service/internal/config"
	"sso-service/internal/database"
	"sso-service/internal/middleware"
	"time"

	"github.com/gin-gonic/gin"
)

// CustomLogger middleware for logging requests
func CustomLogger() gin.HandlerFunc {
	return func(c *gin.Context) {
		// Start timer
		start := time.Now()

		// Process request
		c.Next()

		// Log only after request is processed
		latency := time.Since(start)
		log.Printf("[%s] %s %s | %d | %v",
			c.Request.Method,
			c.Request.URL.Path,
			c.ClientIP(),
			c.Writer.Status(),
			latency,
		)
	}
}

func main() {
	// Load configuration
	cfg, err := config.LoadConfig()
	if err != nil {
		log.Fatalf("Failed to load configuration: %v", err)
	}

	// Initialize auth with JWT secret
	if err := auth.Initialize(cfg.JWTSecret); err != nil {
		log.Fatalf("Failed to initialize auth: %v", err)
	}

	// Disable Gin debug output
	gin.SetMode(gin.ReleaseMode)

	// Initialize database
	if err := database.InitDB(cfg.ClientSecret); err != nil {
		log.Fatalf("Failed to initialize database: %v", err)
	}
	log.Println("[+] Database initialized successfully")

	// Initialize handlers
	authHandler := handlers.NewAuthHandler()
	userHandler := handlers.NewUserHandler()
	oauthHandler := handlers.NewOAuthHandler()
	authMiddleware := middleware.AuthRequired()

	// Create router with custom configuration
	r := gin.New() // Use New() instead of Default()

	// Add only necessary middleware
	r.Use(gin.Recovery()) // Keep recovery for safety
	r.Use(CustomLogger()) // Add our custom logger

	// Load templates
	r.LoadHTMLGlob("web/templates/*")
	log.Println("[+] Templates loaded successfully")

	// Serve static files
	r.Static("/web/static", "web/static")

	// Routes
	r.GET("/", func(c *gin.Context) {
		token, err := c.Cookie("token")
		if err != nil {
			c.Redirect(http.StatusSeeOther, "/login?redirect=/")
			return
		}
		claims, err := auth.ValidateToken(token)
		if err != nil {
			c.Redirect(http.StatusSeeOther, "/login?redirect=/")
			return
		}

		c.HTML(http.StatusOK, "home.tmpl", gin.H{
			"user": gin.H{
				"Name":  claims.Name,
				"Email": claims.Email,
			},
		})
	})

	r.GET("/login", func(c *gin.Context) {
		c.HTML(http.StatusOK, "login.tmpl", gin.H{})
	})

	r.GET("/register", func(c *gin.Context) {
		c.HTML(http.StatusOK, "register.tmpl", gin.H{})
	})

	// API routes
	api := r.Group("/api")
	{
		api.POST("/register", authHandler.Register)
		api.POST("/login", authHandler.Login)
		api.GET("/user", authMiddleware, userHandler.GetUserInfo)
	}

	oauth := r.Group("/oauth", authMiddleware)
	{
		oauth.GET("/authorize", oauthHandler.Authorize)
		oauth.POST("/authorize", oauthHandler.HandleAuthorize)
		oauth.POST("/token", oauthHandler.Token)
	}
	r.GET("/oauth/userinfo", oauthHandler.UserInfo)

	log.Printf("[+] Starting server on :%s", cfg.Port)
	if err := r.Run(":" + cfg.Port); err != nil {
		log.Fatalf("Failed to start server: %v", err)
	}
}
