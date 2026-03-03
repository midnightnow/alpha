import { motion } from 'motion/react';
import { PARABLE_CONTENT } from '../types';

export default function ParableView() {
  return (
    <div className="w-full h-full overflow-y-auto bg-[#4a3728] p-8 flex justify-center">
      <motion.article 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="vellum-page max-w-2xl w-full p-12 md:p-16 text-[#1a1108] font-serif shadow-2xl"
      >
        <div className="text-center mb-8">
          <p className="text-xs italic opacity-60 tracking-[0.2em] uppercase mb-2">
            {PARABLE_CONTENT.subtitle}
          </p>
          <h1 className="font-gothic text-4xl mb-2">{PARABLE_CONTENT.title}</h1>
          <div className="flex items-center justify-center gap-4 opacity-30">
            <div className="h-px w-16 bg-[#b8860b]" />
            <span className="text-xl">✦</span>
            <div className="h-px w-16 bg-[#b8860b]" />
          </div>
        </div>

        {PARABLE_CONTENT.chapters.map((chapter, idx) => (
          <section key={chapter.id} className="mb-12">
            <h2 className="font-display text-xs tracking-[0.2em] uppercase text-[#8b3a1a] mb-4 text-center">
              {chapter.title}
            </h2>
            <div className="relative">
              {idx === 0 && (
                <span className="float-left font-display text-7xl leading-[0.8] mr-2 mt-1 text-[#8b3a1a]">
                  I
                </span>
              )}
              <p className="text-lg leading-relaxed text-justify hyphens-auto">
                {chapter.content}
              </p>
            </div>
            {idx < PARABLE_CONTENT.chapters.length - 1 && (
              <div className="flex justify-center my-8 opacity-20">
                <span className="text-sm">◆</span>
              </div>
            )}
          </section>
        ))}

        <div className="mt-16 pt-8 border-t border-[#1a1108]/10 text-center">
          <p className="text-sm italic opacity-60 mb-4">
            {PARABLE_CONTENT.colophon}
          </p>
          <span className="font-gothic text-2xl text-[#8b3a1a] opacity-60">✦</span>
        </div>
      </motion.article>
    </div>
  );
}
