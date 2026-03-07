import React, { useMemo, useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

interface RomanRoadProps {
    visualMode: 'SQUARE' | 'HEX';
}

export const RomanRoad: React.FC<RomanRoadProps> = ({ visualMode }) => {
    const [isIdle, setIsIdle] = useState(false);

    useEffect(() => {
        let idleTimer: NodeJS.Timeout;

        const resetTimer = () => {
            setIsIdle(false);
            clearTimeout(idleTimer);
            if (visualMode === 'HEX') {
                idleTimer = setTimeout(() => setIsIdle(true), 3600000); // 1 hour
            }
        };

        window.addEventListener('mousemove', resetTimer);
        window.addEventListener('keydown', resetTimer);

        resetTimer();

        return () => {
            window.removeEventListener('mousemove', resetTimer);
            window.removeEventListener('keydown', resetTimer);
            clearTimeout(idleTimer);
        };
    }, [visualMode]);

    const gridSize = 40;
    const lines = useMemo(() => {
        const result = [];
        for (let i = -10; i <= 10; i++) {
            result.push(i);
        }
        return result;
    }, []);

    return (
        <div className="fixed inset-0 pointer-events-none z-0 overflow-hidden">
            <AnimatePresence>
                {visualMode === 'HEX' && (
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 0.15 }}
                        exit={{ opacity: 0 }}
                        className="w-full h-full relative"
                    >
                        {/* The Grid / Roman Road */}
                        <div className="absolute inset-0 flex items-center justify-center">
                            {lines.map((i) => (
                                <motion.div
                                    key={`h-${i}`}
                                    className="absolute w-full h-px bg-rose-500/20"
                                    animate={{
                                        top: isIdle ? '50%' : `calc(50% + ${i * gridSize}px)`,
                                        opacity: isIdle && i !== 0 ? 0 : 1,
                                        scaleX: isIdle && i === 0 ? 1.5 : 1
                                    }}
                                    transition={{ duration: 10, ease: "easeInOut" }}
                                />
                            ))}
                            {lines.map((i) => (
                                <motion.div
                                    key={`v-${i}`}
                                    className="absolute h-full w-px bg-rose-500/20"
                                    animate={{
                                        left: `calc(50% + ${i * gridSize}px)`,
                                        opacity: isIdle ? 0 : 1,
                                    }}
                                    transition={{ duration: 10, ease: "easeInOut" }}
                                />
                            ))}
                        </div>

                        {/* The "History" Fade */}
                        {isIdle && (
                            <motion.div
                                initial={{ opacity: 0 }}
                                animate={{ opacity: 1 }}
                                className="absolute top-1/2 left-1/2 -translate-x-1/2 mt-4 text-[10px] text-rose-500/30 uppercase tracking-[0.5em] font-mono"
                            >
                                Decaying into Roman Road...
                            </motion.div>
                        )}
                    </motion.div>
                )}
            </AnimatePresence>

            {/* The Static 90° Grid for SQUARE mode (Implicit background) */}
            {visualMode === 'SQUARE' && (
                <div className="absolute inset-0 opacity-[0.03]" style={{
                    backgroundImage: 'radial-gradient(#f43f5e 0.5px, transparent 0.5px)',
                    backgroundSize: '20px 20px'
                }} />
            )}
        </div>
    );
};
