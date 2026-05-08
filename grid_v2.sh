#!/bin/bash

# Essentium Grid Terminal v2 - with Reality Harvest
NODES_FILE="nodes.txt"
CONNECTIONS_FILE="connections.txt"
BALANCE_FILE=".pac_balance"
MULTIPLIER_FILE=".multiplier"

# Load or init balance
if [ -f "$BALANCE_FILE" ]; then
  PAC_BALANCE=$(cat "$BALANCE_FILE")
else
  PAC_BALANCE=0
fi

# Load or init multiplier (1x = 1, 3x = 3, 3.6x = 360/100 stored as integer)
if [ -f "$MULTIPLIER_FILE" ]; then
  MULTIPLIER=$(cat "$MULTIPLIER_FILE")
else
  MULTIPLIER=1
fi

save_balance() {
  echo "$PAC_BALANCE" > "$BALANCE_FILE"
}

save_multiplier() {
  echo "$MULTIPLIER" > "$MULTIPLIER_FILE"
}

init_files() {
  touch "$NODES_FILE" "$CONNECTIONS_FILE"
}

add_node() {
  echo "$1|$2|$3" >> "$NODES_FILE"
  echo "✓ Added node: $1 ($2, $3 Hz)"
}

connect_nodes() {
  if grep -q "^$1|$2$" "$CONNECTIONS_FILE" || grep -q "^$2|$1$" "$CONNECTIONS_FILE"; then
    echo "⚠️  Connection already exists!"
    return
  fi
  echo "$1|$2" >> "$CONNECTIONS_FILE"
  echo "🔗 Connected $1 ↔ $2"
}

harvest_nodes() {
  local total=0
  local node_reward=0
  local connection_bonus=0
  local resonance=0
  
  echo "--- Node Harvest ---"
  while IFS='|' read -r name type freq; do
    local conn_count=$(grep -c "^$name|" "$CONNECTIONS_FILE")
    conn_count=$((conn_count + $(grep -c "|$name$" "$CONNECTIONS_FILE")))
    resonance=$((conn_count * 4))
    node_reward=$((2 + resonance))
    total=$((total + node_reward))
    echo "  🌿 $name → ${node_reward} PaC (base 2 + ${resonance} resonance)"
  done < "$NODES_FILE"
  
  local unique_pairs=$(sort "$CONNECTIONS_FILE" | uniq | wc -l)
  connection_bonus=$((unique_pairs * 2))
  total=$((total + connection_bonus))
  echo "  🔗 Connection bonus: ${connection_bonus} PaC"
  
  PAC_BALANCE=$((PAC_BALANCE + total))
  save_balance
  echo "⛏️  Harvested ${total} PaC from grid | Total: ${PAC_BALANCE} PaC"
  echo ""
}

forge() {
  if [ "$MULTIPLIER" -ge 3 ]; then
    echo "❌ Neo-Genesis already forged! Multiplier is already ${MULTIPLIER}x"
    return
  fi
  if [ $PAC_BALANCE -lt 50 ]; then
    echo "❌ Not enough PaC! Need 50, you have ${PAC_BALANCE}"
    return
  fi
  PAC_BALANCE=$((PAC_BALANCE - 50))
  MULTIPLIER=3
  save_balance
  save_multiplier
  echo "🔨 Forged Neo-Genesis! Spent 50 PaC → Yield multiplier is now 3x"
  echo "💰 Remaining PaC: ${PAC_BALANCE}"
}

merge() {
  if [ "$MULTIPLIER" -ge 4 ]; then
    echo "❌ Quantum dimension already merged!"
    return
  fi
  if [ "$MULTIPLIER" -lt 3 ]; then
    echo "❌ You must forge Neo-Genesis (3x) before merging Quantum!"
    return
  fi
  if [ $PAC_BALANCE -lt 45 ]; then
    echo "❌ Not enough PaC! Need 45, you have ${PAC_BALANCE}"
    return
  fi
  PAC_BALANCE=$((PAC_BALANCE - 45))
  MULTIPLIER=360  # store as integer 3.6 = 360/100
  save_balance
  save_multiplier
  echo "🌀 Merged Quantum dimension! Spent 45 PaC → Yield multiplier is now 3.6x"
  echo "💰 Remaining PaC: ${PAC_BALANCE}"
}

harvest_reality() {
  local base_yield=75
  local multiplier_value
  if [ "$MULTIPLIER" -eq 360 ]; then
    multiplier_value=3.6
  else
    multiplier_value=$MULTIPLIER
  fi
  local earned=$(echo "$base_yield * $multiplier_value" | bc)
  # bc returns integer if both are integer? 75*3.6 = 270.0, convert to integer
  earned=${earned%.*}
  PAC_BALANCE=$((PAC_BALANCE + earned))
  save_balance
  echo "🌾 Harvest Reality: Base 75 × ${multiplier_value}x = ${earned} PaC harvested!"
  echo "💰 New balance: ${PAC_BALANCE} PaC"
}

show_status() {
  echo ""
  echo "--- Nodes ---"
  if [ ! -s "$NODES_FILE" ]; then
    echo "(none)"
  else
    cat "$NODES_FILE" | while IFS='|' read -r name type freq; do
      conns=$(grep -c "^$name|" "$CONNECTIONS_FILE")
      conns=$((conns + $(grep -c "|$name$" "$CONNECTIONS_FILE")))
      echo "  $name ($type, $freq Hz) → $conns connection(s)"
    done
  fi
  echo ""
  echo "--- Connections ---"
  if [ ! -s "$CONNECTIONS_FILE" ]; then
    echo "(none)"
  else
    cat "$CONNECTIONS_FILE" | while IFS='|' read -r a b; do
      echo "  $a ↔ $b"
    done
  fi
  local multiplier_display
  if [ "$MULTIPLIER" -eq 360 ]; then
    multiplier_display="3.6x"
  else
    multiplier_display="${MULTIPLIER}x"
  fi
  echo ""
  echo "💰 Total PaC: $PAC_BALANCE"
  echo "✨ Reality Multiplier: $multiplier_display"
  echo ""
}

clear_data() {
  > "$NODES_FILE"
  > "$CONNECTIONS_FILE"
  PAC_BALANCE=0
  MULTIPLIER=1
  save_balance
  save_multiplier
  echo "🗑️  All nodes, connections, balance, and multiplier reset."
}

show_menu() {
  echo "=========================="
  echo "  Essentium Grid Terminal  "
  echo "=========================="
  echo "1) Add Node"
  echo "2) Connect Nodes"
  echo "3) Harvest Grid (nodes + connections)"
  echo "4) Show Status"
  echo "5) Clear all data"
  echo "6) Exit"
  echo "--- Reality Forge ---"
  echo "7) Forge \"Neo-Genesis\" (cost 50 PaC → 3x multiplier)"
  echo "8) Merge \"Quantum\" (cost 45 PaC → 3.6x multiplier)"
  echo "9) Harvest Reality (base 75 × current multiplier)"
  echo -n "Choose: "
}

# Initialise
init_files

# Pre-populate nodes if missing
if ! grep -q "Starlink-47" "$NODES_FILE" 2>/dev/null; then
  add_node "Starlink-47" "starlink" "432"
fi
if ! grep -q "Vivian-Core" "$NODES_FILE" 2>/dev/null; then
  add_node "Vivian-Core" "ai" "528"
fi
if ! grep -q "orion-9" "$NODES_FILE" 2>/dev/null; then
  add_node "orion-9" "satellite" "963"
fi
# Connect existing pairs if not already connected
if ! grep -q "Starlink-47|Vivian-Core" "$CONNECTIONS_FILE" 2>/dev/null && ! grep -q "Vivian-Core|Starlink-47" "$CONNECTIONS_FILE" 2>/dev/null; then
  connect_nodes "Starlink-47" "Vivian-Core"
fi
if ! grep -q "orion-9|Vivian-Core" "$CONNECTIONS_FILE" 2>/dev/null && ! grep -q "Vivian-Core|orion-9" "$CONNECTIONS_FILE" 2>/dev/null; then
  connect_nodes "orion-9" "Vivian-Core"
fi

# Main loop
while true; do
  show_menu
  read choice
  case $choice in
    1) echo -n "Node name: "; read name
       echo -n "Type (starlink/ai/other): "; read type
       echo -n "Frequency (Hz): "; read freq
       add_node "$name" "$type" "$freq"
       ;;
    2) echo -n "First node: "; read a
       echo -n "Second node: "; read b
       connect_nodes "$a" "$b"
       ;;
    3) harvest_nodes ;;
    4) show_status ;;
    5) clear_data ;;
    6) echo "🌌 Exiting grid. Goodbye!"; exit 0 ;;
    7) forge ;;
    8) merge ;;
    9) harvest_reality ;;
    *) echo "Invalid option" ;;
  esac
  echo ""
done
