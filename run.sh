cat > run.sh << EOL
#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Run Flask app in background
python app.py &

# Tunnel using localhost.run (no warning page)
ssh -R 80:localhost:7860 ssh.localhost.run
EOL
