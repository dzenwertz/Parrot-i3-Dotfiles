#!/usr/bin/env bash

# Terminate already running bar instances
# If all your bars have ipc enabled, you can use 
/usr/bin/polybar-msg cmd quit || killall -q polybar
sleep 1

# Launch bar1 and bar2
echo "---" | tee -a /tmp/polybar1.log 
/usr/bin/polybar bar 2>&1 | tee -a /tmp/polybar1.log & disown
# polybar bar2 2>&1 | tee -a /tmp/polybar2.log & disown

echo "Bars launched..."
