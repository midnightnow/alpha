import { useEffect, useRef, useState } from "react";

export interface OraclePacket {
    address: string;
    name: string;
    composition: string[];
    carrier: string;
    is_hades_gap: boolean;
    harmonic_bias: number;
}

export function useOracleGrid() {
    const wsRef = useRef<WebSocket | null>(null);
    const [packet, setPacket] = useState<OraclePacket | null>(null);

    useEffect(() => {
        // Attempt to connect to the bridge.py server
        const ws = new WebSocket("ws://localhost:8000/ws/grid");
        wsRef.current = ws;

        ws.onmessage = (msg) => {
            try {
                const data = JSON.parse(msg.data);
                setPacket(data);
            } catch (e) {
                console.error("Failed to parse Oracle packet:", e);
            }
        };

        ws.onopen = () => console.log("Connected to Ophanim Oracle Bridge");
        ws.onclose = () => console.log("Disconnected from Ophanim Oracle Bridge");
        ws.onerror = (e) => console.error("Oracle Bridge Error:", e);

        return () => {
            ws.close();
        };
    }, []);

    const queryGrid = (x: number, y: number, lat = 0, lng = 0) => {
        if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
            wsRef.current.send(JSON.stringify({ x, y, lat, lng }));
        }
    };

    return { packet, queryGrid };
}
