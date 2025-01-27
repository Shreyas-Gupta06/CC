#!/bin/zsh

# Function to check if already logged in
check_logged_in() {
    page_content=$(curl -s http://www.google.com)

    # If we are redirected, we are not logged in
    if echo "$page_content" | grep -q "window.location=.*fgtauth"; then
        return 1
    else
        echo "Already logged in. No need to authenticate."
        return 0
    fi
}

# Check if already logged in
check_logged_in
logged_in=$?

# If not logged in, attempt login
if [ $logged_in -ne 0 ]; then
    while true; do
        

        # Step 1: Trigger the captive portal redirect
        initial_response=$(curl -s -L "http://edge-http.microsoft.com/captiveportal/generate_204")
        
        # Step 2: Extract the redirected login page URL
        login_url=$(echo "$initial_response" | grep -oP 'location="\K[^"]+')

        if [ -z "$login_url" ]; then
            echo "Failed to fetch the login page. Exiting."
            exit 1
        fi

        # Step 3: Fetch the actual login page to get the token
        login_page=$(curl -s -L "$login_url")

        # Step 4: Extract magic token and 4Tredir value
        token=$(echo "$login_page" | grep -oP 'name="magic" value="\K[^"]+')
        redirect_url=$(echo "$login_page" | grep -oP 'name="4Tredir" value="\K[^"]+')

        # Debug Information
        echo "Extracted token: $token"
        echo "Redirect URL: $redirect_url"

        if [ -z "$token" ]; then
            echo "Token extraction failed. Exiting."
            exit 1
        fi
        echo "Please enter your BITS WiFi credentials."

        # Username and Password Prompt
        read -p "Username: " username
        read -sp "Password: " password
        

        # Step 5: Send credentials via POST request
        response=$(curl -s -d "username=$username&password=$password&magic=$token" \
                  -X POST "$login_url")

        # Step 6: Check if login was successful
        if echo "$response" | grep -q "You are connected"; then
            echo "Login successful!"
            break
        else
            echo "Login failed. Please check your credentials and try again."
        fi
    done
fi
