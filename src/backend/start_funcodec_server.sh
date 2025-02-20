#!/bin/bash

# Set session name
SESSION="Distributed_LauraGPT_TTS"

# Start a new tmux session in detached mode
tmux new-session -d -s $SESSION

# Define ports
ports=(5010 5011 5012 5013)

# Create horizontal splits dynamically (split one less time than the number of elements)
for ((i = 1; i < ${#ports[@]}; i++)); do
    tmux split-window -h  # Split horizontally
done

# Adjust layout after all splits are done
tmux select-layout tiled  # Adjust layout

# Loop through panes and send commands
for ((i = 0; i < ${#ports[@]}; i++)); do
  # Send command to each pane
  tmux send-keys -t $SESSION:0.$i "python funcodec_server.py --port ${ports[$i]} --device 5" C-m
done

# Attach to session
tmux attach-session -t $SESSION

