import React, { Component, ErrorInfo, ReactNode } from 'react';

interface Props {
  children?: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
    error: null
  };

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error("Uncaught error:", error, errorInfo);
  }

  public render() {
    if (this.state.hasError) {
      return (
        <div className="p-8 bg-zinc-900 border border-rose-500 rounded-xl text-rose-500 font-mono text-xs">
          <h2 className="font-bold uppercase mb-2">Lattice Intrusion Detected</h2>
          <p className="opacity-60 mb-4">{this.state.error?.message}</p>
          <button 
            onClick={() => this.setState({ hasError: false })}
            className="px-4 py-2 bg-rose-500 text-white uppercase font-black"
          >
            Re-Vitrify
          </button>
        </div>
      );
    }

    return this.children;
  }
}
