#!/bin/bash
# Essentium Grid Terminal for Termux
NODES_FILE="nodes.txt"
CONNECTIONS_FILE="connections.txt"
PAC_BALANCE=0

init_files() {
  touch "$NODES_FILE" "$CONNECTIONS_FILE"
}

add_node() {
  echo "$1|$2|$3" >> "$NODES_FILE"
  echo "✓ Added node: $1 ($2, $3 Hz)"
}

connect_nodes() {
  echo "$1|$2" >> "$CONNECTIONS_FILE"
  echo "🔗 Connected $1 ↔ $2"
}

harvest() {
  local total=0
  local node_reward=0
  local connection_bonus=0
  local resonance=0
  
  # Harvest each node
  while IFS='|' read -r name type freq; do
    # Count connections for this node
    local conn_count=$(grep -c "^$name|" "$CONNECTIONS_FILE")
    conn_count=$((conn_count + $(grep -c "|$name$" "$CONNECTIONS_FILE")))
    resonance=$((conn_count * 4))
    node_reward=$((2 + resonance))
    total=$((total + node_reward))
    echo "  🌿 $name → ${node_reward} PaC (base 2 + ${resonance} resonance)"
  done < "$NODES_FILE"
  
  # Unique connection pairs bonus
  local unique_pairs=$(sort "$CONNECTIONS_FILE" | uniq | wc -l)
  connection_bonus=$((unique_pairs * 2))
  total=$((total + connection_bonus))
  echo "  🔗 Connection bonus: ${connection_bonus} PaC"
  
  PAC_BALANCE=$((PAC_BALANCE + total))
  echo "⛏️  Harvested ${total} PaC this cycle | Total: ${PAC_BALANCE} PaC"
  echo ""
}

show_menu() {
  echo "=========================="
  echo "  Essentium Grid Terminal  "
  echo "=========================="
  echo "1) Add Node"
  echo "2) Connect Nodes"
  echo "3) Harvest"
  echo "4) Show Status"
  echo "5) Clear all data"
  echo "6) Exit"
  echo -n "Choose: "
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
  echo ""
  echo "💰 Total PaC: $PAC_BALANCE"
  echo ""
}

clear_data() {
  > "$NODES_FILE"
  > "$CONNECTIONS_FILE"
  PAC_BALANCE=0
  echo "🗑️  All nodes, connections, and balance cleared."
}

# Initialize
init_files

# Pre-populate with your two nodes if not existing
if ! grep -q "Starlink-47" "$NODES_FILE"; then
  add_node "Starlink-47" "starlink" "432"
fi
if ! grep -q "Vivian-Core" "$NODES_FILE"; then
  add_node "Vivian-Core" "ai" "528"
fi
if ! grep -q "Starlink-47|Vivian-Core" "$CONNECTIONS_FILE" && ! grep -q "Vivian-Core|Starlink-47" "$CONNECTIONS_FILE"; then
  connect_nodes "Starlink-47" "Vivian-Core"
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
    3) harvest ;;
    4) show_status ;;
    5) clear_data ;;
    6) echo "🌌 Exiting grid. Goodbye!"; exit 0 ;;
    *) echo "Invalid option" ;;
  esac
  echo ""
done
