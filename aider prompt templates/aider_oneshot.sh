prompt="$1"
aider \
    --model o3-mini \
    --architect \
    --reasoning-effort high \
    --editor-model o3-mini  \
    --detect-urls \
    --no-auto-commit \
    --yes-always \
    --file *.py \
    --message "$prompt" 