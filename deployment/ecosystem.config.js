module.exports = {
  apps : [{
    name   : "digital_fte_orchestrator",
    script : "src/main.py",
    interpreter: "python3",
    cwd: "/path/to/digital-fte-starter-kit",
    watch: false,
    autorestart: true,
    restart_delay: 5000,
    env: {
      ENV_STATE: "production"
    }
  }]
}
