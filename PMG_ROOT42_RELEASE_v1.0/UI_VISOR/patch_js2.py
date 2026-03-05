with open("visor.js", "r") as f:
    text = f.read()

# Add the loadRecord function to the state object
new_func = """    async loadRecord() {
        try {
            const resp = await fetch('point_001.veth');
            const data = await resp.json();
            
            // Re-render based on realistic values
            hexLabel.textContent = data.header.hex;
            this.hysteresis = data.hysteresis;
            this.isTaut = data.isTaut;
            
            // Build the string tension
            tensionDot.className = this.isTaut ? 'dot active' : 'dot warning';
            tensionStatus.textContent = this.isTaut ? 'TAUT (SHEER FACE)' : 'SLACK (HYSTERESIS DETECTED)';
            tensionStatus.style.color = this.isTaut ? 'var(--accent-green)' : 'var(--accent-red)';
            
            hysteresisVal.textContent = this.hysteresis + '°';
            
            // Build nodes from the field counts (Volume I, II, III)
            this.nodes = [];
            // Seed nodes representing fields
            const totalFields = data.header.count + data.header.measure + data.header.comm;
            for(let i=0; i<30; i++) {
                const angle = (i / 30) * Math.TAU;
                const active = i < totalFields;
                this.nodes.push({ r: RADIUS * 0.8, a: angle, type: 'seed', active: active, dR: 0, dA: 0 });
            }
            // Shell nodes
            for(let i=0; i<60; i++) {
                const angle = (i / 60) * Math.TAU;
                const r = (i % 2 === 0) ? RADIUS : RADIUS * 0.9;
                this.nodes.push({ r: r, a: angle + (Math.PI/60), type: 'shell', dR: 0, dA: 0 });
            }
            for(let i=0; i<3; i++) {
                const angle = (i / 3) * Math.TAU;
                this.nodes.push({ r: RADIUS * 0.2, a: angle, type: 'core', dR: 0, dA: 0 });
            }
            
            if (this.isTaut) {
                this.repair();
            } else {
                this.disturb();
            }

        } catch (e) {
            console.error('Failed to load record:', e);
            this.initNodes(); // fallback
        }
    },
"""

text = text.replace("    initNodes() {", new_func + "    initNodes() {")

text = text.replace("""        ctx.fillStyle = state.isTaut ? 
            (n.type === 'core' ? '#fff' : (n.type === 'seed' ? 'var(--accent-cyan)' : 'var(--text-dim)')) : 
            'var(--accent-red)';""", """        ctx.fillStyle = state.isTaut ? 
            (n.type === 'core' ? '#fff' : (n.type === 'seed' && n.active ? 'var(--accent-cyan)' : (n.type === 'seed' ? 'rgba(255,255,255,0.1)' : 'var(--text-dim)'))) : 
            'var(--accent-red)';""")

text = text.replace("""        // The 5-12-13 Connection Lines (Draw lines from shell back to core)
        if (state.isTaut && n.type === 'seed' && (idx % 3 === 0)) {""", """        // The 5-12-13 Connection Lines (Draw lines from shell back to core)
        if (state.isTaut && n.type === 'seed' && n.active && (idx % 3 === 0)) {""")


with open("visor.js", "w") as f:
    f.write(text)
