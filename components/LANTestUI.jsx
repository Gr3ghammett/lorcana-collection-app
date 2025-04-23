import React, { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";

const WS_URL = "ws://localhost:8765";

export default function LANTestUI() {
  const [socket, setSocket] = useState(null);
  const [logs, setLogs] = useState([]);
  const [lore, setLore] = useState(0);
  const [playerId] = useState("p1");
  const [name] = useState("Greg");

  useEffect(() => {
    const ws = new WebSocket(WS_URL);
    setSocket(ws);

    ws.onopen = () => {
      ws.send(
        JSON.stringify({
          type: "player_joined",
          payload: {
            player_id: playerId,
            name,
            deck: {
              name: "Test Deck",
              cards: ["test_card_1", "test_card_2"]
            }
          }
        })
      );
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setLogs((prev) => [...prev, data]);
      if (data.type === "update_lore" && data.payload.player_id === playerId) {
        setLore((prev) => prev + data.payload.amount);
      }
    };

    return () => ws.close();
  }, [playerId, name]);

  const sendAction = (action) => {
    if (!socket) return;
    socket.send(
      JSON.stringify({
        type: "card_action",
        payload: {
          player_id: playerId,
          card_id: "test_card_1",
          action,
          target: "none",
          zone: "play"
        }
      })
    );
  };

  const gainLore = () => {
    if (!socket) return;
    socket.send(
      JSON.stringify({
        type: "update_lore",
        payload: {
          player_id: playerId,
          amount: 1
        }
      })
    );
  };

  return (
    <div className="p-4 space-y-4">
      <h1 className="text-xl font-bold">LAN Multiplayer Test UI</h1>

      <div className="space-x-2">
        <Button onClick={() => sendAction("quest")}>Quest</Button>
        <Button onClick={() => sendAction("play")}>Play</Button>
        <Button onClick={() => sendAction("ink")}>Ink</Button>
        <Button onClick={gainLore}>Gain 1 Lore</Button>
      </div>

      <Card>
        <CardContent>
          <p>Lore: {lore}</p>
        </CardContent>
      </Card>

      <Card>
        <CardContent>
          <p className="font-bold">Event Log:</p>
          <div className="max-h-64 overflow-auto text-sm mt-2">
            {logs.map((log, idx) => (
              <pre key={idx}>{JSON.stringify(log, null, 2)}</pre>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
