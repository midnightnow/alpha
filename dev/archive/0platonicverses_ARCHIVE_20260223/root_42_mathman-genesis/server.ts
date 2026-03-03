import express from "express";
import { createServer as createViteServer } from "vite";
import * as h3 from "h3-js";
import { platonicDB } from "@platonic/db";

async function startServer() {
  const app = express();
  const PORT = 3000;

  app.use(express.json());

  app.post("/api/name", (req, res) => {
    const { lat, lng, focus } = req.body;
    if (lat === undefined || lng === undefined) {
      return res.status(400).json({ error: "Missing lat/lng" });
    }

    const h3Index = h3.latLngToCell(lat, lng, 9);

    // Persistent Manifestation
    const node = platonicDB.getOrCreateNode(h3Index);

    // Perception Loop: Scan Neighbors (k-ring of 1)
    const neighbors = h3.gridDisk(h3Index, 1);
    const perceptionMap = neighbors.map(neighborIndex => {
      const neighborNode = platonicDB.getOrCreateNode(neighborIndex);
      return {
        address: neighborIndex,
        name: neighborNode.name,
        state: neighborNode.state
      };
    });

    // 7th Ripple Lens Focus
    const rawBits = BigInt("0x" + h3Index);
    const isObserverBitSet = (rawBits >> 7n) & 1n;
    const focusFactor = focus ? (1.0 / (focus * 17)) : 1.0;

    res.json({
      h3Index,
      name: node.name,
      resonance: node.resonance,
      state: node.state,
      perceptionMap,
      focus: {
        active: isObserverBitSet === 1n,
        factor: focusFactor
      },
      system: platonicDB.getGlobalState()
    });
  });

  app.post("/api/fracture", (req, res) => {
    const { h3Index, resonance } = req.body;
    if (!h3Index || resonance === undefined) {
      return res.status(400).json({ error: "Missing h3Index or resonance" });
    }

    try {
      platonicDB.updateResonance(h3Index, resonance);
      const node = platonicDB.getOrCreateNode(h3Index);
      res.json({ success: true, node });
    } catch (error) {
      res.status(500).json({ error: "Failed to update resonance" });
    }
  });

  // Vite middleware for development
  if (process.env.NODE_ENV !== "production") {
    const vite = await createViteServer({
      server: { middlewareMode: true },
      appType: "spa",
    });
    app.use(vite.middlewares);
  } else {
    app.use(express.static("dist"));
    app.get("*", (req, res) => {
      res.sendFile("dist/index.html", { root: "." });
    });
  }

  app.listen(PORT, "0.0.0.0", () => {
    console.log(`Server running on http://localhost:${PORT}`);
  });
}

startServer();
