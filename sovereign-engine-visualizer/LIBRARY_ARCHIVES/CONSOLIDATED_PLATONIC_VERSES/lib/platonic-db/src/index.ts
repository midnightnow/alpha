import Database from 'better-sqlite3';
import { VOICES, HADES_GAP } from '@platonic/core';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const DB_PATH = path.resolve(__dirname, '../../platonic_memory.db');

export interface PMGNode {
    h3_index: string;
    name: string;
    resonance: number;
    state: 'Resonant' | 'Fractured';
    last_update: number;
}

class PlatonicDB {
    private db: Database.Database;

    constructor() {
        this.db = new Database(DB_PATH);
        this.init();
    }

    private init() {
        this.db.exec(`
      CREATE TABLE IF NOT EXISTS manifestations (
        h3_index TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        resonance REAL NOT NULL,
        state TEXT NOT NULL,
        last_update INTEGER NOT NULL
      );
      
      CREATE INDEX IF NOT EXISTS idx_state ON manifestations(state);
    `);
    }

    public generateNodeName(h3Index: string): string {
        // Phonetic Naming Protocol from PMG Chapter 18
        const bits = BigInt("0x" + h3Index);
        let name = "";
        const voiceValues = Object.values(VOICES);

        // We derive 7 phonemes from the H3 bits
        for (let i = 0; i < 7; i++) {
            const voiceKey = Number((bits >> BigInt(i * 3)) & 0x7n);
            name += voiceValues[voiceKey % 7];
        }
        return `Node_${name.charAt(0).toUpperCase() + name.slice(1)}`;
    }

    public getOrCreateNode(h3Index: string): PMGNode {
        const existing = this.db.prepare('SELECT * FROM manifestations WHERE h3_index = ?').get(h3Index) as PMGNode | undefined;

        if (existing) return existing;

        // manifestation logic
        const name = this.generateNodeName(h3Index);
        // Initial state determined by H3 bit-density relative to Hades Gap
        const bits = BigInt("0x" + h3Index);
        const setBits = this.countSetBits(bits);
        const state = (setBits % 2 === 0) ? 'Resonant' : 'Fractured';

        const newNode: PMGNode = {
            h3_index: h3Index,
            name,
            resonance: 1.0 - (Math.random() * HADES_GAP),
            state,
            last_update: Date.now()
        };

        this.db.prepare(`
      INSERT INTO manifestations (h3_index, name, resonance, state, last_update)
      VALUES (@h3_index, @name, @resonance, @state, @last_update)
    `).run(newNode);

        return newNode;
    }

    public updateResonance(h3Index: string, resonance: number) {
        const state = resonance < (1.0 - HADES_GAP) ? 'Fractured' : 'Resonant';
        this.db.prepare(`
      UPDATE manifestations 
      SET resonance = ?, state = ?, last_update = ?
      WHERE h3_index = ?
    `).run(resonance, state, Date.now(), h3Index);
    }

    private countSetBits(n: bigint): number {
        let count = 0;
        let temp = n;
        while (temp > 0n) {
            temp &= (temp - 1n);
            count++;
        }
        return count;
    }

    public getGlobalState() {
        return {
            totalManifestations: this.db.prepare('SELECT COUNT(*) as count FROM manifestations').get() as { count: number },
            resonantCount: this.db.prepare("SELECT COUNT(*) as count FROM manifestations WHERE state = 'Resonant'").get() as { count: number },
            fractureCount: this.db.prepare("SELECT COUNT(*) as count FROM manifestations WHERE state = 'Fractured'").get() as { count: number }
        };
    }
}

export const platonicDB = new PlatonicDB();
