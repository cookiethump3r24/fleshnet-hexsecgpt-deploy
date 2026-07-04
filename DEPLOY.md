# Deploy to Hugging Face Spaces

1. Open the Docker Space `Nussy24/fleshnet-hexsecgpt`.
2. Upload every file from this package, preserving the `wrapper/` folder.
3. Commit the files to the Space repository.
4. Open **Settings → Variables and secrets**.
5. Add the secret `HEXSECGPT_API_KEY`.
6. Optionally add `HEXSECGPT_PROVIDER=openrouter` and a current `HEXSECGPT_MODEL`.
7. Wait for the Docker build to finish.
8. Open `/health` and confirm `ok` is `true` and `api_key_configured` is `true`.
9. In FleshNet, use:

   `https://nussy24-fleshnet-hexsecgpt.hf.space/v1/chat/completions`

The Space listens on port 7860 as required by Hugging Face Docker Spaces.
